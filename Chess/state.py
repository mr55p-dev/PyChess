import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Union
from math import ceil

from Chess.constants import WinState, BLACK, WHITE, ResultKeys
from Chess.coordinate import Move
from Chess.exceptions import InvalidMoveError
from Chess.result import ResultSet
from Chess.types import Piece, Position


class Board(ABC):
    """Board.
    This wraps a games state and provides utilities for interacting with it and calculating
    the moves which are available in the position. It can also execute moves on the current
    state which performs internal mainpulation rather than copying, since instantiating
    this object is kind of slow...

    Subclasses must implement _psuedolegal_moves and override the __init__ method to include a
    Position parmeter, since i am too lazy to duplicate the logic in get_king_start et al.
    """

    def __init__(self,
                 starting_position: Tuple[List[Piece], List[Piece]] = None,
                 to_move: int = WHITE,
                 can_castle: str = "KQkq",
                 en_passant_opts: str = "-",
                 half_turn: int = 0,
                 turn: int = 1,
                 ) -> None:
        # Setup a logger
        self.log = logging.getLogger("State")

        # Store the fen information given and piece representations
        # Construct a map of location: piece
        self._white, self._black = starting_position or self.new_game()
        self._turn = turn
        self._half_turn = half_turn

        # Define convenient variables so we know which pieces are moving
        self.to_move = to_move
        self._opposition = WHITE if to_move == BLACK else BLACK

        # Setup properties which we will later bind in the `calculate` function
        self.__is_check = []
        self.__win_state = WinState.cont
        self._evaluation = 0

        # This is just while castling and en-passant is not implemented
        self._castle = self.__parse_castle(can_castle) # castle[4] : white kingside, queenside, black kingside, queenside

        # Generate all the important stuff
        self.calculate()

        # Create a history list
        self.history = list(self.to_fen())

    def __repr__(self) -> str:
        """__repr__.
        Provide a basic string representation of the board.

        :rtype: str
        """

        board = [[" " for _ in range(8)] for _ in range(8)]
        for loc, piece in self.loc_map.items():
            board[loc.i][loc.j] = piece.kind
        return "\n".join([" ".join(list(row)) for row in board])

    def __parse_castle(self, castle_str) -> List[bool]:
        """__parse_castle.
        Turn the castling move notation from FEN strings into
        the representation used by Board.

        :param self:
        :param castle_str:
        :rtype: List[bool]
        """
        castling = [False, False, False, False]
        if castle_str == "-": return castling

        for i in castle_str:
            if i == "K": castling[0]    = True
            elif i == "Q": castling[1]  = True
            elif i == "k": castling[2]  = True
            elif i == "q": castling[3]  = True
            
        return castling

    @abstractmethod
    def _psuedolegal_moves(self, pieces: List[Piece]) -> ResultSet:
        """Must be implemented by a subclass"""
        ...

    def __filter_moves(self, results: ResultSet) -> ResultSet:
        """__filter_moves.
        Applies the constraints of checks and pins to the given "psuedolegal" results.
        This only needs to be done once each turn to get all the fully legal moves of the
        allied pieces. ALthough this does not account for castling moves - that is handled
        by the parser and state variables instead since it applies to the whole lifetime
        of the state.

        :param self:
        :param results:
        :type results: ResultSet
        :rtype: ResultSet
        """
        # Fetches enemy psuedolegal moves and returns attacking pieces
        attackers = self.__is_check[:]
        king = self.__get_king()
        if len(attackers) > 1:
            # Remove all other piece moves
            not_king = [i for i in results.keys() if i != king]
            results.clear_set(not_king)

        if king in results:
            # Mark the king as captured
            king.is_active = False

            # Calculate the moves for the enemy pieces without the king there
            opposing_moves = self._psuedolegal_moves(self.opposing)

            # Fix that
            king.is_active = True

            # Filter out moves which are to spaces controlled attacks). Also
            # filter out captures of "defended" pieces which would result in the king being in check.
            controlled_squares = opposing_moves.all_attack + opposing_moves.all_defend
            results[king] = results[king].filter_all(lambda x: x not in controlled_squares)

        attacker = None
        if len(attackers) == 1:
            attacker = attackers.pop()
            assert attacker

        opposing_moves = self._psuedolegal_moves(self.opposing)
        for piece in results.keys():
            # If there is only one attacker, non-king pieces can only move on the path attacker - king
            # If the piece is a king then fetch the king_moves from __filter_king_moves algorithm
            if piece == king:
                continue
            if attacker:
                # Get the path from the attacker to the king, filter moves to only that path.
                path = self.piece_map[attacker].path_to(self.piece_map[king])
                results[piece] = results[piece].filter_valid(lambda x: x in path)

            # Finally, if attackers <=1 resolve pins.
            piece_loc = self.piece_map[piece]
            if pin := opposing_moves.lookup_pin(piece_loc):
                # Only valid moves for a pinned piece will be on the axis of the opposing piece
                # and king.
                path = self.piece_map[pin].path_to(self.piece_map[king])
                results[piece] = results[piece].filter_valid(lambda x: x in path)

        return results

    def __update_piece(self,
                       piece: Piece,
                       new_position: Position = None,
                       is_active = None
                       ) -> None:
        """__update_piece.
        Convenience method for safely updating the properties of a piece.

        :param self:
        :param piece:
        :type piece: Piece
        :param is_active:
        :rtype: None
        """

        if new_position:
            piece._position = new_position
        if is_active:
            piece.is_active = is_active

    def __get_king(self) -> Piece:
        """__get_king.
        Returns the kind of the side moving this turn

        :param self:
        :rtype: King
        """
        return [i for i in self.moving if i.kind == "K"].pop()

    def __evaluate_check(self) -> List[Piece]:
        """__evaluate_check.
        Calculates if a position is in check (if the king is under attack).
        Returns a list of all the pieces which directly attack the king.

        :param self:
        :rtype: List[Piece]
        """
        moves = self._psuedolegal_moves(self.opposing)
        king = self.__get_king()

        king_loc = self.piece_map[king]
        moves = moves.filter_by_move_type(ResultKeys.capture, lambda x: x == king_loc)
        return [i for i in moves if moves[i][ResultKeys.capture]]

    def __evaluate_mate(self) -> WinState:
        """__evaluate_mate.
        Uses the fully legal moves calculated for this state to determine if a position
        is checkmate or stalemate.

        Returns keys defined in WinState.

        :param self:
        :rtype: WinState
        """
        if not self._allowed_moves.all_valid:
            return WinState.mate if self.__is_check else WinState.stalemate
        return WinState.cont

    def legal_moves(self, pieces: List[Piece] = None) -> ResultSet:
        """legal_moves.
        External api for interacting with all the legal moves in a position.
        Calling this forces a full recalculation of the position.

        :param self:
        :param pieces: List of pieces to calculate on
        :type pieces: list[Piece]
        """
        # Either use all the moving pieces, or the list of pieces
        # passed which also exist in the moving side.
        pieces = self.moving if not pieces else [i for i in pieces if i in self.moving]
        # Get psuedolegal moves for allied pieces
        psl = self._psuedolegal_moves(pieces)

        # Filter the moves 
        results = self.__filter_moves(psl)

        # Fix the king passive moves if castling is allowed.
        king = self.__get_king()
        for i in self.valid_castle():
            results[king][ResultKeys.passive].append(i)

        return results

    def calculate(self) -> None:
        """calculate.
        Should be called on every change of state.
        Updates internal attributes used in calculation and rechecks the state of the game.
        All the legal moves are redefined for the side moving and the win state is updated.

        :param self:
        :rtype: None
        """
        self.__loc_map = { piece.position: piece for piece in self.moving + self.opposing if piece.is_active}
        self.__piece_map = { piece: piece.position for piece in self.moving + self.opposing if piece.is_active}

        self.__is_check = self.__evaluate_check()

        # Calculate the possible moves
        self._allowed_moves = self.legal_moves(self.moving)

        self.__win_state = self.__evaluate_mate()

    def get_king_start(self, colour: Union[int, bool]) -> Position:
        return self.Position("E1") if colour else self.Position("E8")

    def get_rook_start(self, colour) -> Tuple[Position, Position]:
        return (
            self.Position("H1"),
            self.Position("A1")
            ) if colour else (
                self.Position("H8"),
                self.Position("A8")
            )

    def get_castled_rook(self, colour, type: str) -> Position:
        rank = 0 if colour else 7
        file = 3 if type == "long" else 5
        return self.Position(rank, file)

    def valid_castle(self) -> List[Position]:
        """valid_castle.
        Gets the positions which would need to be entered for a valid castling move to be executed.
        Walks through a checklist of conditions which must all be met to allow castling to be valid
        such as not in check, king and rook have not moved, no pieces in between etc...

        :param self:
        :rtype: List[Position]
        """
        king_start = self.get_king_start(self.to_move)
        rook_short, rook_long = self.get_rook_start(self.to_move)

        if self.to_move:
            castle_short = self._castle[0]
            castle_long  = self._castle[1]
        else:
            castle_short = self._castle[2]
            castle_long  = self._castle[3]

        if not (castle_short or castle_long):
            return []

        if self.__is_check:
            return []

        king = self.__get_king()
        if self.piece_map[king] != king_start:
            return []

        if castle_long and castle_short:
            rooks = [rook_short, rook_long]
        elif castle_long:
            rooks = [rook_long]
        else:
            rooks = [rook_short]

        valid = []
        for rook in rooks:
            if rook not in self.loc_map:
                continue

            if self.loc_map[rook].kind != "R":
                continue

            path = self.piece_map[king].path_to(rook)
            path = [i for i in path if i != self.piece_map[king]]
            if [i for i in path if i in self.loc_map]:
                continue

            enemy_moves = self._psuedolegal_moves(self.opposing)
            if [i for i in path if i in enemy_moves.all_valid + enemy_moves.all_attack]:
                continue

            final = [king_start.i, king_start.j]
            final[1] += -2 if rook.j == 0 else 2
            final = (final[0], final[1])

            valid.append(self.Position(final))

        return valid

    def move(self, mov: Move) -> 'Board':
        """Runs a move in the current state. Takes a `Move` object.
        Reupdates the state at the end of the call.

        :param self:
        :param mov:
        :type mov: Move
        """

        if mov.start not in self.loc_map:
            self.log.error(f"{mov.start} does not appear as a piece in loc_map")
            raise InvalidMoveError(f"{mov.start} does not appear as a piece in loc_map")

        # Set the new position
        moving_piece = self.loc_map[mov.start]
        self.__update_piece(moving_piece, new_position=mov.end)

        # Check if the move is a castle
        if mov.is_castle:
            # Get the location of the rook
            rook_start = self.get_rook_start(self.to_move)[0 if mov.is_castle == "short" else 1]
            rook = self.loc_map[rook_start] # Get the rook object at that position
            rook_end = self.get_castled_rook(self.to_move, mov.is_castle) # Get the end position
            self.__update_piece(rook, rook_end)

            if self.to_move: # Disallow future castling
                self._castle[0] = False
                self._castle[1] = False
            else:
                self._castle[2] = False
                self._castle[3] = False

        if self.to_move:
            self.to_move = BLACK
        else:
            self.to_move = WHITE
            self._turn = self._turn + 1

        self._half_turn = self._half_turn + 1

        # Remove captured pieces so they dont remain forever.
        if mov.takes:
            captured = self.loc_map[mov.end]
            self.__update_piece(captured, is_active=False)
            if captured.kind == "P":
                self._half_turn = 0

        self.calculate()

        # Save the FEN string to the history
        self.history.append(self.to_fen())

        return self

    def to_fen(self) -> str:
        """to_fen.
        Calculate the FEN string of the current state

        :param self:
        :rtype: str
        """
        fields = []
        ranks = [["" for _ in range(8)] for _ in range(8)]
        # The rank of a piece will be calculated as 7 - i; 
        # In FEN the 8th rank (list index 7) is at i=0
        for position, piece in self.loc_map.items():
            symbol = piece.kind
            if piece.colour == BLACK: symbol = symbol.lower()
            ranks[7-position.i][position.j] = symbol
        # Reduce the ranks down to proper notation
        # Hacky but itll do
        irreducable_ranks = []
        for rank in ranks:
            new_rank = []
            counter = 0
            for iter, char in enumerate(rank):
                if not char:
                    counter += 1
                if char and counter:
                    new_rank.append(str(counter))
                    counter = 0
                elif iter == 7 and counter > 0:
                    new_rank.append(str(counter))
                    continue
                new_rank.append(char)
            irreducable_ranks.append("".join(new_rank))
        
        fields.append("/".join(irreducable_ranks))
        
        next_move = "w" if self.to_move == WHITE else 'b'
        fields.append(next_move)

        castle_rep = ["K", "Q", "k", "q"]
        can_castle = [v for i, v in enumerate(castle_rep) if self._castle[i]]

        can_castle = "".join(can_castle)
        if not can_castle: can_castle = "-"

        # Since i am not ready to finish FEN we will add default data to the end
        fields.append(can_castle) # Right to castle
        fields.append("-") # En-passant right
        fields.append(str(self._half_turn)) # Half move clock ish...
        fields.append(str(self._turn)) # Full move clock
        return " ".join(fields)

    @property
    def moving(self) -> List[Piece]:
        """moving.
        All the active pieces moving on this turn.

        :param self:
        :rtype: List[Piece]
        """
        if self._to_move == BLACK:
            return [i for i in self._black if i.is_active]
        else:
            return [i for i in self._white if i.is_active]

    @property
    def opposing(self) -> List[Piece]:
        """opposing.
        All the active pieces NOT moving on this turn.

        :param self:
        :rtype: List[Piece]
        """
        if self._to_move == WHITE:
            return [i for i in self._black if i.is_active]
        else:
            return [i for i in self._white if i.is_active]

    @property
    def all_pieces(self) -> List[Piece]:
        """all_pieces.
        All the active pieces on the board

        :param self:
        :rtype: List[Piece]
        """
        return [i for i in self._white + self._black if i.is_active]

    @property
    def loc_map(self) -> Dict[Position, Piece]:
        """loc_map.
        Convenient mapping of Positions and the piece occupying them.

        :param self:
        :rtype: Dict[Position, Piece]
        """
        return self.__loc_map

    @property
    def piece_map(self) -> Dict[Piece, Position]:
        """piece_map.
        Reverse mapping to loc_map, to speed up inverse lookups.

        :param self:
        :rtype: Dict[Piece, Position]
        """
        return self.__piece_map

    @property
    def turn(self) -> int:
        """turn.
        The turn number (increments after black moves).

        :param self:
        :rtype: int
        """
        return self._turn

    @property
    def is_check(self) -> List[Piece]:
        return self.__is_check

    @property
    def is_mate(self) -> bool:
        return self.__win_state == WinState.mate
    
    @property
    def is_stale(self) -> bool:
        return self.__win_state == WinState.stalemate

    @property
    def to_move(self) -> int:
        """to_move.
        The colour which is next to apply a move.

        :param self:
        :rtype: int
        """
        return self._to_move

    @to_move.setter
    def to_move(self, player) -> None:
        self._to_move = player


    @property
    def moves(self) -> ResultSet:
        """moves.
        The moves of the side which is next to apply a move

        :param self:
        :rtype: ResultSet
        """
        return self._allowed_moves
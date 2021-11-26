from enum import Enum, auto
from typing import Dict, List, Optional, Tuple

from Chess.constants import BLACK, WHITE
from Chess.coordinate import Move, Position
from Chess.result import ResultSet, ResultKeys, Result
from Chess.exceptions import InvalidFormat
from Chess.helpers import new_game
from Chess.pieces import King, Piece

class MoveSignal(Enum):
    blocked         = 0
    capture         = 1
    empty           = 2
    checking_attack = 3
    disallowed      = 4
    attacks         = 5


class WinState(Enum):
    cont = auto()
    mate = auto()
    stalemate = auto()
    draw = auto()
    move_timeout = auto()


class Board():
    # Static attributes
    BLOCKED         = 0
    CAPTURE         = 1
    EMPTY           = 2
    CHECKING_ATTACK = 3
    DISALLOWED      = 4
    ATTACKS         = 5

    CHECKMATE = 10
    STALEMATE = 20
    CONTINUE  = 30
    gametype = Tuple[List[Piece], List[Piece]]

    def __init__(self,
                 starting_position: Tuple[List[Piece], List[Piece]] = new_game(),  # type: ignore
                 to_move: int = WHITE,
                 turn: int = 1,
                 can_castle: str = "KQkq",
                 other_fen_params = []) -> None:

        # Store the fen information gi en and piece representations
        # Construct a map of location: piece
        self._white, self._black = starting_position
        self._turn = turn

        # Define convenient variables so we know which pieces are moving
        self._to_move = to_move
        self._opposition = WHITE if to_move == BLACK else BLACK

        # Setup properties which we will later bind in the `calculate` function
        self.__is_check = []
        self.__win_state = WinState.cont
        self._evaluation = 0

        # This is just while castling and en-passant is not implemented
        self._castle = self.__parse_castle(can_castle) # castle[4] : white kingside, queenside, black kingside, queenside
        self.other_FEN_params = other_fen_params

        self.calculate()

    def __repr__(self) -> str:
        """__repr__.
        Provide a basic string representation of the board.

        :rtype: str
        """

        board = [[" " for _ in range(8)] for _ in range(8)]
        for loc, piece in self.loc_map.items():
            board[loc.i][loc.j] = piece.kind
        return "\n".join([" ".join([cell for cell in row]) for row in board])

    def __parse_castle(self, castle_str) -> List[bool]:
        castling = [False, False, False, False]
        if castle_str == "-": return castling

        for i in castle_str:
            if i == "K": castling[0]    = True
            elif i == "Q": castling[1]  = True
            elif i == "k": castling[2]  = True
            elif i == "q": castling[3]  = True
            
        return castling


    def __allowed_move(self, position, piece) -> MoveSignal:
        """__allowed_move.
        Decides if a move is valid and what type of move it is if so.

        Returns self.EMPTY if a move is allowed
        Returns self.BLOCKED if a move is blocked by an allied piece
        Returns self.CHECKING_ATTACK if a move is a check
        Returns self.CAPTURE if a move is a capture
        Returns self.DISALLOWED if a move is not allowed (such as pawn push)

        :param position:
        :param piece:
        """
        capture_allowed = True
        passive_allowed = True
        # Faster than using isinstance calls
        if piece.kind == 'P':

            start_position = self.piece_map[piece]
            # The pieces start at either i=1 or i=6
            start = 1 if piece.colour == WHITE else 6
            has_moved = bool(start - start_position._i)
            if start_position._j - position._j != 0:
                passive_allowed = False
            if start_position._j - position._j == 0:
                capture_allowed = False
            if has_moved and start_position._i - position._i in [2, -2]:
                return MoveSignal.disallowed

        if position in self.loc_map.keys():
            occupied_by = self.loc_map[position]
            if occupied_by.colour == piece.colour: return MoveSignal.blocked
            else:
                if isinstance(occupied_by, King): return MoveSignal.checking_attack
                else:
                    if capture_allowed: return MoveSignal.capture
                    else: return MoveSignal.disallowed
        else:
            if passive_allowed: 
                return MoveSignal.empty
            elif capture_allowed: 
                return MoveSignal.attacks
            else: 
                return MoveSignal.disallowed

    def __psuedolegal_moves(self, pieces: List[Piece]) -> ResultSet:
        results = ResultSet()
        for piece in pieces:
            result = Result()
            for dir in piece.projections:
                # Iterate over all the directions a piece can move in
                # Reset the pinned marker.
                pinned = None
                for step in range(1, piece.distance + 1):
                    # Count up all the steps the piece can take until it meets
                    # a stop condition
                    try: landed_on = self.piece_map[piece] + (dir * step)
                    except InvalidFormat: break
                    
                    if (allowed:=self.__allowed_move(landed_on, piece)) == MoveSignal.empty:
                        # Store empty squares if we are not looking for a pin
                        # if pinned == None: results[piece][results.PASSIVE].append(landed_on)
                        if pinned == None: result[ResultKeys.passive].append(landed_on)
                    elif allowed == MoveSignal.capture:
                        # Store a capture if we are not looking for a pin
                        if pinned == None:
                            # results[piece][results.CAPTURE].append(landed_on) 
                            result[ResultKeys.capture].append(landed_on) 
                            pinned = self.loc_map[landed_on]
                        # Stop looking for a pin if we encounter a piece that isnt the king
                        else: break
                    elif allowed == MoveSignal.checking_attack:
                        # Store a check if we are not looking for a pin
                        # if pinned == None: results[piece][results.CAPTURE].append(landed_on); break
                        if pinned == None: result[ResultKeys.capture].append(landed_on); break
                        # Store a pin if we found one
                        # else: results[piece][results.PIN].append(pinned); break
                        else: result[ResultKeys.pin].append(landed_on); break
                    elif allowed == MoveSignal.blocked:
                        # Store a piece as defended if we are not looking for a pin
                        # if pinned == None: results[piece][results.DEFEND].append(landed_on); break
                        if pinned == None: result[ResultKeys.defend].append(landed_on); break
                        # Stop looking if there is another piece before the king
                        else: break
                    elif allowed == MoveSignal.attacks and pinned == None: 
                        # Store a pawns attacks in a separate list
                        # results[piece][results.ATTACK].append(landed_on); break
                        result[ResultKeys.attack].append(landed_on); break
                    elif allowed == MoveSignal.disallowed: break
            results[piece] = result

        return results
     
    def __filter_moves(self, results: ResultSet) -> ResultSet:
        # Fetches enemy psuedolegal moves and returns attacking pieces
        attackers = self.__evaluate_check()
        king = self.__get_king()
        if len(attackers) > 1:
            # Remove all other piece moves
            not_king = [i for i in results.keys() if i != king]
            results.clear_set(not_king)

            # Remove the allied king from the state
            moving_pieces = self.moving
            king_index = moving_pieces.index(king)
            temp_king = moving_pieces.pop(king_index)
            
            # Calculate the moves for the enemy pieces without the king there
            opposing_moves = self.__psuedolegal_moves(self.opposing)
            moving_pieces.insert(king_index, temp_king)

            # Filter out moves which are to spaces controlled (either through valid moves,
            # psuedo moves or pawn "hypothetical" moves (stored as attacks). Also
            # filter out captures of "defended" pieces which would result in the king being in check.
            invalid_squares = \
                opposing_moves.all_valid + opposing_moves.all_attack + opposing_moves.all_defend
            results[king] = results[king].filter_all(lambda x: x not in invalid_squares)

        for piece in results.keys():
            # If there is only one attacker, non-king pieces can only move on the path attacker - king
            # If the piece is a king then fetch the king_moves from __filter_king_moves algorithm
            if len(attackers) == 1:
                attacker = attackers.pop()
                assert attacker

                # Get the path from the attacker to the king, filter moves to only that path.
                path = self.piece_map[attacker].path_to(self.piece_map[king])
                results[piece] = results[piece].filter_all(lambda x: x in path)

            # Finally, if attackers <=1 resolve pins.
            opposing_moves = self.__psuedolegal_moves(self.opposing)
            pin = opposing_moves.lookup_pin(self.piece_map[piece])
            if pin:
                # Only valid moves for a pinned piece will be on the axis of the opposing piece
                # and king.
                path = self.piece_map[pin].path_to(self.piece_map[king])
                results[piece] = results[piece].filter_all(lambda x: x in path)

        return results

    def __update_piece(self,
                       piece: Piece,
                       new_position = None,
                       is_active = None
                       ) -> None:

        if isinstance(new_position, Position):
            # Change this to just update the map in the future.
            piece._position = new_position
        if isinstance(is_active, bool):
            piece.is_active = is_active

    def __get_king(self) -> King:
        return [i for i in self.moving if isinstance(i, King)].pop()

    def __evaluate_check(self) -> List[Piece]:
        moves = self.__psuedolegal_moves(self.opposing)
        king = self.__get_king()

        king_loc = self.piece_map[king]
        moves = moves.filter_by_move_type(ResultKeys.capture, lambda x: x == king_loc)
        return [i for i in moves if moves[i][ResultKeys.capture]]

    def __evaluate_mate(self) -> WinState:
        """_evaluate_mate.
        Will evaluate if the position is checkmate or stalemate.
        Returns one of self.CONTINUE, self.STALEMATE or self.CHECKMATE

        :rtype: int
        """
        moves = self.legal_moves(self.moving)

        if not moves.all_valid: 
            if self.__is_check: return WinState.mate
            else: return WinState.stalemate
        return WinState.cont

    def _evaluate_score(self):
        """_evaluate_score."""
        pass

    def legal_moves(self, pieces: list[Piece] = None) -> ResultSet:
        """get_move_set.
        Wrapper to get a set of moves instead of just those for a singular piece

        :param self:
        :param pieces:
        :type pieces: list[Piece]
        :rtype: ResultSet
        """
        if not pieces: pieces = self.moving
        # Get psuedolegal moves for allied pieces
        psl = self.__psuedolegal_moves(pieces)

        # Filter the moves 
        return self.__filter_moves(psl)

    def calculate(self) -> None:
        self.__is_check = self.__evaluate_check() 
        self.__win_state = self.__evaluate_mate() 

        # Calculate the possible moves
        self._allowed_moves = self.legal_moves(self.moving)


    def move(self, mov: Move) -> bool:
        """Runs a move in the current state. Takes a `Move` object.
        This method does NOT implement full validity checks. Raises `InvalidStateChange` exception.

        :param self:
        :param mov:
        :type mov: Move
        """
        try: moving_piece = self.loc_map[mov.start]
        except KeyError: raise ValueError(f"Move.start is invalid: {mov.start}")
        self.__update_piece(moving_piece, new_position=mov.end)

        # Remove captured pieces so they dont remain forever.
        if mov.takes:
            captured = self.loc_map[mov.end]
            self.__update_piece(captured, is_active=False)

        if self._to_move:
            self._to_move = BLACK
        else:
            self._to_move = WHITE
            self._turn = self._turn + 1

        self.calculate()
        return True


    def to_fen(self) -> str:
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
        
        next_move = "w" if self._to_move == WHITE else 'b'
        fields.append(next_move)

        castle_rep = ["K", "Q", "k", "q"]
        can_castle = [v for i, v in enumerate(castle_rep) if self._castle[i]]

        # Since i am not ready to finish FEN we will add default data to the end
        fields.append("".join(can_castle))
        fields.append("-") # En-passant right
        fields.append(str(0)) # Half move clock ish...
        fields.append(str(self._turn)) # Full move clock
        return " ".join(fields)

    @property
    def moving(self) -> List[Piece]:
        """_get_moving.
        Returns the active pieces moving in this state.

        :rtype: List[Piece]
        """
        if self._to_move == BLACK:
            return [i for i in self._black if i.is_active]
        else:
            return [i for i in self._white if i.is_active]

    @property
    def opposing(self) -> List[Piece]:
        """_get_opposing.
        Returns the active pieces not moving in this state.

        :rtype: List[Piece]
        """
        if self._to_move == WHITE:
            return [i for i in self._black if i.is_active]
        else:
            return [i for i in self._white if i.is_active]
    @property
    def loc_map(self) -> Dict[Position, Piece]:
        return { piece.position: piece for piece in self.moving + self.opposing }
    
    @property
    def piece_map(self) -> Dict[Piece, Position]:
        return { piece: piece.position for piece in self.moving + self.opposing }

    @property 
    def turn(self) -> int:
        return self._turn

    @property
    def pos_map(self) -> dict:
        """Convenience attribute
        Returns a hash map of each occupied position and its associated piece"""
        return self.loc_map

    @property
    def pieces(self) -> list:
        return self._black + self._white

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
        """to_move."""
        return self._to_move

    @property
    def allied_moves(self) -> ResultSet:
        return self.legal_moves()

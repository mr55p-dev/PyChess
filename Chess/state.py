from enum import Enum, auto
from itertools import repeat
from typing import Dict, List, Tuple

from Chess.constants import BLACK, WHITE
from Chess.coordinate import Move, Position
from Chess.exceptions import InvalidFormat
from Chess.helpers import new_game
from Chess.pieces import King, Pawn, Piece, Rook
from Chess.result import Result, ResultKeys, ResultSet

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

def new_pieces():
    yield new_game()


class Board():
    def __init__(self,
                 starting_position: Tuple[List[Piece], List[Piece]] = None,
                 to_move: int = WHITE,
                 can_castle: str = "KQkq",
                 en_passant_opts: str = "-",
                 half_moves_since_pawn: int = 0,
                 turn: int = 1,
                 ) -> None:

        # Store the fen information gi en and piece representations
        # Construct a map of location: piece
        if starting_position: self._white, self._black = starting_position
        else: self._white, self._black = new_game()
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


        occupier = None
        if position in self.loc_map:
            occupier = self.loc_map[position]

        if not occupier:
            if passive_allowed: return MoveSignal.empty
            elif capture_allowed: return MoveSignal.attacks
        elif occupier.colour == piece.colour:
            if capture_allowed: return MoveSignal.blocked
        else:
            if capture_allowed and isinstance(occupier, King):
                return MoveSignal.checking_attack
            elif capture_allowed:
                return MoveSignal.capture
        return MoveSignal.disallowed

    def __psuedolegal_moves(self, pieces: List[Piece]) -> ResultSet:
        # Preallocate the dict to hpoefully speed things up a bit
        results = ResultSet(dict.fromkeys(pieces))
        for piece in pieces:
            result = Result()
            for dir in piece.projections:
                # Iterate over all the directions a piece can move in
                # Reset the pinned marker.
                pinned = None
                for step in range(1, piece.distance + 1):
                    # Count up all the steps the piece can take until it meets
                    # a stop condition
                    loc = self.piece_map[piece]
                    ni = loc.i + (dir.i * step)
                    nj = loc.j + (dir.j * step)
                    if ni > 7 or ni < 0 or nj > 7 or nj < 0: break
                    landed_on = Position((ni, nj))
                    # try: landed_on = self.piece_map[piece] + (dir * step)
                    # except InvalidFormat: break
                    allowed = self.__allowed_move(landed_on, piece)

                    # Reordered expressions to make use of short-circuiting
                    if not pinned and allowed == MoveSignal.empty :
                        # Do not store this location if we are searching for a pin
                        # Store this location as a passive, and an attack for pieces which are
                        # not pawns
                        if not isinstance(piece, Pawn):
                            result[ResultKeys.attack].append(landed_on)
                        result[ResultKeys.passive].append(landed_on)
                    elif not pinned and allowed == MoveSignal.capture:
                        # Do not store a capture on a normal piece if looking for a pin
                        # Store a piece which can be captured as a capture, and an attack
                        # since that square is controlled by the piece so an enemy king could not
                        # move there.
                        result[ResultKeys.capture].append(landed_on)
                        result[ResultKeys.attack].append(landed_on)
                        # Snapshot the current location and check if this piece which can
                        # be captures is pinned to the king.
                        pinned = Position((landed_on.i, landed_on.j))
                    elif not pinned and allowed == MoveSignal.attacks: 
                        # Do not save an attack if we are scanning for a pin
                        # This will only ever be pawn attacks (to separate their passive
                        # capturing and non-capturing moves)
                        result[ResultKeys.attack].append(landed_on); break
                    elif allowed == MoveSignal.checking_attack:
                        # Store a check if we are not looking for a pin
                        if pinned:
                            result[ResultKeys.pin].append(pinned) 
                            break
                        result[ResultKeys.capture].append(landed_on) 
                        break
                    elif allowed == MoveSignal.blocked:
                        # Do not consider a piece defended if we are looking at a pin
                        if pinned: break
                        # Store a piece as defended if an allied piece sees it
                        result[ResultKeys.defend].append(landed_on)
                        break
                    elif allowed == MoveSignal.disallowed:
                        # Do not continue looking if a move is disallowed
                        break

            results[piece] = result

        return results
     
    def __filter_moves(self, results: ResultSet) -> ResultSet:
        # Fetches enemy psuedolegal moves and returns attacking pieces
        attackers = self.__is_check[:]
        king = self.__get_king()
        if len(attackers) > 1:
            # Remove all other piece moves
            not_king = [i for i in results.keys() if i != king]
            results.clear_set(not_king)

        if king in results:
            # Mark the king as captured
            king.active = False
            
            # Calculate the moves for the enemy pieces without the king there
            opposing_moves = self.__psuedolegal_moves(self.opposing)

            # Fix that
            king.active = True

            # Filter out moves which are to spaces controlled attacks). Also
            # filter out captures of "defended" pieces which would result in the king being in check.
            controlled_squares = opposing_moves.all_attack + opposing_moves.all_defend
            results[king] = results[king].filter_all(lambda x: x not in controlled_squares)

        attacker = None
        if len(attackers) == 1:
            attacker = attackers.pop()
            assert attacker

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
            opposing_moves = self.__psuedolegal_moves(self.opposing)
            pin = opposing_moves.lookup_pin(self.piece_map[piece])
            if pin:
                # Only valid moves for a pinned piece will be on the axis of the opposing piece
                # and king.
                path = self.piece_map[pin].path_to(self.piece_map[king])
                results[piece] = results[piece].filter_valid(lambda x: x in path)

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

        if not self._allowed_moves.all_valid:
            if self.__is_check: return WinState.mate
            else: return WinState.stalemate
        return WinState.cont

    def _evaluate_score(self):
        """_evaluate_score."""
        pass

    def legal_moves(self, pieces: list[Piece] = None) -> ResultSet:
        """get_move_set.
        Wrapper to get a set of moves instead of just those for a singular piece. Works only with
        the side "moving".

        :param self:
        :param pieces:
        :type pieces: list[Piece]
        :rtype: ResultSet
        """
        # Either use all the moving pieces, or the list of pieces
        # passed which also exist in the moving side.
        if not pieces: pieces = self.moving
        else: pieces = [i for i in pieces if i in self.moving]

        # Get psuedolegal moves for allied pieces
        psl = self.__psuedolegal_moves(pieces)

        # Filter the moves 
        results = self.__filter_moves(psl)

        # Fix the king passive moves if castling is allowed.
        king = self.__get_king()
        for i in self.valid_castle():
            results[king][ResultKeys.passive].append(i)

        return results

    def calculate(self) -> None:
        self.__loc_map = { piece.position: piece for piece in self.moving + self.opposing }
        self.__piece_map = { piece: piece.position for piece in self.moving + self.opposing }

        self.__is_check = self.__evaluate_check()

        # Calculate the possible moves
        self._allowed_moves = self.legal_moves(self.moving)

        self.__win_state = self.__evaluate_mate()

    def valid_castle(self) -> List[Position]:
        """
        Case right to castle is not true:
            No move
        Case in check:
            No move
        Case king not on start:
            No move
        Case Rook not on start:
            No move
        Case Any square between king and rook occupied:
            No move
        Case Attack on any square in castle path:
            No move

        Allow castle
        Add move to king passives

        - Listen for O-O or O-O-O
        - For WHITE: (king then rook)
            CASTLE_LONG  = (G1, F1)
            CASTLE_SHORT = (C1, D1)
        - For BLACK:
            CASTLE_LONG  = (G8, F8)
            CASTLE_SHORT = (C8, D8)
        - Check if castling is valid ^
        - Do the move
        - Update the right to castle for this side.
        """ 
        if self._to_move:
            castle_short = self._castle[0]
            castle_long  = self._castle[1]

            king_start = Position("E1")

            rook_short = Position("H1")
            rook_long  = Position("A1")
        else:
            castle_short = self._castle[2]
            castle_long  = self._castle[3]

            king_start = Position("E8")

            rook_short = Position("H8")
            rook_long  = Position("A8")

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

            if not isinstance(self.loc_map[rook], Rook):
                continue

            path = self.piece_map[king].path_to(rook)
            path = [i for i in path if i != self.piece_map[king]]
            if [i for i in path if i in self.loc_map]:
                continue

            enemy_moves = self.__psuedolegal_moves(self.opposing)
            if [i for i in path if i in enemy_moves.all_valid + enemy_moves.all_attack]:
                continue


            final = [king_start.i, king_start.j]
            if rook.j == 0:
                final[1] = final[1] - 2
            else:
                final[1] = final[1] + 2

            final = (final[0], final[1])
                
            valid.append(Position(final))

        return valid

    def move(self, mov: Move) -> bool:
        """Runs a move in the current state. Takes a `Move` object.
        This method does NOT implement full validity checks. Raises `InvalidStateChange` exception.

        :param self:
        :param mov:
        :type mov: Move
        """

        if mov.start not in self.loc_map:
            print("Start is not a piece")
            return False

        # Set the new position
        moving_piece = self.loc_map[mov.start]
        self.__update_piece(moving_piece, new_position=mov.end)

        # Check if the move is a castle
        if mov.is_castle:
            # Validate if the castle is allowed
            rook_i = mov.start.i
            # Set long or short castle
            if mov.is_castle == "short":
                rook_j = 7
                rook_end_j = 5
            elif mov.is_castle == "long":
                rook_j = 0
                rook_end_j = 3
            else:
                raise Exception()
            rook = self.loc_map[Position((rook_i, rook_j))]
            rook_end = Position((rook_i, rook_end_j))
            self.__update_piece(rook, rook_end)
            if self._to_move:
                self._castle[0] = False
                self._castle[1] = False
            else:
                self._castle[2] = False
                self._castle[3] = False

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

        can_castle = "".join(can_castle)
        if not can_castle: can_castle = "-"

        # Since i am not ready to finish FEN we will add default data to the end
        fields.append(can_castle) # Right to castle
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
        return self.__loc_map
    
    @property
    def piece_map(self) -> Dict[Piece, Position]:
        return self.__piece_map

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
        return self._allowed_moves

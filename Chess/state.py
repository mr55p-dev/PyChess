from itertools import chain, repeat
from typing import Dict, Tuple, List, Optional
from Chess.constants import BLACK, RANKS, WHITE
from Chess.pieces import King, Piece
from Chess.coordinate import Position
from Chess.exceptions import InvalidFormat
from Chess.helpers import new_game

class Board():
    """Contains a state of the board"""
    """
	Representation for the game.
	Stores the "active" and "inactive" (captured) pieces,
	the valid continuations (only moves which will not put the king in check)
	and the next piece to move.

	:param white_active:	[ChessPiece]
	:param black_active:	[ChessPiece]
							List of the active pieces for each side
	:attr to_move: 			White|Black
	:attr is_check: 		bool
	:attr is_mate: 			bool
	:attr evaluation: 		int
							The material evaluation (difference in value between active pieces)
	:method calc_moves: 	ChessMove
							All the valid moves for each piece
	:method do_move
		:param move_from: 	Piece starting position
		:param move_to: 	Piece ending position
		:returns: 			ChessBoard
	:method best_move: 		ChessMove
							The best continuting move (based on pieces which can be captured).

    """
    BLOCKED         = 0
    CAPTURE         = 1
    EMPTY           = 2
    CHECKING_ATTACK = 3
    gametype = Tuple[List[Optional[Piece]], List[Optional[Piece]]]

    def __init__(self,
                 starting_position: gametype=new_game(),
                 turn: int = 0,
                 to_move: int = WHITE,
                 other_fen_params = []) -> None:
        """__init__.

        :param starting_position:
        :param to_move:
        :type to_move: int
        :rtype: None
        """
        self._white, self._black = starting_position
        self._turn = turn
        self._loc_map = { piece.position: piece for piece in self._white + self._black }

        self._to_move = to_move
        self._opposition = WHITE if to_move == BLACK else BLACK

        self._is_check = None
        self._is_mate = None
        self._evaluation = None

        self._valid_moves = None

        self.other_FEN_params = other_fen_params
        self._evaluated = False 


    def __hash__(self) -> int:
        return hash(self.to_fen())

    def __repr__(self) -> str:
        """__repr__.  """

        board = [[" " for _ in range(8)] for _ in range(8)]
        for loc, piece in self._loc_map.items():
            board[loc.i][loc.j] = piece.kind  # type: ignore
        return "\n".join([" ".join([cell for cell in row]) for row in board])

    def __allowed_move(self, position, piece):
        """Calculate if the position is occupied, and if so if the move is blocked by a friendly piece or an enemy piece
        Returns self.EMPTY if a move is allowed
        Returns self.BLOCKED if a move is blocked by an allied piece
        returns self.CHECKING_ATTACK if a move is a check
        Returns self.CAPTURE if a move is a capture"""
        if position in self._loc_map.keys():
            occupied_by = self._loc_map[position]
            if occupied_by.colour == piece.colour: return self.BLOCKED
            else:
                if isinstance(occupied_by, King): return self.CHECKING_ATTACK
                else: return self.CAPTURE
        else: return self.EMPTY

    def __find_moves(self, piece) -> Dict[str, List[Piece]]:
        """__find_moves.
        :param self:
        :param piece:
        :rtype: Dict[str, List[Piece]]

        Internal method to find moves.
        Returns a dict with keys:
            - passive   -> the passive moves for that piece
            - captures  -> the captures this piece can make
            - defending -> the allied pieces this is defending
            - check    -> the location of a check this piece is delivering
            - pin      -> the location of a pin this piece is exerting
        """

        results = {}
        results["passive"] = []
        results["captures"] = []
        results["defending"] = []

        results["check"] = None
        results["pin"] = None
        for dir in piece.projections:
            # Iterate over all the directions a piece can move in
            pinned = None
            for step in range(1, piece.distance + 1):
                # Count up all the steps the piece can take until it meets
                # a stop condition; capturing or moving onto an allied piece.
                """Make invalid moves just set a flag on position,
                rather than raising an exception?"""
                """if not landed_on.allowed: break"""
                try: landed_on = piece.position + (dir * step)
                except InvalidFormat: break

                if (allowed:=self.__allowed_move(landed_on, piece)) == self.EMPTY:
                    # Store empty squares if we are not looking for a pin
                    if pinned == None: results["passive"].append(landed_on)
                elif allowed == self.CAPTURE:
                    # Store a capture if we are not looking for a pin
                    if pinned == None: results["captures"].append(landed_on); pinned = landed_on
                    # Stop looking for a pin if we encounter a piece that isnt the king
                    else: break
                elif allowed == self.CHECKING_ATTACK:
                    # Store a check if we are not looking for a pin
                    if pinned == None: results["check"] = landed_on; break
                    # Store a pin if we found one
                    else: results["pin"] = pinned; break
                elif allowed == self.BLOCKED:
                    # Store a piece as defended if we are not looking for a pin
                    if pinned == None: results["defending"].append(landed_on)
                    # Stop looking if there is another piece before the king
                    else: break

        return results

    def _get_moving(self) -> List[Piece]:
        return self._white if self._to_move == WHITE else self._black  # type: ignore

    def _get_opposing(self) -> List[Piece]:
        return self._black if self._to_move == WHITE else self._white  # type: ignore

    def _get_king(self) -> King:
        return [i for i in self._get_moving() if isinstance(i, King)].pop()

    def _filter_moves(self, moves, by):
        valid_moves = {}
        # valid_moves = {type: [move for move in move_list if move in by] for type, move_list in moves.items()}
        for type, move_list in moves.items():
            if not isinstance(move_list, list): pass
            valid_moves[type] = [move for move in move_list if move in by]
        return valid_moves

    def _evaluate_check(self) -> List[Optional[Piece]]:
        """_evaluate_check."""
        moves = self.get_moves_set(self._get_opposing())
        king = self._get_king()

        # Extract all the attacks from the move
        attacks = {piece: move_list["attacks"] for piece, move_list in moves}

        # Return a list of all the pieces which have the king as a valid attack
        return [piece for piece, attack_list in attacks.items() if king.position in attack_list]

    def _evaluate_mate(self):
        """_evaluate_mate."""
        if not (attackers := self.is_check):
            return False
        # I am working on calculating valid moves in here as well, so it will need refactoring
        # into the move validation functions
        
        # attackers
        """
        Now I need to evaluate if a piece is pinned.
        We can do this by modifying our original __find_moves function to add a key for pinning_king
        """
        king = self._get_king()
        all_moves = self.get_moves_set(self._get_moving())

        # Create a list of tuples of a piece exerting a pin pins[0] on 
        # some other position pins[1]
        pins = [(piece, results["pin"]) for piece, results in all_moves if results["pin"]]
        pinned_pieces = [self._loc_map[pinned] for _, pinned in pins] 
        other_pieces = [piece for piece in self._get_moving() if piece not in pinned_pieces]
        
        filter = lambda moves, by: list(map(self._filter_moves, moves, repeat(by)))

        # CASE: IS NOT CHECK: ATTACKERS == None
        
        # Look over each pinner, pinned piece
        for pinner, pinned_loc in pins:
            # Loop up the piece identifier for the pinned piece
            # Calculate the path of squares between the pinning 
            # piece and the king
            pinned = self._loc_map[pinned_loc]
            path = pinner.position - king.position

            # For each move type, filter the moves to be only those on the path
            all_moves[pinned] = {type: filter(moves, path) for type, moves in all_moves[pinned].items()}

        # CASE: IS CHECK: ATTACKERS == 1

        # The same logic applies for pinned pieces as always, however now we have
        # some additional constraints to apply on the pieces which are not pinned.
        # In this case where len(attackers) == 1 there is the possibility for
        # other pieces to block the checkon squares between the attacker and the
        # king. These may hang the piece but they are still legal moves
        # Such is the case with backrank mate, where multiple pieces can come
        # in to defend the king as a legal defense before checkmate can be achieved.
        # In this circumstance, we need to know the path from the attacker to the king
        # and then do the same move-filtering process as before

        if len(attackers) == 1:
            path = attackers[0].position - king.position
            for piece in other_pieces: 
                all_moves[piece] = {type: filter(moves, path) for type, moves in all_moves[piece].items()}




        # Calculate the squares which surround the king
        captures, passives = self._find_piece_moves(king)

        opposing_pieces = [i for i in self._get_opposing() if not isinstance(i, King)]

        passives = list(map(self._square_is_defended, passives, repeat(opposing_pieces)))
        captures = list(map(self._square_is_defended, captures, repeat(opposing_pieces)))
        
        # There must be a better way of doing this...
        # Instead, we could mark pieces as pinned to the king, meaning they cannot be moved.
        # This is the first pass when looking at the board.
        # Then, when we calculate all the moves on the board we only iterate over pieces that
        # are not pinned, or moves by the pinned piece which capture the attacking piece.
        # The logic would look like:
        """
        Board instantiated
        Find all the pieces that attack the king (isCheck)
            if none: pass
            if > 0:
                Create a list of all the opposing attackers
                Create a list of pinned allied pieces
                Find all the moves for !pinned pieces which can block the check
                Find all the moves for  pinned pieces which result in attackers = []
                    This can work by instantiating a new board and then performing the same
                    evaluation step
                    So say attackers [R, R] and pinned [N], check = True
                    We call Board(new_state), and then in that board we will have 
                    pinned = [N], check = False so we allow this move
                    The only states for which this will be valid is those which are the capture
                    of one of the pinning pieces, so we only have to evauate the captures for 
                    pinned = [N] in the first layer
                Only allow moves for the pinned pieces which resolve the check.
                Evaluate the moves for the king by:
                    Create a list of all passive or capturing moves for the king
                    For the passive moves, check if that square is attacked by an enemy piece
                    For the capturing moves, check if that piece is defended by another piece
                        This could instead work by
                        For each king move:
                            Evaluate if the position is in check
        """
        return passives

        
    def _square_is_defended(self, position: Position, pieces=None):
        # using pieces from get_opposition()
        # return if the square appears in their passive move list
        if not pieces:
            pieces = self._get_opposing()

        moves = self._find_all_moves(self._get_opposing()).values()
        passive_moves = [i[1] for i in moves]
        defended_positions = list(map(self._find_piece_moves, self._get_opposing(), repeat(True)))
        
        passive = list(chain.from_iterable(passive_moves))
        defended = list(chain.from_iterable(defended_positions))

        if position in passive:
            return True
        elif position in defended:
            return True
        return False

    def _evaluate_score(self):
        """_evaluate_score."""
        pass

    def update(self):
        if not (changed := self.__hash__() == self._evaluated):
            # In here we calculate all the evaluations for the position:
            # is_check
            # is_mate
            # is_stalemate
            # is_halfmove_timeout
            # is_resigned
            # valid_moves
            # We only need to do this more than once if the position has been changed by some outside
            # force, and since it is computationally expensive its easier to just check the hash.
            # We can also use the hash as a caching mechanism when doing analysis
            pass
        return changed

    def get_moves(self, piece):
        return self.__find_moves(piece)

    def get_moves_set(self, pieces):
        move_list = map(self.__find_moves, pieces)
        return {piece: moves for piece, moves in zip(pieces, move_list)}

    @property 
    def turn(self) -> int:
        return self._turn

    @property
    def map(self) -> dict:
        """Convenience attribute
        Returns a hash map of each occupied position and its associated piece"""
        return self._loc_map

    @property
    def pieces(self) -> list:
        return self._black + self._white

    @property
    def is_check(self) -> Optional[List[Piece]]:
        return self._evaluate_check()

    @property
    def is_mate(self) -> bool:
        return self._evaluate_mate()  # type: ignore
    
    @property
    def to_move(self):
        """to_move."""
        return self._to_move

    def to_fen(self):
        fields = []
        ranks = [["" for i in range(8)] for _ in range(8)]
        # The rank of a piece will be calculated as 7 - i; 
        # In FEN the 8th rank (list index 7) is at i=0
        for position, piece in self.map.items():
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
        
        # Since i am not ready to finish FEN we will add default data to the end
        other_p = [str(i) for i in self.other_FEN_params]
        fields.append(other_p[0])
        fields.append(other_p[1])
        fields.append(other_p[2])
        # fields.append("KQkq")
        # fields.append("-")
        # fields.append("0")
        fields.append(self._turn)
        return " ".join(fields)

            
class Game():
    """
	1. Initialise a new game based on the starting board
	2. Calculate the legal continuations
	3. Monitor for stalemate, checkmate, etc
	4. Monitor for the right to castle, double pawn push
		

	:param starting_board: 	ChessBoard
	:attr full_game: 		[ChessBoard]
	:attr current: 			ChessBoard
	:attr turn: 			int > 0
    """

    pass


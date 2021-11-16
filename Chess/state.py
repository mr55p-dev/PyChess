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
    BLOCKED  = 0
    CAPTURE = 1
    EMPTY    = 2
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
        self._update_map()

        self._to_move = to_move
        self._opposition = WHITE if to_move == BLACK else BLACK

        self._is_check = self._evaluate_check()
        self._is_mate = self._evaluate_mate()
        self._evaluation = self._evaluate_score()



        self.other_FEN_params = other_fen_params


    def __repr__(self) -> str:
        """__repr__.

        :rtype: str
        """
        # Maybe write a board class which is accessable on rows and columns for ease.
        board = [[" " for _ in range(8)] for _ in range(8)]
        for loc, piece in self._loc_map.items():
            board[loc.i][ loc.j] = piece.kind
        return "\n".join([" ".join([cell for cell in row]) for row in board])

    def _get_moving(self) -> List[Piece]:
        return self._white if self._to_move == WHITE else self._black  # type: ignore

    def _get_opposing(self) -> List[Piece]:
        return self._black if self._to_move == WHITE else self._white  # type: ignore

    def _update_map(self) -> None:
        """Generates a hashmap of position: piece
        Might be able to bring it inside __init__ since state should
        only update through creating a new instance based on a Move
        object."""
        self._loc_map = { piece.position: piece for piece in self._white + self._black }

    def _find_all_moves(self, pieces=None):
        """_find_all_moves.
        Returns a dict of piece locations, then two lists of passive and capture moves"""
        if not pieces:
            pieces = self._get_moving()

        move_list = map(self._find_piece_moves, pieces)
        return {piece: moves for piece, moves in zip(pieces, move_list)}

    def _allowed_move(self, position, piece):
        """Calculate if the position is occupied, and if so if the move is blocked by a friendly piece or an enemy piece
        Returns self.EMPTY   if a move is allowed
        Returns self.BLOCKED if a move is blocked by an allied piece
        Returns self.CAPTURE if a move is a capture"""
        # if position in [i.position for i in self._get_moving()]:
        #     return self.BLOCKED
        # elif position in [i.position for i in self._get_opposing()]:
        #     return self.CAPTURE
        # return self.EMPTY

        if position in self._loc_map.keys():
            occupied_by = self._loc_map[position]
            if occupied_by.colour == piece.colour:
                return self.BLOCKED
            else:
                return self.CAPTURE
        else:
            return self.EMPTY

    def _find_piece_moves(self, piece, defending=False) -> Tuple[list[Position], list[Position]]:
        """Finds all the valid moves for a piece
        returns a tuple of captured and passive moves"""
        captures = []
        passive = []
        defended = []

        """ Rewrite as a map """

        for dir in piece.projections:
            # Iterate over all the directions a piece can move in
            for step in range(1, piece.distance + 1):
                # Count up all the steps the piece can take until it meets
                # a stop condition; capturing or moving onto an allied piece.
                """Make invalid moves just set a flag on position,
                rather than raising an exception?"""
                """if not landed_on.allowed: break"""
                try:
                    landed_on = piece.position + (dir * step)
                except InvalidFormat:
                    break

                if (allowed:=self._allowed_move(landed_on, piece)) == self.EMPTY:
                    passive.append(landed_on)
                elif allowed == self.CAPTURE:
                    # Add the possible capture to the captures map
                    captures.append(landed_on)
                    break
                elif allowed == self.BLOCKED:
                    defended.append(landed_on)
                    break
        if defending:
            return defended
        return captures, passive

    def _get_king(self) -> King:
       return [i for i in self._get_moving() if isinstance(i, King)].pop()

    def _evaluate_check(self):
        """_evaluate_check."""
        moves = self._find_all_moves(self._opposition)
        king = self._get_king()

        # Extract all the attacks from the move
        attacks = [attack for attack, _ in moves.values()]
        attacks = list(chain.from_iterable(attacks))

        if king.position in attacks:
            return True
        else:
            return False

    def _evaluate_mate(self):
        """_evaluate_mate."""
        if not self.is_check:
            return False
        
        # Calculate the squares which surround the king
        king = self._get_king()
        captures, passives = self._find_piece_moves(king)

        # For the passive moves, we need to check if those squares are attacked by the enemy pieces
        # For the capture moves, we need to check if that piece is defended by another enemy piece
        # In both cases, we can check if the square is defended by the enemy pieces
        # We need to evaluate if a square is defended as if the king is not there.
        opposing_pieces = [i for i in self._get_opposing() if not isinstance(i, King)]

        passives = list(map(self._square_is_defended, passives, repeat(opposing_pieces)))
        captures = list(map(self._square_is_defended, captures, repeat(opposing_pieces)))
        # If there are no passive moves, then we need to check if any piece can block?
        # We need all the positions between the attacker and the king
        # King.pos - Attacker.pos (there may be more than one attacker too)
        # attackers = [i for p, m in fetch_all_moves() if king.pos in m[1]]
        # We also need to evaluate if that move then results in a check.
        
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
    def is_check(self) -> bool:
        return self._is_check
    
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


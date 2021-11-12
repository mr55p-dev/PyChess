from typing import Tuple, List, Optional
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
        self._moved = WHITE if to_move == BLACK else WHITE
        self._moving_pieces = self._white if to_move == WHITE else self._black
        self._moved_pieces = self._black if to_move == WHITE else self._black

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


    def _update_map(self):
        """Generates a hashmap of position: piece
        Might be able to bring it inside __init__ since state should
        only update through creating a new instance based on a Move
        object."""
        self._loc_map = { piece.position: piece for piece in self._white + self._black }

    def _find_all_moves(self, previous=False):
        """_find_all_moves."""
        passive = {}
        captures = {}
        if previous:
            moving = self._moved_pieces
        else:
            moving = self._moving_pieces
        for piece in moving:
            capturing_moves, passive_moves = self._find_piece_moves(piece)
            captures[piece] = capturing_moves
            passive[piece] = passive_moves
        return passive, captures

    def _allowed_move(self, position, piece):
        """Calculate if the position is occupied, and if so if the move is blocked by a friendly piece or an enemy piece
        Returns self.EMPTY   if a move is allowed
        Returns self.BLOCKED if a move is blocked by an allied piece
        Returns self.CAPTURE if a move is a capture"""
        if position in self._loc_map.keys():
            occupied_by = self._loc_map[position]
            if occupied_by.colour == piece.colour:
                return self.BLOCKED
            else:
                return self.CAPTURE
        else:
            return self.EMPTY

    def _find_piece_moves(self, piece) -> Tuple[list[Position], list[Position]]:
        """Finds all the valid moves for a piece
        returns a tuple of captured and passive moves"""
        captures = []
        passive = []
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
                    break
        return captures, passive

    def _get_king(self):
        """Returns the king of the side *not* moving on this turn"""
        king_w, king_b = tuple([i for i in self.pieces if isinstance(i, King)])
        if self._moved == BLACK:
            return king_b
        else:
            return king_w

    def _evaluate_check(self):
        """_evaluate_check."""
        king = self._get_king()
        _, attacks = self._find_all_moves(self._moved)
        if king in attacks:
            return True
        else:
            return False

    def _evaluate_mate(self):
        """_evaluate_mate."""
        pass

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


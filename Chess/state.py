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
    def __init__(self, starting_position=new_game()) -> None:
        self._white, self._black = starting_position
        self._update_map()
        """
        self._to_move
        self._
        """

    def __repr__(self) -> str:
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
        # self._loc_map = {}
        # for piece in self._white + self._black:
        #     self._loc_map[piece.position] = piece
        self._loc_map = {
            piece.position: piece for piece in self._white + self._black
        }

    @property
    def map(self) -> dict:
        """Convenience attribute
        Returns a hash map of each occupied position and its associated piece"""
        return self._loc_map


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


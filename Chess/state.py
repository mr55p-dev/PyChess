from typing import Tuple
from Chess.constants import WHITE
from Chess.coordinate import Position
from Chess.exceptions import InvalidFormat, InvalidStartingPosition
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

 r   """
    BLOCKED  = 0
    CAPTURE = 1
    EMPTY    = 2
    def __init__(self, starting_position=new_game(), to_move: int = WHITE) -> None:
        self._white, self._black = starting_position
        self._update_map()
        self._to_move = to_move
        self._is_check = self._evaluate_check()
        self._is_mate = self._evaluate_mate()
        self._evaluation = self._evaluate_score()

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
        self._loc_map = { piece.position: piece for piece in self._white + self._black }

    def _find_all_moves(self):
        moving_pieces = self._white if self._to_move == WHITE else self._black
        passive = {}
        captures = {}
        for piece in moving_pieces:
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
                    print(f"Allowed move at {landed_on}")
                    passive.append(landed_on)
                elif allowed == self.CAPTURE:
                    # Add the possible capture to the captures map
                    captures.append(landed_on)
                    print(f"Capture at {landed_on}")
                    break
                elif allowed == self.BLOCKED:
                    break
        return captures, passive

    def _evaluate_check(self):
        pass

    def _evaluate_mate(self):
        pass

    def _evaluate_score(self):
        pass

    @property
    def map(self) -> dict:
        """Convenience attribute
        Returns a hash map of each occupied position and its associated piece"""
        return self._loc_map
    
    @property
    def to_move(self):
        return self._to_move


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


from Chess.constants import WHITE, BLACK
from Chess.coordinate import Position, Vec

class Piece:
    """
	:param colour: 			White|Black
	:param type: 			King|Queen|Rook|Bishop|Knight|Pawn
	:param position: 		ChessVec
							A vector containing piece position
    :param kind:            String containing the letter of the piece.
	:method move: 			updates position
	:attr value: 			int
							The value of the piece (based on kind)
    """
    KING = "K"
    QUEEN = "Q"
    ROOK = "R"
    BISHOP = "B"
    KNIGHT = "N"
    PAWN = "P"
    
    def __init__(
            self,
            colour: WHITE|BLACK,
            position: Position,
            kind: str
        ) -> None:
        self._colour = colour
        self._position = position
        self._kind = kind

    def __repr__(self) -> str:
        return self._kind

    def __str__(self) -> str:
        return self._kind

    @property
    def colour(self) -> int:
        return self._colour

    @property
    def position(self) -> Position:
        return self._position

    @property
    def kind(self) -> str:
        return self._kind

    @staticmethod
    def projections():
        """A list of the directions that the piece can move in."""
        pass


class King(Piece):
    pass


class Queen(Piece):
    pass


class Rook(Piece):
    pass


class Bishop(Piece):
    pass


class Knight(Piece):
    pass


class Pawn(Piece):
    pass

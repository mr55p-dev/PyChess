from itertools import product
from Chess.constants import PIECE_TYPES, WHITE, BLACK
from Chess.coordinate import Position, Vec
from Chess.exceptions import InvalidPiece

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
            colour: int,
            position: Position,
            kind: str,
            is_active: bool = True
        ) -> None:
        if colour not in [WHITE, BLACK]: raise InvalidPiece("Not a valid colour")
        if kind not in PIECE_TYPES: raise InvalidPiece("Not a valid type")
        if not isinstance(is_active, bool): raise InvalidPiece("is_active must be bool")

        self._colour = colour
        self._position = position
        self._kind = kind
        self._is_active = is_active

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

    @property
    def active(self) -> bool:
        return self._is_active

    @active.setter
    def active(self, state: bool) -> None:
        assert isinstance(state, bool)
        self._is_active = state

    def capture(self) -> None:
        """Mark the piece as captured"""
        self._is_active = False

    @staticmethod
    def projections():
        """A list of the directions that the piece can move in."""
        pass

    @staticmethod
    def max_distance():
        """The maximum distance a piece can move"""
        pass

    @staticmethod
    def special_moves():
        """The special moves a piece can participate in, if they are still valid
        i.e castling for a king, en-passant,..."""


class King(Piece):
    def __init__(self, colour: int, position: Position) -> None:
        super().__init__(colour, position, kind="K")

    @property
    def projections(self):
        """The directions this piece can move in"""
        return [
            Vec(1, 1),
            Vec(1, 0),
            Vec(1, -1),
            Vec(0, 1),
            Vec(0, -1),
            Vec(-1, 1),
            Vec(-1, 0),
            Vec(-1, -1)
        ]



class Queen(Piece):
    def __init__(self, colour: int, position: Position) -> None:
        super().__init__(colour, position, kind="Q")

    @property
    def projections(self):
        """The directions this piece can move in"""
        return [
            Vec(1, 1),
            Vec(1, 0),
            Vec(1, -1),
            Vec(0, 1),
            Vec(0, -1),
            Vec(-1, 1),
            Vec(-1, 0),
            Vec(-1, -1)
        ]

class Rook(Piece):
    def __init__(self, colour: int, position: Position) -> None:
        super().__init__(colour, position, kind="R")

    @property
    def projections(self):
        """The directions this piece can move in"""
        return [
            Vec(1, 0),
            Vec(0, 1),
            Vec(0, -1),
            Vec(-1, 0),
        ]

class Bishop(Piece):
    def __init__(self, colour: int, position: Position) -> None:
        super().__init__(colour, position, kind="B")

    @property
    def projections(self):
        """The directions this piece can move in"""
        return [
            Vec(1, 1),
            Vec(1, -1),
            Vec(-1, 1),
            Vec(-1, -1)
        ]

class Knight(Piece):
    def __init__(self, colour: int, position: Position) -> None:
        super().__init__(colour, position, kind="N")

    @property
    def projections(self):
        """The directions this piece can move in"""
        return [
            Vec(1, 2),
            Vec(1, -2),
            Vec(2, 1),
            Vec(2, -1),
            Vec(-1, 2),
            Vec(-1, -2),
            Vec(2, 1),
            Vec(2, -1),
        ]

class Pawn(Piece):
    def __init__(self, colour: int, position: Position) -> None:
        super().__init__(colour, position, kind="P")

    @property
    def projections(self):
        """The directions this piece can move in"""
        if self._kind == WHITE:
            return [
                Vec(1, 0),
                Vec(2, 0),
                Vec(1, -1),
                Vec(1, 1),
            ]
        else:
            return [
                Vec(-1, 0),
                Vec(-2, 0),
                Vec(-1, -1),
                Vec(-1, 1),
            ]

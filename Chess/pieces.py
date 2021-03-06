"""I, Ellis Lunnon, have read and understood the School's Academic Integrity Policy, as well as guidance relating to this
module, and confirm that this submission complies with the policy. The content of this file is my own original work,
with any significant material copied or adapted from other sources clearly indicated and attributed."""

from typing import List
from Chess.constants import PIECE_TYPES, WHITE, BLACK, USE_CPP
from Chess.coordinate import Vec
from Chess.exceptions import InvalidPiece

try:
    from libpychess import Position
except ImportError:
    from Chess.coordinate import Position

class Piece:
    """Piece
    Wrapper for a chess piece. This is the base class, and is subclassed and overloaded
    for each type of piece to make construction a bit more smooth.
    Stores the projections, position, colour, move distance and activity of the piece.
    """

    KING = "K"
    QUEEN = "Q"
    ROOK = "R"
    BISHOP = "B"
    KNIGHT = "N"
    PAWN = "P"
    
    def __init__(
            self,
            colour: bool,
            position: Position,
            kind: str,
            max_distance: int = 7,
            is_active: bool = True
        ) -> None:
        """__init__.

        :param colour: Piece colour
        :type colour: bool
        :param position: Piece position
        :type position: Position
        :param kind: Piece kind 
        :type kind: str (K|Q|R|B|N|P)
        :param max_distance: The furthest this piece can move
        :type max_distance: int
        :param is_active: If the piece should be considered in calculation
        :type is_active: bool
        :rtype: None
        """
        if colour not in [WHITE, BLACK]: raise InvalidPiece("Not a valid colour")
        if kind not in PIECE_TYPES: raise InvalidPiece("Not a valid type")
        if max_distance not in range(1, 8): raise InvalidPiece("max_distance must be between 0, 8")
        if not isinstance(is_active, bool): raise InvalidPiece("is_active must be bool")

        self._colour = colour
        self._position = position
        self._kind = kind
        self._is_active = is_active
        self._max_distance = max_distance

    def __repr__(self) -> str:
        return f"<{self._kind} colour {self._colour} at {self._position}>"

    def __str__(self) -> str:
        return f"<{self._kind} colour {self._colour} at {self._position}>"

    def __eq__(self, other: 'Piece') -> bool:
        return self.__hash__() == hash(other)

    def __neq__(self, other: 'Piece') -> bool:
        return self.__hash__() != hash(other)

    def __hash__(self) -> int:
        """__hash__.
        15 bit integer hash mapped as follows:
            000(i)000(j)0000000(char)0(active)0(colour)
        :rtype: int
        """
        return 0 | (self._position.i<<12) | (self._position.j<<9) | (ord(self.kind)<<2) | (self._is_active<<1) | (self._colour)

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

    @property
    def distance(self) -> int:
        """The maximum distance a piece can move"""
        return self._max_distance

    @property
    def is_active(self) ->  bool:
        return self._is_active

    @is_active.setter
    def is_active(self, state) -> None:
        self._is_active = state

    def capture(self) -> None:
        """Mark the piece as captured"""
        self._is_active = False

    @property
    def projections(self) -> List[Vec]:
        """A list of the directions that the piece can move in."""
        return [Vec(1,1)]


class King(Piece):
    def __init__(self, colour: bool, position: Position) -> None:
        super().__init__(colour, position, kind="K", max_distance=1)

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
    def __init__(self, colour: bool, position: Position) -> None:
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
    def __init__(self, colour: bool, position: Position) -> None:
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
    def __init__(self, colour: bool, position: Position) -> None:
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
    def __init__(self, colour: bool, position: Position) -> None:
        super().__init__(colour, position, kind="N", max_distance=1)

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
            Vec(-2, 1),
            Vec(-2, -1),
        ]

class Pawn(Piece):
    def __init__(self, colour: bool, position: Position) -> None:
        super().__init__(colour, position, kind="P", max_distance=2)

    @property
    def projections(self):
        """The directions this piece can move in"""
        if self._colour == WHITE:
            return [
                Vec(1, 0),
                Vec(1, -1),
                Vec(1, 1),
            ]
        else:
            return [
                Vec(-1, 0),
                Vec(-1, -1),
                Vec(-1, 1),
            ]

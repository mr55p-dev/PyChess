from typing import List
from Chess.constants import PIECE_TYPES, WHITE, BLACK
from Chess.coordinate import Vec
from Chess.exceptions import InvalidPiece
from Chess import types

class Piece(types.Piece):
    """Piece
    Wrapper for a chess piece. This is the base class, and is subclassed and overloaded
    for each type of piece to make construction a bit more smooth.
    Stores the projections, position, colour, move distance and activity of the piece.
    """
    def __init__(
            self,
            colour: bool,
            position: types.Position,
            kind: str,
            max_distance: int = 7,
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

        self._colour = colour
        self._position = position
        self._kind = kind
        self._is_active = True
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
    def position(self) -> types.Position:
        return self._position

    @property
    def kind(self) -> str:
        return self._kind

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


    @property
    def projections(self) -> List[Vec]:
        """A list of the directions that the piece can move in."""
        return [Vec(1,1)]


class King(Piece):
    def __init__(self, colour: bool, position: types.Position) -> None:
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
    def __init__(self, colour: bool, position: types.Position) -> None:
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
    def __init__(self, colour: bool, position: types.Position) -> None:
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
    def __init__(self, colour: bool, position: types.Position) -> None:
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
    def __init__(self, colour: bool, position: types.Position) -> None:
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
    def __init__(self, colour: bool, position: types.Position) -> None:
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

# Pieces factory can be used like this!
"""

Both C++ API and Python export a common interface;

from libpychess import c_pieces
from Chess import py_pieces

c_pieces.King(c_WHITE, c_Position(1, 1))
py_pieces.King(py_WHITE, py_Position(1, 1))

So as long as the correct instances for WHITE, BLACK and
Position are defined it will work perfectly

class BaseFactory():
    def __init__(self, use_acceleration=False):
        if use_acceleration:
            from libpychess import pieces as Pieces
            from libpychess import black as BLACK, white as WHITE
            from libpychess import Position, Vec
        else:
            from Chess import Pieces
            from Chess.coordinate import Position, Vec
            from Chess.constants import BLACK, WHITE

    def get_colours(self):
        return (WHITE, BLACK)

    def get_pieces(self):
        return Pieces

    def get_position(self):
        return Position

Client < clientFactory < C/P/State
                         PState < BaseFactory(use_acceleration=False)
                         CState < BaseFactory(use_acceleration=True )


"""
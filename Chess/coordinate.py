"""I, Ellis Lunnon, have read and understood the School's Academic Integrity Policy, as well as guidance relating to this
module, and confirm that this submission complies with the policy. The content of this file is my own original work,
with any significant material copied or adapted from other sources clearly indicated and attributed."""

from itertools import repeat
from typing import List, Tuple, Union
import math
import Chess.constants as cons

class Vec:
    """Vec: lightweight vector class implementation
    Used throught the program specifically to manipulate Position objects 
    (a piece's position can be projected along a vector through scalar multiplicaiton).
    This is the Python reference implementation - this class has been reimplemented in C++ 
    to speed up computations by MoveAnalyser.
    """

    __slots__ = ('i', 'j')

    def __init__(self, i: int, j: int) -> None:
        """__init__.

        :param self:
        :param i: Row coordinate
        :type i: int
        :param j: Column coordinate
        :type j: int
        :rtype: None
        """
        self.i: int = i
        self.j: int = j

    def __repr__(self) -> str:
        return str((self.i, self.j))

    def __eq__(self, o) -> bool:
        """__eq__.

        :param self:
        :param o:
        :type o: Position | Vec
        :rtype: bool
        
        Equality checking only supports objects which implement i and j attributes (Vec, Position).
        """
        return self.i == o.i and self.j == o.j

    def __ne__(self, o) -> bool:
        return self.i != o.i or self.j != o.j

    def __add__(self, o) -> 'Vec':
        """__add__.

        :param self:
        :param o:
        :type o: Position | Vec
        :rtype: 'Vec'
        """
        return Vec(self.i + o.i, self.j + o.j)

    def __sub__(self, o) -> 'Vec':
        return Vec(self.i - o.i, self.j - o.j)

    def __mul__(self, scalar: int) -> 'Vec':
        """__mul__

        :param self:
        :param scalar:
        :type scalar: int
        :rtype: 'Vec'

        Only scalar multiplication is supported for speed.
        """
        return Vec(self.i * scalar, self.j * scalar)

class Position:
    """Position
    Wrapper for a board position. Also implemeted in C++ for speed.
    Uses __slots__ for preallocation of attributes so does not support
    dynamic assignment. 
    
    This is mainly designed to make handling chess positions more simple -
    locations can be defined using the algebraic (A-H)(1-8) notation which is much
    more intuitive. Coordinates are represented internally by (0-7)(0-7) still.
    Invalid positions may be instantiated however self.is_valid can be used to check
    them.
    """
    __slots__ = ('i', 'j')

    _TYPE_ALG = str
    _TYPE_CAR = Tuple[int, int]
    _TYPE_INI = Union[str, Tuple[int, int]]

    def __init__(self, pos: _TYPE_INI) -> None:
        """__init__.

        :param self:
        :param pos: 
        :type pos: (int, int) | str[2]
        :rtype: None
        """
        if isinstance(pos, str):
            self._from_algebraic(pos)
        else:
            self._from_grid(pos)

    def _from_algebraic(self, pos: _TYPE_ALG) -> None:
        # file 0  A   65
        #      1  B   66
        #      2  C   67
        #      ...
        #      7  H   72
        self.i = int(pos[1]) - 1
        self.j = ord(pos[0]) - 65 # Using ASCII character codes to revert capital letters back to numbers.

    def _from_grid(self, pos: _TYPE_CAR) -> None:
        """Load in rows and columns from a tuple"""
        self.i = pos[0]
        self.j = pos[1]

    def is_valid(self) -> bool:
        """is_valid.

        :param self:
        :rtype: bool

        Validate that the current position is on the board
        """
        if self.i > 7 or self.i < 0 or self.j > 7 or self.j < 0:
            return False
        return True

    def __repr__(self) -> str:
        """Reproduce the vector in algebraic notation"""
        return self.algebraic

    def __eq__(self, o) -> bool:
        """Support testing equality between two instances of this class"""
        # if isinstance(o, Position): return self.algebraic == o.algebraic
        # Optimisation for the purpose of data generation - might remove since calling__hash__ 
        # directly feels almost wrong...
        return self.__hash__() == o.__hash__()

    def __ne__(self, o: 'Position') -> bool:
        """Support testing equality between two instances of this class"""
        assert isinstance(o, Position)
        return self.algebraic != o.algebraic
    
    def __add__(self, o: Vec) -> 'Position':
        """Support addition by a vector Vec"""
        return Position((self.i + o.i, self.j + o.j))

    def __sub__(self, o: Union[Vec, 'Position']) -> 'Position':
        """Support subtraction by a vector Vec"""
        return Position((self.i - o.i, self.j - o.j))

    def path_to(self, to: 'Position') -> List['Position']:
        """path_to.
        A.path_to(B) returns a list of positions from A (inclusive) to B (exclusive).
        Gives all positions diagonally, vertically or horizontally, and if a non-linear
        path is requested the value [A] is returned.

        :param self:
        :param to:
        :type to: Position
        :rtype: List[Position]
        """
        sign = lambda x: int(math.copysign(1, x))
        di = to.i - self.i
        dj = to.j - self.j
        ri = range(self.i, to.i, sign(di))
        rj = range(self.j, to.j, sign(dj))
        # If there is a straight or diagonal path between the pieces then give that
        if len(ri) == len(rj):
            return [Position((i, j)) for i, j in zip(ri, rj)]
        elif len(ri) == 0:
            return [Position((i, j)) for i, j in zip(repeat(self.i), rj)]
        elif len(rj) == 0:
            return [Position((i, j)) for i, j in zip(ri, repeat(self.j))]
        # Else just give the original location (used for the path of knights)
        else: return [Position((self.i, self.j))]

    def __hash__(self) -> int:
        """__hash__.
        Returns a 6-bit integer (iiijjj) uniquely ideitifying each position on the board.

        :param self:
        :rtype: int
        """
        return 0 | (self.i<<3) | self.j

    @property
    def algebraic(self) -> str:
        """algebraic.

        Returns the algebraic representation of the position ([A-H][1-8])
        :param self:
        :rtype: str
        """
        return f"{chr(self.j + 65)}{chr(self.i + 49)}"



class Move():
    """Move wrapper class.
    Simple class to wrap properties required to execute a move and define an API for
    view functions to use to interact with Board and Game."""
    __slots__ = ('__start', '__end', '__takes', '__is_castle')

    def __init__(self, 
                 start: Position, 
                 end: Position, 
                 takes: bool,
                 castle: str = ''                
                 ):
        """Move

        :param self:
        :param start: The start position of the piece moving
        :type start: Position
        :param end: The end position of the piece moving
        :type end: Position
        :param takes: If the move is a capture (required)
        :type takes: bool
        :param castle: If the move is castling (optional, default False)
        :type castle: str
        """
        self.__start = start
        self.__end = end
        self.__takes = takes
        self.__is_castle = castle

    @property
    def start(self) -> Position:
        return self.__start

    @property
    def end(self) -> Position:
        return self.__end

    @property
    def takes(self) -> bool:
        return self.__takes

    @property
    def is_castle(self) -> str:
        return self.__is_castle

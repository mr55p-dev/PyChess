from itertools import repeat
from pickle import HIGHEST_PROTOCOL
from typing import List, Tuple, Union
import math
import Chess.constants as cons
from Chess.exceptions import InvalidFormat, InvalidVector


class Vec:
    __slots__ = ('i', 'j')

    def __init__(self, i: int, j: int) -> None:
        self.i: int = i
        self.j: int = j

    def __repr__(self) -> str:
        return str((self.i, self.j))

    def __eq__(self, o) -> bool:
        return self.i == o.i and self.j == o.j

    def __ne__(self, o) -> bool:
        return self.i != o.i and self.j != o.j

    def __add__(self, o) -> 'Vec':
        return Vec(self.i + o.i, self.j + o.j)

    def __sub__(self, o) -> 'Vec':
        return Vec(self.i - o.i, self.j - o.j)

    def __mul__(self, scalar) -> 'Vec':
        return Vec(self.i * scalar, self.j * scalar)

#     @property
#     def i(self) -> int:
#         return self.i
# 
#     @property
#     def j(self) -> int:
#         return self.j


class Position:
    """
	Wrapper for the positions on a chess board.
	Can convert to/from algebraic ("A1", "B2"..."H8") notation.

    :param pos str|tuple: Either a string representing
                            algebraic notation, or a set
                            of i and j coordinates as a
                            tuple or list.
	:attr coord: [0-7, 0-7]
	:attr algebraic: "[A-H][0-7]"

    rank and file are internally represented as `i` and `j` to avoid some confusion,
    relating them to matrix notation feels more familiar.
    - consider implementing __slots__
    """

    __slots__ = ('i', 'j')

    _TYPE_ALG = str
    _TYPE_CAR = Tuple[int, int]
    _TYPE_INI = Union[str, Tuple[int, int]]

    def __init__(self, pos: _TYPE_INI) -> None:
        """__init__.

        :param self:
        :param pos str|tuple: Either a string representing
                                algebraic notation, or a set
                                of i and j coordinates as a
                                tuple or list.
        :rtype: None
        """
        if isinstance(pos, str):
            self._from_algebraic(pos)
        else:
            self._from_grid(pos)

        # if self._i not in cons.CART_COORD: print(self._i); raise InvalidFormat
        # if self._j not in cons.CART_COORD: raise InvalidFormat

    def _from_algebraic(self, pos: _TYPE_ALG) -> None:
        if len(pos) != 2: raise InvalidFormat
    
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

    def _validate_position(self) -> bool:
        """Validate that the current position is on the board"""
        if self.i not in cons.CART_COORD: raise InvalidFormat
        if self.j not in cons.CART_COORD: raise InvalidFormat
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

    def path_to(self, o: 'Position') -> List['Position']:
        """path_to. Calculates the squares from this position to another position.
        Given `a.path_to(b)` the position of `a` will be included, but not the position of `b`

        :param self:
        :param o:
        :rtype: List['Position']
        """
        sign = lambda x: int(math.copysign(1, x))
        di = o.i - self.i
        dj = o.j - self.j
        ri = range(self.i, o.i, sign(di))
        rj = range(self.j, o.j, sign(dj))
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
        """Generate a hash of the position
        allows positions to be the key of the _loc_map dict in 
        `Game`"""
        return 10*self.i + self.j

    @property
    def algebraic(self) -> str:
        """algebraic.
        :param self:
        :rtype: str
        """
        return cons.FILES[self.j] + str(self.i + 1)

    @property
    def grid(self) -> Tuple[int, int]:  
        return self.i, self.j 

#     @property
#     def i(self) -> int:
#         return self.i
# 
#     @property
#     def j(self) -> int:
#         return self.j


class Move():
    
    __slots__ = ('__start', '__end', '__takes', '__is_castle')

    def __init__(self, 
                 start: Position, 
                 end: Position, 
                 takes: bool,
                 castle: str = ''                
                 ):
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

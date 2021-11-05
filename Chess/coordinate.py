from typing import ClassVar, Tuple, Union
import Chess.constants as cons
from Chess.exceptions import InvalidFormat, InvalidVector


class Vec:
    VALID_RANGE = range(-8, 9)

    def __init__(self, i: int, j: int) -> None:
        if i not in self.VALID_RANGE: raise InvalidVector
        if j not in self.VALID_RANGE: raise InvalidVector

        self._i: int = i
        self._j: int = j

    def __eq__(self, o) -> bool:
        return self._i == o.i and self._j == o.j

    def __ne__(self, o) -> bool:
        return self._i != o.i and self._j != o.j

    def __add__(self, o):
        return Vec(self._i + o.i, self._j + o.j)

    def __sub__(self, o):
        return Vec(self._i - o.i, self._j - o.j)

    @property
    def i(self) -> int:
        return self._i

    @property
    def j(self) -> int:
        return self._j


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
    def __init__(self, pos: Union[Tuple[int, int], str]) -> None:
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
        elif isinstance(pos, tuple):
            self._from_grid(pos)

        self._validate_position()

    def _from_algebraic(self, pos):
        if len(pos) != 2: raise InvalidFormat
        file = pos[0]
        # convert rank to numeric
        try:
            rank = int(pos[1])
        except ValueError:
            raise InvalidFormat
        rank -= 1
        # convert file to numeric
        try:
            file = cons.REV_FILES[file]
        except KeyError:
            raise InvalidFormat

        self._i = rank
        self._j = file

    def _from_grid(self, pos: Tuple[int, int]):
        """Load in rows and columns from a tuple"""
        self._i = pos[0]
        self._j = pos[1]

    def _validate_position(self):
        """Validate that the current position is on the board"""
        if self._i not in cons.CART_COORD: raise InvalidFormat
        if self._j not in cons.CART_COORD: raise InvalidFormat

    def __repr__(self) -> str:
        """Reproduce the vector in algebraic notation"""
        return self.algebraic

    def __eq__(self, o) -> bool:
        """Support testing equality between two instances of this class"""
        assert isinstance(o, Position)
        return self.algebraic == o.algebraic

    def __ne__(self, o) -> bool:
        """Support testing equality between two instances of this class"""
        assert isinstance(o, Position)
        return self.algebraic != o.algebraic
    
    def __add__(self, o: Vec):
        """Support addition by a vector Vec"""
        return Position((self._i + o.i, self._j + o.j))

    def __sub__(self, o: Vec):
        """Support subtraction by a vector Vec"""
        return Position((self._i - o.i, self._j - o.j))

    def __hash__(self) -> int:
        """Generate a hash of the position
        allows positions to be the key of the _loc_map dict in 
        `Game`"""
        return 10*self._i + self._j

    @property
    def algebraic(self) -> str:
        """algebraic.
        :param self:
        :rtype: str
        """
        return cons.FILES[self._j] + str(self._i + 1)

    @property
    def grid(self) -> (int, int):  # type: ignore
        return self._i, self._j # type: ignore

        
    @property
    def i(self) -> int:
        return self._i

    @property
    def j(self) -> int:
        return self._j



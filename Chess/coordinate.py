from typing import ClassVar
import Chess.constants as cons
from Chess.exceptions import InvalidFormat


class Vec:
    def __init__(self, x: int, y: int) -> None:
        assert x in range(-8, 9)
        assert y in range(-8, 9)

        self.x = x
        self.y = y

    @property
    def x(self) -> int:
        return self.x

    @property
    def y(self) -> int:
        return self.y

    



class Position:
    """
	Wrapper for the positions on a chess board.
	Can convert to/from algebraic ("A1", "B2"..."H8") notation.

	:param rank: 			0-7
	:param file: 			A-H|0-7
	:attr coord: 			[0-7, 0-7]
	:attr algebraic: 		"[A-H][0-7]"
    """
    def __init__(self, rank: int, file) -> None:
        if isinstance(file, str) and isinstance(rank, int):
            # Check if we are being supplied algebraic notation
            self.rank = rank - 1
            try:
                self.file = cons.REV_FILES[file]
            except KeyError:
                raise InvalidFormat
        elif isinstance(file, int) and isinstance(rank, int):
            # Else update the coordinates to Cartesian
            self.rank = rank
            self.file = file
        else:
            raise InvalidFormat

        # Validate that the position is in the bord bounds.
        try:
            assert self.rank in cons.CART_COORD
            assert self.file in cons.CART_COORD
        except AssertionError:
            raise InvalidFormat

    def __repr__(self) -> str:
        """Reproduce the vector in algebraic notation"""
        return self.algebraic

    def __eq__(self, o: Position) -> bool:
        assert isinstance(o, Position)
        return self.cartesian == o.cartesian

    def __ne__(self, o: Position) -> bool:
        assert isinstance(o, Position)
        return self.cartesian != o.cartesian
    
    def __add__(self, o: Motion) -> Position:
        pass


    @property
    def algebraic(self) -> str:
        rank = str(self.rank + 1)
        file = cons.FILES[self.file]
        return file + rank 

    @property
    def cartesian(self) -> (int, int):  # type: ignore
        """cartesian.

        :param self:
        :rtype: (int, int)
        """
        return self.rank, self.file  # type: ignore

        


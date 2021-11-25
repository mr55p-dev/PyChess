from collections.abc import MutableMapping
import re
from itertools import repeat
from typing import Callable, ClassVar, Dict, List, Optional, Tuple, Union
import math
import Chess.constants as cons
from Chess.exceptions import InvalidFormat, InvalidVector


class Vec:
    VALID_RANGE = range(-8, 9)

    def __init__(self, i: int, j: int) -> None:
        if i not in self.VALID_RANGE: raise InvalidVector
        if j not in self.VALID_RANGE: raise InvalidVector

        self._i: int = i
        self._j: int = j

    def __repr__(self) -> str:
        return str((self._i, self._j))

    def __eq__(self, o) -> bool:
        return self._i == o.i and self._j == o.j

    def __ne__(self, o) -> bool:
        return self._i != o.i and self._j != o.j

    def __add__(self, o):
        return Vec(self._i + o.i, self._j + o.j)

    def __sub__(self, o):
        return Vec(self._i - o.i, self._j - o.j)

    def __mul__(self, scalar):
        return Vec(self._i * scalar, self._j * scalar)

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
        if isinstance(o, Position): return self.algebraic == o.algebraic
        else: return self.__hash__() == o

    def __ne__(self, o) -> bool:
        """Support testing equality between two instances of this class"""
        assert isinstance(o, Position)
        return self.algebraic != o.algebraic
    
    def __add__(self, o: Vec):
        """Support addition by a vector Vec"""
        return Position((self._i + o.i, self._j + o.j))

    def __sub__(self, o: Union[Vec, 'Position']) -> 'Position':
        """Support subtraction by a vector Vec"""
        return Position((self._i - o.i, self._j - o.j))

    def path_to(self, o) -> List['Position']:
        """path_to. Calculates the squares from this position to another position.
        Given `a.path_to(b)` the position of `a` will be included, but not the position of `b`

        :param self:
        :param o:
        :rtype: List['Position']
        """
        sign = lambda x: int(math.copysign(1, x))
        di = o._i - self._i
        dj = o._j - self._j
        ri = range(self._i, o._i, sign(di))
        rj = range(self._j, o._j, sign(dj))
        # If there is a straight or diagonal path between the pieces then give that
        if len(ri) == len(rj): 
            return [Position((i, j)) for i, j in zip(ri, rj)]
        elif len(ri) == 0:
            return [Position((i, j)) for i, j in zip(repeat(self._i), rj)]
        elif len(rj) == 0:
            return [Position((i, j)) for i, j in zip(ri, repeat(self._j))]
        # Else just give the original location (used for the path of knights)
        else: return [Position((self._i, self._j))]

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

class Move():
    def __init__(self, start, to, takes: bool):
        self._from = start
        self._to = to
        self._takes = takes

    # @property
    # def piece(self) -> str:
    #     return self._piece

    @property
    def start(self) -> Position:
        return self._from

    @property
    def end(self) -> Position:
        return self._to

    @property
    def takes(self) -> bool:
        return self._takes


class ResultSet(MutableMapping):
    PROTOTYPE_STORE = {
                "passive": [],
                "captures": [],
                "attacks": [],
                "defending": [],
                "pin": []
            }
    PASSIVE = "passive"
    CAPTURE = "captures"
    ATTACK  = "attacks"
    DEFEND  = "defending"
    PIN     = "pin"
    """Object to store results in

    Default implementation of MutableMapping from https://stackoverflow.com/questions/3387691/how-to-perfectly-override-a-dict"""
    def __init__(self, pieces = [], *args, **kwargs):
        # Setup a default dict of all the pieces being represented.
        self.store = {piece: self.PROTOTYPE_STORE for piece in pieces}
        # Initalise the cached values
        self.all = []
        self.passive = []
        self.capture = []
        self.attacks = []
        self.defended = []
        self.pins = []

    def __getitem__(self, key):
        return self.store[self._keytransform(key)]

    def __setitem__(self, key, value):
        self.store[self._keytransform(key)] = value

    def __delitem__(self, key):
        del self.store[self._keytransform(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def _keytransform(self, key):
        return key

    @property
    def all_valid(self) -> List[Position]:
        """Get all the valid moves for all pieces. Wrapper for passive+capture
        All the moves which can physically be executed on the board."""
        if self.all: return self.all

        # Very basic cachening
        self.all = []
        for _, moves in self.store.items():
            [self.all.append(i) for i in moves[self.PASSIVE]]
            [self.all.append(i) for i in moves[self.CAPTURE]]
        return self.all

    @property
    def all_passive(self):
        """Get all the passive"""
        if self.passive: return self.passive

        self.passive = []
        for _, moves in self.store.items():
            [self.passive.append(i) for i in moves[self.PASSIVE]]
        return self.passive

    @property
    def all_capture(self):
        """Get all the capture"""
        if self.capture: return self.capture

        self.capture = []
        for _, moves in self.store.items():
            [self.passive.append(i) for i in moves[self.CAPTURE]]
        return self.capture

    @property
    def all_attacks(self):
        """Get all the attacks"""
        if self.attacks: return self.attacks

        self.attacks = []
        for _, moves in self.store.items():
            [self.attacks.append(i) for i in moves[self.ATTACK]]
        return self.attacks

    @property
    def all_defended(self):
        """Get all the squares marked as defended"""
        if self.defended: return self.defended

        self.defended = []
        for _, moves in self.store.items():
            [self.defended.append(i) for i in moves[self.DEFEND]]
        return self.defended

    def piece_valid(self, key):
        """Get all the valid moves for a piece"""
        piece_results = self[key]
        passive = piece_results[self.PASSIVE]
        captures = piece_results[self.CAPTURE]
        return passive + captures

    def piece_defending(self, key):
        return self[key][self.DEFEND]

    def by_kind_str(self, key) -> Dict:
        """takes "passive", "attacks", "captures", "defends", "pin" """
        return {piece: moves[key] for piece, moves in self.store.items()}

    def by_types(self, keys):
        return {piece: {key: val for key, val in moves if key in keys} for piece, moves in self.store.items()}

    def lookup_pin(self, loc):
        for piece, moves in self.store.items():
            if moves[self.PIN] == loc:
                return piece
        return None

    @property
    def all_pins(self):
        """Get a dict of pinning: pin_location pieces"""
        if self.pins: return self.pins

        self.pins = []
        for _, moves in self.store.items():
            [self.pins.append(i) for i in moves[self.PIN]]
        return self.pins

        self.pins = []
        for piece, moves in self.store.items():
            if moves["pin"]:
                self.pins[piece] = moves[self.PIN]
        return self.pins

    @property
    def king(self):
        result = ResultSet()
        for p, m in self.store.items():
            if p.kind == 'k':
                result[p] = m

    def clear(self, key):
        self.store[key] = self.PROTOTYPE_STORE

    def clear_all(self):
        for key in self.store.keys():
            self.store[key] = self.PROTOTYPE_STORE

    def filter_all(self, test: Callable) -> None:
        map(self.filter, self.store.keys(), repeat(test))
        for key in self.store:
            self.filter(key, test)

    def filter(self, key, test: Callable) -> None:
        # Performs a filter in place
        # Get the passive and capture values (only legit moves)
        passive = self.store[key][self.PASSIVE]
        capture = self.store[key][self.CAPTURE]

        # Generate a boolean mask of values to keep and discard
        passive_mask = list(map(test, passive))
        capture_mask = list(map(test, capture))

        # Walk through and keep only the values we want
        passive = [i[0] for i in zip(passive, passive_mask) if i[1]]
        capture = [i[0] for i in zip(capture, capture_mask) if i[1]]

    def by_kind_str(self, piece: str):
        return {p: self.store[p] for p in self.store if p.kind == piece)}

"""I, Ellis Lunnon, have read and understood the School's Academic Integrity Policy, as well as guidance relating to this
module, and confirm that this submission complies with the policy. The content of this file is my own original work,
with any significant material copied or adapted from other sources clearly indicated and attributed."""

from collections.abc import MutableMapping
from typing import Any, Callable, Dict, Iterator, List, Optional
from Chess.pieces import King, Piece
from Chess.constants import ResultKeys

try:
    from libpychess import Position
except ImportError:
    from Chess.coordinate import Position


class BaseResult(MutableMapping):
    """BaseResult
    Common class for Result and ResultSet. Defines the store and flatten methods
    """

    __slots__ = ('store')

    @staticmethod
    def flatten(l: List[List[Any]]) -> List[Any]:
        """flatten
        Utility function to flatten [[A, B, C], [D, E]] -> [A, B, C, D, E]

        :param l: List to flatten
        :type l: List[List[Any]]
        :rtype: List[Any]
        """
        return [j for i in l for j in i]


class Result(BaseResult):
    """Result
    Stores the moves of each piece in an internal dict, self.store.
    Defines useful functions to manipulate the result.
    Result stores moves as a dict of lists under the keys defined in ResultKeys, 
    to separate the lists out"""
    __slots__ = ()
    _KT = int
    _VT = List[Position]

    def __init__(self, res: Dict[_KT, _VT] = {}) -> None:
        """__init__
        Default constructor for a Result object.

        :param self:
        :param res: initial value for the store.
        :type res: Dict[_KT, _VT]
        :rtype: None
        """
        # I am aware this isnt hugely pythonic, however
        # Result is constructed over 50k times in some runs,
        # so getting it to be quick is quite important.
        self.store = {
            ResultKeys.passive: [],
            ResultKeys.capture: [],
            ResultKeys.attack:  [],
            ResultKeys.defend:  [],
            ResultKeys.pin:     []
        }
        if res:
            self.store = res

    def __delitem__(self, v: _KT) -> None:
        del self.store[v]

    def __getitem__(self, k: _KT) -> _VT:
        return self.store[k]

    def __setitem__(self, k: _KT, v: _VT) -> None:
        self.store[k] = v

    def __iter__(self) -> Iterator[_KT]:
        return iter(self.store)

    def __len__(self) -> int:
        return len(self.store)

    def filter(self, key: ResultKeys, test: Callable) -> 'Result':
        """filter
        Returns a new result with only values for which `test` returns True.

        :param self:
        :param key: Which result key to filter by
        :type key: ResultKeys
        :param test: Function called with each Position to evaluate keep or delete
        :type test: Callable
        :rtype: 'Result'
        """
        filtered = [i for i in self.store[key] if test(i)]
        res = Result({k: self.store[k] for k in self.store})
        res[key] = filtered
        return res
    
    def filter_valid(self, test: Callable) -> 'Result':
        """filter_valid
        Returns a new result which applies filter to the passive and capture moves.
        These are the moves which can be realised on the board, so it is useful to
        access them directly.

        :param self:
        :param test: Function called with each Position to evaluate keep or delete
        :type test: Callable
        :rtype: 'Result'
        """
        res = Result({k: self.store[k] for k in self.store})
        res[ResultKeys.passive] = [i for i in self.store[ResultKeys.passive] if test(i)]
        res[ResultKeys.capture] = [i for i in self.store[ResultKeys.capture] if test(i)]
        return res

    def filter_all(self, test: Callable) -> 'Result':
        """filter_all
        Applies filter to every key in self.store

        :param self:
        :param test: Function called with each Position to evaluate keep or delete
        :type test: Callable
        :rtype: 'Result'
        """
        res = Result({k: self.store[k] for k in self.store})
        for k in self.store:
            res[k] = [i for i in self.store[k] if test(i)]
        return res

    @property
    def has_moves(self) -> bool:
        """has_moves
        Utility to view if there are any moves listed at all

        :param self:
        :rtype: bool
        """
        for k in self.store:
            if self.store[k]:
                return True
        return False

    @property
    def has_valid(self) -> bool:
        """has_valid.
        Utility to view if there are any realisable moves

        :param self:
        :rtype: bool
        """
        if self.store[ResultKeys.capture] or self.store[ResultKeys.passive]:
            return True
        return False

class ResultSet(BaseResult):
    """ResultSet
    Wrapper of results to store results by the piece which can execute those moves"""

    __slots__ = ()
    _KT = Piece
    _VT = Result

    def __init__(self, mapping: Dict[_KT, _VT] = {}) -> None:
        """__init__.

        :param self:
        :param mapping: Inital value of self.store
        :type mapping: Dict[_KT, _VT]
        :rtype: None
        """
        self.store = mapping

    def __len__(self) -> int:
        return len(self.store)

    def __delitem__(self, v: _KT) -> None:
        del self.store[v]

    def __getitem__(self, k: _KT) -> _VT:
        return self.store[k]

    def __setitem__(self, k: _KT, v: _VT) -> None:
        self.store[k] = v

    def __iter__(self) -> Iterator[_KT]:
        return iter(self.store)

    @property
    def all_valid(self) -> List[Position]:
        """all_valid.
        Flat list of every realisable move.

        :param self:
        :rtype: List[Position]
        """
        result_passive = self.flatten([result[ResultKeys.passive] for result in self.store.values()])
        result_capture = self.flatten([result[ResultKeys.capture] for result in self.store.values()])
        return result_passive + result_capture

    @property
    def all_passive(self) -> List[Position]:
        """all_passive.
        Flat list of every passive move

        :param self:
        :rtype: List[Position]
        """
        return self.flatten([result[ResultKeys.passive] for result in self.store.values()])

    @property
    def all_capture(self) -> List[Position]:
        """all_capture.
        Flat list of every capture move

        :param self:
        :rtype: List[Position]
        """
        return self.flatten([result[ResultKeys.capture] for result in self.store.values()])

    @property
    def all_defend(self) -> List[Position]:
        """all_defend.
        Flat list of every defending move

        :param self:
        :rtype: List[Position]
        """
        return self.flatten([result[ResultKeys.defend] for result in self.store.values()])

    @property
    def all_attack(self) -> List[Position]:
        """all_attack.
        Flat list of every attacking move

        :param self:
        :rtype: List[Position]
        """
        return self.flatten([result[ResultKeys.attack] for result in self.store.values()])

    @property
    def all_pins(self) -> List[Position]:
        """all_pins.
        Flat list of every pin

        :param self:
        :rtype: List[Position]
        """
        return self.flatten([result[ResultKeys.pin] for result in self.store.values()])

    @property
    def king(self) -> Result:
        """king.
        Returns the King stored in this set of moves

        :param self:
        :rtype: Result
        """
        for k in self.store:
            if isinstance(k, King):
                return self.store[k]
        raise IndexError("There is no king in this result set")

    def lookup_pin(self, pin_loc: Position) -> Optional[Piece]:
        """lookup_pin.
        Returns a piece which is exerting a pin to a piece at location `pin_loc`

        :param self:
        :param pin_loc:
        :type pin_loc: Position
        :rtype: Optional[Piece]
        """
        for piece in self.store:
            if pin_loc in self.store[piece][ResultKeys.pin]:
                return piece
        return None

    def filter_by_move_type(self, key: ResultKeys , test: Callable) -> 'ResultSet':
        """filter_by_move_type.
        Calls `Result.filter` for a given key and test, for all pieces stored.

        :param self:
        :param key:
        :type key: ResultKeys
        :param test:
        :type test: Callable
        :rtype: 'ResultSet'
        """
        return ResultSet({k: self.store[k].filter(key, test) for k in self.store})

    def filter_all_by_value(self, test: Callable) -> 'ResultSet':
        """filter_all_by_value.
        Calls `Result.filter_all` for each piece and a given callable

        :param self:
        :param test:
        :type test: Callable
        :rtype: 'ResultSet'
        """
        return ResultSet({k: self.store[k].filter_all(test) for k in self.store}) 

    def filter_all_by_key(self, test: Callable) -> 'ResultSet':
        """filter_all_by_key.
        Filters out entries whose key when called with `test` returns false.
        Used to filter by `Piece` instead of `Position`.

        :param self:
        :param test:
        :type test: Callable
        :rtype: 'ResultSet'
        """
        return ResultSet({k: self.store[k] for k in self.store if test(k)})

    def clear_set(self, pieces: List[Piece]) -> None:
        """clear_set.
        Clears all the moves for given piece

        :param self:
        :param pieces:
        :type pieces: List[Piece]
        :rtype: None
        """
        for k in self.store:
            if k in pieces:
                self.store[k] = Result()

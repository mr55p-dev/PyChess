from enum import Enum, auto
from collections.abc import MutableMapping
from typing import Any, Callable, Dict, Iterator, List, Optional

from Chess.coordinate import Position
from Chess.pieces import King, Piece


class ResultKeys(Enum):
    passive = auto()
    capture = auto()
    attack = auto()
    defend = auto()
    pin = auto()


class BaseResult(MutableMapping):
    __slots__ = ('store')

    @staticmethod
    def flatten(l: List[List[Any]]) -> List[Any]:
        return [j for i in l for j in i]


class Result(BaseResult):
    __slots__ = ()
    _KT = ResultKeys
    _VT = List[Position]

    def __init__(self, res: Dict[_KT, _VT] = {}) -> None:
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
        filtered = [i for i in self.store[key] if test(i)]
        res = Result({k: self.store[k] for k in self.store})
        res[key] = filtered
        return res
    
    def filter_valid(self, test: Callable) -> 'Result':
        res = Result({k: self.store[k] for k in self.store})
        res[ResultKeys.passive] = [i for i in self.store[ResultKeys.passive] if test(i)]
        res[ResultKeys.capture] = [i for i in self.store[ResultKeys.capture] if test(i)]
        return res

    def filter_all(self, test: Callable) -> 'Result':
        res = Result({k: self.store[k] for k in self.store})
        for k in self.store:
            res[k] = [i for i in self.store[k] if test(i)]
        return res

    @property
    def has_moves(self) -> bool:
        for k in self.store:
            if self.store[k]:
                return True
        return False

    @property
    def has_passive_or_capture(self) -> bool:
        if self.store[ResultKeys.capture] or self.store[ResultKeys.passive]:
            return True
        return False

class ResultSet(BaseResult):
    __slots__ = ()
    _KT = Piece
    _VT = Result

    def __init__(self, mapping: Dict[_KT, _VT] = {}) -> None:
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
        result_passive = self.flatten([result[ResultKeys.passive] for result in self.store.values()])
        result_capture = self.flatten([result[ResultKeys.capture] for result in self.store.values()])
        return result_passive + result_capture

    @property
    def all_passive(self) -> List[Position]:
        return self.flatten([result[ResultKeys.passive] for result in self.store.values()])

    @property
    def all_capture(self) -> List[Position]:
        return self.flatten([result[ResultKeys.capture] for result in self.store.values()])

    @property
    def all_defend(self) -> List[Position]:
        return self.flatten([result[ResultKeys.defend] for result in self.store.values()])

    @property
    def all_attack(self) -> List[Position]:
        return self.flatten([result[ResultKeys.attack] for result in self.store.values()])

    @property
    def all_pins(self) -> List[Position]:
        return self.flatten([result[ResultKeys.pin] for result in self.store.values()])

    @property
    def king(self) -> Result:
        for k in self.store:
            if isinstance(k, King):
                return self.store[k]
        raise IndexError("There is no king in this result set")

    def lookup_pin(self, pin_loc: Position) -> Optional[Piece]:
        for piece in self.store:
            if pin_loc in self.store[piece][ResultKeys.pin]:
                return piece
        return None

    def filter_by_move_type(self, key: ResultKeys , test: Callable) -> 'ResultSet':
        return ResultSet({k: self.store[k].filter(key, test) for k in self.store})

    def filter_all_by_value(self, test: Callable) -> 'ResultSet':
        return ResultSet({k: self.store[k].filter_all(test) for k in self.store}) 

    def filter_all_by_key(self, test: Callable) -> 'ResultSet':
        return ResultSet({k: self.store[k] for k in self.store if test(k)})

    def clear_set(self, pieces: List[Piece]) -> None:
        for k in self.store:
            if k in pieces:
                self.store[k] = Result()
        
    def clear(self) -> None:
        for k in self.store:
            self.store[k] = Result()
        
    # This should be redundant
    def lookup_kind(self, kind_str: str) -> 'ResultSet':
        empty_set = ResultSet()
        for k in self.store:
            if k.kind == kind_str:
                empty_set[k] = self.store[k]  # type: ignore
        return empty_set



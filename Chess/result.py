from enum import Enum, auto
from collections.abc import MutableMapping
from typing import Any, Callable, Dict, Iterator, List, Optional, Type

from Chess.coordinate import Position
from Chess.pieces import King, Piece

class ResultKeys(Enum):
    passive = auto()
    capture = auto()
    attack = auto()
    defend = auto()
    pin = auto()

class BaseResult(MutableMapping):
    _KT = ResultKeys
    _VT = List[Position]

    def __init__(self) -> None:
        self.__store = dict()

    def __len__(self) -> int:
        return len(self.__store)

    @staticmethod
    def flatten(l: List[List[Any]]) -> List[Any]:
        return [j for i in l for j in i]


class Result(BaseResult):
    _KT = ResultKeys
    _VT = List[Position]

    def __init__(self) -> None:
        self.__store = {k: [] for k in ResultKeys}
    
    def __delitem__(self, v: _KT) -> None:
        del self.__store[v]

    def __getitem__(self, k: _KT) -> _VT:
        return self.__store[k]

    def __setitem__(self, k: _KT, v: _VT) -> None:
        self.__store[k] = v

    def __iter__(self) -> Iterator[_KT]:
        return iter(self.__store)

    def filter(self, key: ResultKeys, test: Callable) -> None:
        self.__store[key] = [i for i in self.__store[key] if test(i)]

    def filter_all(self, test: Callable) -> None:
        for k in self.__store:
            self.filter(k, test)

    @property
    def has_moves(self) -> bool:
        for k in self.__store:
            if self.__store[k]:
                return True
        return False

class ResultSet(BaseResult):
    _KT = Piece
    _VT = Result

    def __init__(self, piece_list: List[Piece] = []) -> None:
        self.__store = {k: Result() for k in piece_list}

    def __delitem__(self, v: _KT) -> None:
        del self.__store[v]

    def __getitem__(self, k: _KT) -> _VT:
        return self.__store[k]

    def __setitem__(self, k: _KT, v: _VT) -> None:
        self.__store[k] = v

    def __iter__(self) -> Iterator[_KT]:
        return iter(self.__store)

    @property
    def all_valid(self) -> List[Position]:
        result_passive = self.flatten([result[ResultKeys.passive] for result in self.__store.values()])
        result_capture = self.flatten([result[ResultKeys.capture] for result in self.__store.values()])
        return result_passive + result_capture

    @property
    def all_passive(self) -> List[Position]:
        return self.flatten([result[ResultKeys.passive] for result in self.__store.values()])

    @property
    def all_capture(self) -> List[Position]:
        return self.flatten([result[ResultKeys.capture] for result in self.__store.values()])

    @property
    def all_defend(self) -> List[Position]:
        return self.flatten([result[ResultKeys.defend] for result in self.__store.values()])

    @property
    def all_attack(self) -> List[Position]:
        return self.flatten([result[ResultKeys.attack] for result in self.__store.values()])

    @property
    def all_pins(self) -> List[Position]:
        return self.flatten([result[ResultKeys.pin] for result in self.__store.values()])

    @property
    def king(self) -> Result:
        for k in self.__store:
            if isinstance(k, King):
                return self.__store[k]
        raise IndexError("There is no king in this result set")

    def lookup_pin(self, pin_loc: Position) -> Optional[Piece]:
        for piece in self.__store:
            if pin_loc in self.__store[piece][ResultKeys.pin]:
                return piece
        return None

    def filter_by_move_type(self, key: ResultKeys , test: Callable) -> None:
        for k in self.__store:
            self.__store[k].filter(key, test)

    def filter_all_by_value(self, test: Callable) -> None:
        for k in self.__store:
            self.__store[k].filter_all(test)

    def filter_all_by_key(self, test: Callable) -> None:
        for k in self.__store:
            if not test(k):
                del(self.__store[k])

    def clear_set(self, pieces: List[Piece]) -> None:
        for k in self.__store:
            if k in pieces:
                del self.__store[k]
                self.__store[k] = Result()
        
    def clear(self) -> None:
        for k in self.__store:
            del self.__store[k]
            self.__store[k] = Result()
        
    # This should be redundant
    def lookup_kind(self, kind_str: str) -> 'ResultSet':
        pieces = [k for k in self.__store if k.kind == kind_str]
        empty_set = ResultSet(pieces)
        for k in self.__store:
            if k.kind == kind_str:
                empty_set[k] = self.__store[k]  # type: ignore
        return empty_set


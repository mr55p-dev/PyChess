from abc import ABC, abstractmethod, abstractproperty
from typing import List, Tuple, Union

class Vec(ABC):
    __slots__ = ('i', 'j')
    
    @abstractmethod
    def __init__(self, i: int, j: int):
        ...

class Position(ABC):
    __slots__ = ('i', 'j')

    @abstractmethod
    def __init__(self, *args: Union[Tuple[str], Tuple[int, int]]):
        ...

    @abstractmethod
    def __eq__(self, o) -> bool:
        ...

    @abstractmethod
    def __ne__(self, o: 'Position') -> bool:
        ...

    @abstractmethod
    def __add__(self, o: Vec) -> 'Position':
        ...

    @abstractmethod
    def __sub__(self, o: Union[Vec, 'Position']) -> 'Position':
        ...

    @abstractmethod
    def is_valid(self) -> bool:
        ...

    @abstractmethod
    def path_to(self, to: 'Position') -> List['Position']:
        ...

    @abstractproperty
    def algebraic(self) -> str:
        ...

class Move(ABC):
    @abstractproperty
    def start(self) -> Position:
        ...

    @abstractproperty
    def end(self) -> Position:
        ...

    @abstractproperty
    def takes(self) -> bool:
        ...

    @abstractproperty
    def is_castle(self) -> str:
        ...

class Piece(ABC):
    @abstractmethod
    def __eq__(self, other: 'Piece') -> bool:
        ...

    @abstractmethod
    def __neq__(self, other: 'Piece') -> bool:
        ...

    @abstractmethod
    def __hash__(self) -> int:
        ...
        
    @abstractproperty
    def colour(self) -> int:
        ...

    @abstractproperty
    def position(self) -> Position:
        ...
        
    @abstractproperty
    def kind(self) -> str:
        ...
        
    @abstractproperty
    def distance(self) -> int:
        ...

    @abstractproperty
    def is_active(self) ->  bool:
        ...

    @is_active.setter
    def is_active(self, state: bool) -> None:
        ...

    @abstractproperty
    def projections(self) -> List[Vec]:
        ...

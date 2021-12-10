USE_CPP = True 

WHITE = True
BLACK = False

CART_COORD = list(range(0, 8))
RANKS = list(range(1, 9))

FILES = {
    0: "A",
    1: "B",
    2: "C",
    3: "D",
    4: "E",
    5: "F",
    6: "G",
    7: "H"
}

REV_FILES = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6,
    "H": 7
}

PIECE_TYPES = ["K", "Q", "R", "N", "B", "P"]

class BaseEnum:
    __slots__ = ()

    def __iter__(self):
        return iter(self.__slots__)

class MoveSignal(BaseEnum):
    __slots__ = ('blocked', 'capture', 'empty', 'checking_attack', 'disallowed', 'attacks')

    def __init__(self) -> None:
        blocked         = 0
        capture         = 1
        empty           = 2
        checking_attack = 3
        disallowed      = 4
        attacks         = 5

class WinState():
    __slots__ = ('cont', 'mate', 'stalemate', 'draw', 'move_timeout',)

    def __init__(self) -> None:
        cont = 1
        mate = 2
        stalemate = 3
        draw = 4
        move_timeout = 5
# 
# class ResultKeys():
#     """
#     Enum iteration is VERY slow
#     We can replace it with a base class that defines a slot for each key,
#     returns an itertor of those keys for __iter__ and defines a unique value for
#     each of them which is used as the key in the Results store dict"""
# 
#     __slots__ = ('passive', 'capture', 'attack', 'defend', 'pin')
#     def __init__(self):
#         passive = 1
#         capture = 2
#         attack = 3
#         defend = 4
#         pin = 5
# 
#     def __iter__(self):
#         return iter(self.__slots__)
# 
# 
class ResultKeys():
    """
    Enum iteration is VERY slow
    We can replace it with a base class that defines a slot for each key,
    returns an itertor of those keys for __iter__ and defines a unique value for
    each of them which is used as the key in the Results store dict"""

    # __slots__ = ('passive', 'capture', 'attack', 'defend', 'pin')
    passive = 1
    capture = 2
    attack = 3
    defend = 4
    pin = 5

    def __iter__(self):
        return [1, 2, 3, 4, 5]


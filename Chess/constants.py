from typing import Iterator


# Define the values for piece/player colours

ALLOW_CPP = False

class colourFactory():
    def __init__(self):
        try:
            from libpychess import white, black
            self.white = white
            self.black = black
        except ImportError:
            self.white = True
            self.black = False

cf = colourFactory()
WHITE = cf.white
BLACK = cf.black

# Valid piece identifiers, used in helpers to quickly mock
# piece instantiation
PIECE_TYPES = ["K", "Q", "R", "N", "B", "P"]

class BaseEnum:
    """A simple enum class implementing __slots__ for very fast item recall.

    Classes can be derrived from this, and must implement __slots__ for each of the instance attributes
    defined in the object constructor. Note that static methods will conflict with instance attributes.
    """
    __slots__ = ()

    def __iter__(self) -> Iterator:
        return iter(self.__slots__)

class MoveSignal(BaseEnum):
    """MoveSignal enum
    keys:

    blocked = 0
    capture = 1
    empty = 2
    checking_attack = 3
    disallowed = 4
    attacks = 5

    Defines the possible return types for Board.__py_allowed_move - these signal the category of move.
    Python reference implementation is identical to the implemetation by libpychess's MoveAnalyser."""

    __slots__ = ('blocked', 'capture', 'empty', 'checking_attack', 'disallowed', 'attacks')

    def __init__(self) -> None:
        blocked         = 0
        capture         = 1
        empty           = 2
        checking_attack = 3
        disallowed      = 4
        attacks         = 5

class WinState():
    """WinState enum
    keys:

    cont = 1
    mate = 2
    stalemate = 3
    draw = 4
    move_timeout = 5

    Enum for the types of state the board can be in. The board is always in one of these states.
    Note that draw and move_timeout are not yet implemented by either game or state."""

    __slots__ = ('cont', 'mate', 'stalemate', 'draw', 'move_timeout',)

    def __init__(self) -> None:
        cont = 1
        mate = 2
        stalemate = 3
        draw = 4
        move_timeout = 5

class ResultKeys():
    """ResultKeys
    keys:

    passive = 1
    capture = 2
    attack = 3
    defend = 4
    pin = 5

    Base object with static attributes mapping to integers. Same implementation as in libpychess
    explicitly to allow the transposition from the C++ library output to the Python Result object to
    be completely seamless (just pass the output as the constructor for Result). Used to be implemeted
    as a BaseEnum which was significantly faster than the original implementation relying on enum.Enum
    """
    passive = 1
    capture = 2
    attack = 3
    defend = 4
    pin = 5

    def __iter__(self):
        return [1, 2, 3, 4, 5]


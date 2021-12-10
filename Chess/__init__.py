from .constants import BLACK, WHITE, USE_CPP
if USE_CPP:
    import sys
    sys.path.append("vendor/pychessbinds/build")

from .state import Board
from .coordinate import Vec
from .view import view_board_colour as view_board
from .pieces import Piece
from .helpers import pieces_from_fen

try:
    from libpychess import Position
except ImportError:
    from .coordinate import Position

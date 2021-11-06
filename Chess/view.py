from Chess.constants import WHITE
from Chess.state import Board


class bcolors:
    """Class providing terminal escape sequences to set text colour.
    From https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    """Custom chess piece
    Guidance from https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences"""
    WHITE_PIECE = '\033[38;5;0;48;5;255m' # Black text = [35;5;0; white bg = 48;5;255m
    BLACK_PIECE = '\033[38;5;255;48;5;0m' # Black text = [35;5;0; white bg = 48;5;255m


def view_board(board: Board):
    """Simple fuction to view a game state"""
    representation = [[" " for _ in range(8)] for _ in range(8)]
    for loc, piece in board.map.items():
        prefix = bcolors.WHITE_PIECE if piece.colour == WHITE else bcolors.BLACK_PIECE
        representation[loc.i][loc.j] = prefix + piece.kind + bcolors.ENDC
    print("\n".join([" ".join([cell for cell in row]) for row in representation]))


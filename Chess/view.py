from Chess.constants import BLACK, WHITE
from Chess.result import ResultKeys
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
    WHITE_SQUARE = '\033[48;5;250m'
    BLACK_SQUARE = '\033[48;5;71m'



def view_board_mono(board: Board, show_moves: Piece = None):
    """Simple fuction to view a game state"""
    representation = [["   " for _ in range(8)] for _ in range(8)]
    count = 0
    for loc, piece in board.loc_map.items():
        rep = piece.kind
        if piece.colour == BLACK: rep = piece.kind.lower()
        representation[loc.i][loc.j] = f" {rep} "

    if show_moves:
        moves = board.legal_moves(show_moves)
        for cap in moves[show_moves][ResultKeys.capture]:
            representation[cap.i][cap.j] = " x "
        for pas in moves[show_moves][ResultKeys.passive]:
            representation[pas.i][pas.j] = " o "
        print("PIECE MOVES")

    print(f"{'White' if board.to_move else 'Black'} to move - turn {board.turn}")
    print("\n".join(["".join([cell for cell in row]) for row in representation[::-1]]))

def view_board_colour(board: Board, show_moves=None):
    """Simple fuction to view a game state"""
    representation = [["   " for _ in range(8)] for _ in range(8)]
    count = 0
    for loc, piece in board.loc_map.items():
        prefix = bcolors.WHITE_PIECE if piece.colour == WHITE else bcolors.BLACK_PIECE
        representation[loc.i][loc.j] = f"{prefix} {piece.kind} {bcolors.ENDC}"

    if show_moves:
        moves = board.legal_moves(show_moves)
        for cap in moves[show_moves][ResultKeys.capture]:
            representation[cap.i][cap.j] = " x "
        for pas in moves[show_moves][ResultKeys.passive]:
            representation[pas.i][pas.j] = " o "
        print("PIECE MOVES")
        
    for i_ind, i in enumerate(representation):
        for j_ind, _ in enumerate(i):
            square = representation[i_ind][j_ind]
            if (i_ind + count) % 2 == 0:
                representation[i_ind][j_ind] = bcolors.WHITE_SQUARE + square + bcolors.ENDC
            else:
                representation[i_ind][j_ind] = bcolors.BLACK_SQUARE + square + bcolors.ENDC
            count += 1

    print(f"{'White' if board.to_move else 'Black'} to move - turn {board.turn}")
    print("\n".join(["".join([cell for cell in row]) for row in representation[::-1]]))


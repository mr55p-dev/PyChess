from Chess.state import Board


def view_game(board: Board):
    """Simple fuction to view a game state"""
    representation = [[" " for _ in range(8)] for _ in range(8)]
    for loc, piece in board.map:
        representation[loc.i][ loc.j] = piece.kind
    print("\n".join([" ".join([cell for cell in row]) for row in representation]))


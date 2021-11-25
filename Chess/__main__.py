from copy import copy
from Chess.constants import WHITE
from Chess.helpers import move_from_str, pieces_from_fen
from Chess.state import Board  # type: ignore
from Chess.view import view_board_mono, view_board_colour  # type: ignore
from Chess.coordinate import Position, Vec # type: ignore


def construct_board(fen):
    params = pieces_from_fen(fen)
    board = Board(params[0], params[1], params[5], params[2])
    return board

def game_end(board: Board):
    if board.is_mate or board.is_stale:
        return True
    else:
        return False

def ng():
    view_board = view_board_mono
    hist = []
    # fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" Initial
    fen = "rnb1k1nr/pppp1ppp/8/8/PP6/8/4PPPP/RNq1KBNR w kq - 0 1" # Checkmate
    board = construct_board(fen)

    for i in [1]:
        hist.append(copy(board))
        moving = "white" if board.to_move == WHITE else "black"

        print(board.to_fen())
        print(f"Turn {board.turn} - {moving} to move.")

        view_board(board)
        move_str = i
        move = move_from_str(move_str=move_str, board=board)

        if board.move(move):
            continue
        else:
            raise Exception("invalid state woo")


def ngi():
    view_board = view_board_mono
    hist = []
    # fen = input("FEN: ")
    fen = None
    if not fen: fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = construct_board(fen)
    
    while not game_end(board):
        hist.append(copy(board))
        moving = "white" if board.to_move == WHITE else "black"

        print(f"Turn {board.turn} - {moving} to move.")
        view_board(board)

        complete = False
        while not complete:
            move_str = input("Enter a move> ")
            try: move = move_from_str(move_str=move_str, board=board)
            except ValueError: print("wrong."); continue

            complete = board.move(move)


if __name__ == "__main__":
            
    ng()


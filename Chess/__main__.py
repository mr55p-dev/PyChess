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
    moves = ["a4", "a5", 
             "b4", "b5",
             "axb5", "c5",
             "Nc3", "Nf6", 
             "bxc5", "a4",
             "Rxa4", ""]

    hist = []
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = construct_board(fen)

    for i in moves:
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
        hist = []
        fen = input("FEN: ")
        if not fen: fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        board = construct_board(fen)
        
        while not game_end(board):
            valid_moves = board.get_move_set(board._get_moving())
            moving = "white" if board.to_move == WHITE else "black"
            new_state = None
            while not new_state:
                print(board.to_fen())
                print(f"Turn {board.turn} - {moving} to move.")
                view_board(board)
                # move_str = input("Enter a move> ")
                move_str = "a4"
                try: move = move_from_str(move_str=move_str, board=board)
                except ValueError: print("wrong."); continue

                new_state = board.move(move)

            hist.append(copy(board))
            board = new_state

if __name__ == "__main__":
            
    ng()


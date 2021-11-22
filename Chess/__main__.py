from copy import copy
from Chess.constants import WHITE
from Chess.helpers import move_from_str, pieces_from_fen
from Chess.state import Board  # type: ignore
from Chess.view import view_board  # type: ignore
from Chess.coordinate import Position, Vec # type: ignore

def construct_board(fen):
    params = pieces_from_fen(fen)
    board = Board(params[0], params[1], params[5])
    return board

def game_end(board: Board):
    if board.is_mate or board.is_stale:
        return True
    else:
        return False

if __name__ == "__main__":
    def ng():
        hist = []
        fen = input("FEN: ")
        if fen:
            board = construct_board(fen)
        else:
            board = Board()
        
        while not game_end(board):
            valid_moves = board.get_move_set(board._get_moving())
            moving = "white" if board.to_move == WHITE else "black"
            while True:
                print(board.to_fen())
                print(f"Turn {board.turn} - {moving} to move.")
                view_board(board)
                move_str = input("Enter a move> ")
                try: move = move_from_str(move_str=move_str, board=board)
                except ValueError: print("wrong."); continue
                
                new_state = board.move(move)
                if new_state: break
                else: print("A new state was not created")

            hist.append(copy(board))
            board = new_state


        
    ng()


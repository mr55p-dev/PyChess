from copy import copy
from Chess.constants import WHITE
from Chess.helpers import pieces_from_fen
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
        board = Board()
        
        while not game_end(board):
            valid_moves = board.get_move_set(board._get_moving())
            moving = "white" if board.to_move == WHITE else "black"
            while True:
                print(f"Turn {board.turn} - {moving} to move.")
                view_board(board)
                dest = input("Select a destination square>>> ")
                new_state = board.move(dest)
                if new_state:
                    break
                else:
                    print("A new state was not created")

            hist.append(copy(board))
            board = new_state


        
    ng()


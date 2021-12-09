from copy import copy
from Chess import view
from Chess.helpers import move_from_str, pieces_from_fen
from Chess.state import Board
from Chess.view import view_board_colour
from Chess.game import Game


def construct_board(fen):
    params = pieces_from_fen(fen)
    board = Board(*params)
    return board

def game_end(board: Board):
    if board.is_mate or board.is_stale:
        return True
    else:
        return False

def new_game_interactive():
    if (x:=input(">>> ")):
        board = construct_board(x)
    else:
        board = Board()
    game = Game(view_board_colour, start_state=board)
    game.play()

if __name__ == "__main__":
            
    g = Game(view_board_colour)
    g.play()


from Chess.__main__ import construct_board
from Chess.helpers import move_from_str
from Chess.view import view_board_mono

fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
moves = ["d4", "e5",
         "c4", "exd4",
         "Nc3", "Nf6",
         "Bf5"]

board = construct_board(fen)
for move in moves:
    view_board_mono(board)
    move_obj = move_from_str(move, board)
    board.move(move_obj)


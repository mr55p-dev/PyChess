from Chess.__main__ import construct_board
from Chess.coordinate import Move, Position
from Chess.game import Game
from Chess.helpers import move_from_str
from Chess.state import Board
from Chess.view import view_board_mono

fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
P = Position
movs = []

movs = ["c3", "Nc6", "d4", "Nxd4", "cxd4", "d5", "e4", "dxe4", "Be3", "Qxd4", "Qxd4", "a6", "Na3", "a5", "Rd1", "a4", "Qd8"]

# board = Board()
#view_board_mono(board)
# for move in movs:
#     ans = board.move(move)
#     print(ans)
#     view_board_mono(board)
 
game = Game(
    view_callback=view_board_mono,
    start_state=fen
)
game.show_board()

for move in movs: 
    print(f"Perforing {move}")
    game.execute_move_str(move)
    game.show_board()

    print(game.peek.is_check)


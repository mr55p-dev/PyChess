from Chess.__main__ import construct_board
from Chess.coordinate import Move, Position
from Chess.game import Game
from Chess.helpers import move_from_str
from Chess.state import Board
from Chess.view import view_board_mono

fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
P = Position
movs = [Move(P("D2"), P("D4"), False), Move(P("E7"), P("E5"), False)]
         # "c4", "exd4",
         # "Nc3", "Nf6",
         # "Bf5"]


board = Board()
view_board_mono(board)
for move in movs:
    ans = board.move(move)
    print(ans)
    view_board_mono(board)

move_strings = ["d4", "e5"]

game = Game(
    view_callback=view_board_mono,
    start_state=fen
)
game.show_board()

for move in move_strings:
    print(f"Performing {move}")
    game.execute_move_str(move)
    game.show_board()



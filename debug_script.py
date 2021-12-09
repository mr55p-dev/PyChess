from Chess.__main__ import construct_board
from Chess.coordinate import Move, Position
from Chess.game import Game
from Chess.helpers import move_from_str
from Chess.state import Board
from Chess.view import view_board_mono

starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
checkmate_fen = "r1bQkbnr/1pp1pppp/8/8/p3p3/N3B3/PP3PPP/3RKBNR b KQkq - 0 8"
pinned_knight_fen = "r1bqkbnr/pppp1ppp/8/4n3/8/4Q3/PPPPPPPP/RNB1KBNR b KQkq - 0 1"
white_can_castle_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1"
black_can_castle_fen = "r3k2r/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1"
black_castle_queenside = "r3kbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq - 0 1"
false_checkmate_fen = "r1bq1rk1/ppp3pp/5n2/3Nnp2/8/3Q1NP1/PPP1PP1P/2KR1B1R w - - 0 1"
missed_b4_fen = "8/3B2p1/8/2k2R2/4P3/1P1K2P1/2P4P/8 b - - 0 1"
problematic_queen_fen = "r2kQb1r/pbpp3p/1pn1p3/7B/3PP2q/P1N5/1PP2PPP/R3K2R b KQ - 2 13"

start = construct_board(starting_fen)
game = Game(view_board_mono, start_state=start)
game.show_board()
game.execute_move_str("d3")
game.execute_move_str("d6")

# castling_move = Move(Position("E1"), Position("C1"), False, castle="long") 
# board = construct_board(white_can_castle_fen)
# view_board_mono(board)
# board.move(castling_move)
# view_board_mono(board)
# board.to_fen()

# movs = ["c3", "Nc6", "d4", "Nxd4", "cxd4", "d5", "e4", "dxe4", "Be3", "Qxd4", "Qxd4", "a6", "Na3", "a5", "Rd1", "a4", "Qd8"]
# game = Game(
#     view_callback=view_board_mono,
#     start_state=fen
# )
# game.show_board()
# 
# for move in movs: 
#     print(f"Perforing {move}")
#     game.execute_move_str(move)
#     game.show_board()
# 
#     print(game.peek.is_check)
# 

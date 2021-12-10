from Chess.constants import BLACK, WHITE
from Chess.coordinate import Move
from Chess.game import Game
from Chess.helpers import pieces_from_fen 
from Chess.pieces import Pawn
from Chess.state import Board
from Chess.view import view_board_mono
try:
    from libpychess import Position
except ImportError:
    from Chess.coordinate import Position


p1 = Pawn(WHITE, Position((2, 2)))
p2 = Pawn(BLACK, Position((3, 3)))

d = {p1: 1, p2: 2}
print(f"p1 hash {hash(p1)}")

n = Pawn(WHITE, Position((2, 2)))
print(f"n1 hash {hash(n)}")

print(n == p1)
print(n in d)

starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
checkmate_fen = "r1bQkbnr/1pp1pppp/8/8/p3p3/N3B3/PP3PPP/3RKBNR b KQkq - 0 8"
pinned_knight_fen = "r1bqkbnr/pppp1ppp/8/4n3/8/4Q3/PPPPPPPP/RNB1KBNR b KQkq - 0 1"
white_can_castle_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1"
black_can_castle_fen = "r3k2r/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1"
black_castle_queenside = "r3kbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq - 0 1"
false_checkmate_fen = "r1bq1rk1/ppp3pp/5n2/3Nnp2/8/3Q1NP1/PPP1PP1P/2KR1B1R w - - 0 1"
missed_b4_fen = "8/3B2p1/8/2k2R2/4P3/1P1K2P1/2P4P/8 b - - 0 1"
problematic_queen_fen = "r2kQb1r/pbpp3p/1pn1p3/7B/3PP2q/P1N5/1PP2PPP/R3K2R b KQ - 2 13"

def construct_board(fen):
    params = pieces_from_fen(fen)
    board = Board(*params)
    return board

start = construct_board(starting_fen)
game = Game(view_board_mono, start_state=start)
game.show_board()
game.execute_move_str("d4")
game.execute_move_str("e5")
game.execute_move_str("dxe5")
game.show_board()

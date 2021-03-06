"""I, Ellis Lunnon, have read and understood the School's Academic Integrity Policy, as well as guidance relating to this
module, and confirm that this submission complies with the policy. The content of this file is my own original work,
with any significant material copied or adapted from other sources clearly indicated and attributed."""

from Chess.constants import BLACK, WHITE
from Chess.coordinate import Move
from Chess.game import Game
from Chess.helpers import pieces_from_fen 
from Chess.pieces import Pawn
from Chess.state import Board, construct_board
from Chess.view import view_board_mono
try:
    from libpychess import Position
except ImportError:
    from Chess.coordinate import Position

starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
checkmate_fen = "r1bQkbnr/1pp1pppp/8/8/p3p3/N3B3/PP3PPP/3RKBNR b KQkq - 0 8"
pinned_knight_fen = "r1bqkbnr/pppp1ppp/8/4n3/8/4Q3/PPPPPPPP/RNB1KBNR b KQkq - 0 1"
white_can_castle_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1"
black_can_castle_fen = "r3k2r/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1"
black_castle_queenside = "r3kbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq - 0 1"
false_checkmate_fen = "r1bq1rk1/ppp3pp/5n2/3Nnp2/8/3Q1NP1/PPP1PP1P/2KR1B1R w - - 0 1"
missed_b4_fen = "8/3B2p1/8/2k2R2/4P3/1P1K2P1/2P4P/8 b - - 0 1"
problematic_queen_fen = "r2kQb1r/pbpp3p/1pn1p3/7B/3PP2q/P1N5/1PP2PPP/R3K2R b KQ - 2 13"

no_dxe4_fen = "rnbqkbnr/pp2pppp/2p5/3p4/4P3/2N2Q2/PPPP1PPP/R1B1KBNR b KQkq - 0 3"
c3_issue_fen = "r3k2r/pp2b1pp/2p1N1b1/q7/8/3P1Q2/PPP2PPP/R3K2R w KQkq - 0 15"
qg2_fen = "r4r1k/1p2Np2/p2p1np1/2p5/Q1P1P2p/3B1P1q/PP2K3/R6R b - - 0 23"

start = construct_board(qg2_fen)
game = Game(view_board_mono, start_state=start)

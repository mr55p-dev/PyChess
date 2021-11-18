import pytest
from Chess.state import Board
from Chess.helpers import pieces_from_fen

fen = [
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "r4rk1/pp3p2/8/2pp2p1/1B4np/P3P1Q1/KP3PPP/3q1B1R w - - 0 22",
    "r2qk2r/ppp2ppp/5n2/3p1b2/3b1B2/2NN4/PP2PPPP/n1KQ1B1R w kq - 4 11",
    "5rk1/1p1b2pp/5p2/1p6/3P4/2P2N2/PP2r1K1/5R2 w - - 2 33",
    "r2qkb1r/1p1b1ppp/4n3/1p1p4/3P4/1QP2NK1/PP1N3P/R3n3 w kq - 0 21",
    "r3r1k1/5pp1/pR2b3/2pp2pN/3b4/7P/P1P2PP1/3R2K1 b - - 1 25"
]

@pytest.mark.parametrize("fen_str", fen)
def test_fen(fen_str):
    params = pieces_from_fen(fen_string=fen_str)
    other_params = params[2:]
    board = Board(params[0], params[5], params[1], other_params)
    assert fen_str == board.to_fen()

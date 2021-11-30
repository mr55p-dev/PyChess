from itertools import product
import pytest
from Chess.__main__ import construct_board
from Chess.coordinate import Move, Position
from Chess.result import ResultKeys
from Chess.state import Board
from Chess.helpers import pieces_from_fen

fen = [
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "r4rk1/pp3p2/8/2pp2p1/1B4np/P3P1Q1/KP3PPP/3q1B1R w KQkq - 0 22",
    "r2qk2r/ppp2ppp/5n2/3p1b2/3b1B2/2NN4/PP2PPPP/n1KQ1B1R w KQkq - 4 11",
    "5rk1/1p1b2pp/5p2/1p6/3P4/2P2N2/PP2r1K1/5R2 w KQkq - 2 33",
    "r2qkb1r/1p1b1ppp/4n3/1p1p4/3P4/1QP2NK1/PP1N3P/R3n3 w KQkq - 0 21",
    "r3r1k1/5pp1/pR2b3/2pp2pN/3b4/7P/P1P2PP1/3R2K1 b KQkq - 1 25"
]

@pytest.mark.parametrize("fen_str", fen)
def test_fen(fen_str):
    params = pieces_from_fen(fen_string=fen_str)
    other_params = params[2:]
    board = Board(params[0], params[5], params[1], other_params)
    assert fen_str == board.to_fen()

def test_initalise():
    board = Board()
    board.calculate()

def test_move():
    board = Board()
    move = Move(Position("A2"), Position("A4"), False)
    board.move(move)
    assert board.to_fen() == "rnbqkbnr/pppppppp/8/8/P7/8/1PPPPPPP/RNBQKBNR b KQkq - 0 1"

fen_tests = [
    "r3kbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq - 0 1",
    "r3kbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQk - 0 1",
    "r3k2r/pppppppp/8/3n4/2P5/5b2/PP1PPPPP/RNBQKBNR b KQ - 0 1",
    "r3k2r/pppppppp/8/3n4/2P5/5b2/PP1PPPPP/RNBQKBNR b KQk - 0 1",
    "r3k2r/ppppp1pp/8/3n1Q2/2P5/5b2/PP1PPPPP/RNB1KBNR b KQkq - 0 1",
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/R3KBNR w KQkq - 0 1",
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQ - 0 1",
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w - - 0 1",
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w K - 0 1",
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/4K3 w kq - 0 1",
]
correct_outcome = [
    [Position("C8")],
    [],
    [],
    [Position("G8")],
    [Position("C8")],
    [Position("C1")],
    [Position("G1"), Position("C1")],
    [],
    [Position("G1")],
    []
]

@pytest.mark.parametrize('fen,outcome', zip(fen_tests, correct_outcome))
def test_castling(fen, outcome):
    board = construct_board(fen)
    castle = board.valid_castle()
    assert castle == outcome

@pytest.mark.parametrize('fen,outcome', zip(fen_tests, correct_outcome))
def test_king_passive(fen, outcome):
    board = construct_board(fen)
    valid_moves = board.allied_moves
    king_moves = valid_moves.king[ResultKeys.passive]
    for i in outcome:
        assert i in king_moves

@pytest.mark.parametrize('fen,outcome', zip(fen_tests, correct_outcome))
def test_king_passive_not(fen, outcome):
    board = construct_board(fen)
    valid_moves = board.allied_moves
    king_moves = valid_moves.king[ResultKeys.passive]
    possible = [Position("C1"), Position("G1"), Position("C8"), Position("G8")]
    for j in possible:
        if j not in outcome:
            assert j not in king_moves




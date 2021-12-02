from itertools import product
import pytest
from Chess.__main__ import construct_board
from Chess.coordinate import Move, Position
from Chess.result import ResultKeys
from Chess.state import Board
from Chess.helpers import pieces_from_fen

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



import pytest
from itertools import product
from Chess.pState import PyBoard
from Chess.cState import CBoard

fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
e4 = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1"
c5 = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2"
Nf3 = "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"

boards = [PyBoard, CBoard]

@pytest.mark.parametrize('board', boards)
def test_init(board):
    b = board()
    assert b.to_fen() == fen
    
fen_seq = [
    fen,
    e4,
    c5,
    Nf3
]

# These tests still fail as half move clock and en-passant not working
@pytest.mark.parametrize('fen, board', product(fen_seq, boards))
def test_construct(board, fen):
    b = board(fen)
    assert b.to_fen() == fen

def test_calculate():
    ...

def test_check():
    ...

def test_mate():
    ...

def test_stalemate():
    ...

def test_legal_moves():
    ...

def test_move():
    ...

def test_castle_long():
    ...

def test_castle_short():
    ...

def test_double_pawn_push():
    ...

def test_standard_capture():
    ...

def test_pawn_capture_valid():
    ...

def test_pawn_capture_invalid():
    ...

from Chess.constants import PIECE_TYPES, WHITE, BLACK
from Chess.coordinate import Position
from Chess.pieces import Piece, King, Queen, Knight, Rook, Bishop, Pawn


def test_init():
    p = Piece(WHITE, Position("A1"), 'K', 7, is_active = True)

def test_eq():
    p = Piece(WHITE, Position("A1"), 'K', 7, is_active = True)
    r = Piece(WHITE, Position("A1"), 'K', 7, is_active = True)
    assert p == r

def test_neq():
    p = Piece(WHITE, Position("A1"), 'K', 7, is_active = True)
    r = Piece(BLACK, Position("A1"), 'K', 7, is_active = True)
    s = Piece(BLACK, Position("B1"), 'K', 7, is_active = True)
    t = Piece(BLACK, Position("B1"), 'N', 7, is_active = True)
    u = Piece(BLACK, Position("B1"), 'N', 7, is_active = False)
    assert p != r != s != t != u

def test_hash():
    p = Piece(WHITE, Position("B7"), 'K', 7, is_active = True)
    # 111 001 1001011 1 1
    assert hash(p) == int(0b110001100101111)

def test_active():
    p = Piece(WHITE, Position("B7"), 'K', 7, is_active = True)
    assert p.is_active == True
    p.is_active = False
    assert p.is_active == False

def test_subclass_projections():
    pos = Position("A1")

    k = King(WHITE, pos)
    q = Queen(WHITE, pos)
    r = Rook(WHITE, pos)
    n = Knight(WHITE, pos)
    b = Bishop(WHITE, pos)
    p = Pawn(WHITE, pos)

    assert len(k.projections) == 8
    assert len(q.projections) == 8
    assert len(n.projections) == 8

    assert len(r.projections) == 4
    assert len(b.projections) == 4

    assert len(p.projections) == 3

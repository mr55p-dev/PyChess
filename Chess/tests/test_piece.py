import pytest
from Chess.API import Chess

cc = Chess(use_acceleration=True)
pc = Chess(use_acceleration=False)
constructors = [cc, pc]

@pytest.mark.parametrize('m', constructors)
def test_init(m: Chess):
    p = m.Pieces.Piece(m.white, m.Position("A1"), 'K', 7, [], False)

@pytest.mark.parametrize('m', constructors)
def test_eq(m: Chess):
    p = m.Pieces.Piece(m.white, m.Position("A1"), 'K', 7)
    r = m.Pieces.Piece(m.white, m.Position("A1"), 'K', 7)
    assert p == r

@pytest.mark.parametrize('m', constructors)
def test_neq(m: Chess):
    p = m.Pieces.Piece(m.white, m.Position("A1"), 'K')
    r = m.Pieces.Piece(m.black, m.Position("A1"), 'K')
    s = m.Pieces.Piece(m.black, m.Position("B1"), 'K')
    t = m.Pieces.Piece(m.black, m.Position("B1"), 'N')
    u = m.Pieces.Piece(m.black, m.Position("B2"), 'N')
    u.is_active = False
    assert p != r != s != t != u

@pytest.mark.parametrize('m', constructors)
def test_hash(m: Chess):
    p = m.Pieces.Piece(m.white, m.Position("B7"), 'K', 7)
    # 111 001 1001011 1 1
    assert hash(p) == int(0b110001100101111)

@pytest.mark.parametrize('m', constructors)
def test_active(m: Chess):
    p = m.Pieces.Piece(m.white, m.Position("B7"), 'K', 7)
    assert p.is_active == True
    p.is_active = False
    assert not p.is_active

@pytest.mark.parametrize('m', constructors)
def test_subclass_projections(m: Chess):
    pos = m.Position("A1")

    k = m.Pieces.King(m.white, pos)
    q = m.Pieces.Queen(m.white, pos)
    r = m.Pieces.Rook(m.white, pos)
    n = m.Pieces.Knight(m.white, pos)
    b = m.Pieces.Bishop(m.white, pos)
    p = m.Pieces.Pawn(m.white, pos)

    assert len(k.projections) == 8
    assert len(q.projections) == 8
    assert len(n.projections) == 8

    assert len(r.projections) == 4
    assert len(b.projections) == 4

    assert len(p.projections) == 3

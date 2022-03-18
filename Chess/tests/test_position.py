from collections import Counter

import pytest
from Chess.API import Chess

# Setup the API
pc = Chess(use_acceleration=False)
cc = Chess(use_acceleration=True)
position_constructors = [pc.Position, cc.Position]
vector_constructors = [pc.Vec, cc.Vec]

# Cute, hot, beuatiful, favourite

@pytest.mark.parametrize('position', position_constructors)
def test_init_py(position):
    p = position(0, 0)
    assert p.i == 0
    assert p.j == 0

@pytest.mark.parametrize('position', position_constructors)
def test_valid_py(position):
    p = position(0, 0)
    assert p.is_valid() == True

    q = position(-1, 0)
    assert q.is_valid() == False

    r = position(0, -1)
    assert r.is_valid() == False

    s = position(2, 8)
    assert s.is_valid() == False

    t = position(8, 2)
    assert t.is_valid() == False

@pytest.mark.parametrize('position, vector', zip(
    position_constructors,
    vector_constructors
))
def test_add_py(position, vector):
    p = position(1, 1)
    v = vector(1, 1)
    q = p + v
    assert q == position(2, 2)

    u = vector(-1, -1)
    r = p + u
    assert r == position(0, 0)

@pytest.mark.parametrize('position', position_constructors)
def test_path_py(position):
    p = position(1, 1)
    q = position(3, 3)
    path = Counter([position(2, 2), position(3, 3)])
    assert Counter(q.path_to(p)) == path

    r = position(1, 4)
    path = Counter([position(1, 2), position(1, 3), position(1, 4)])
    assert Counter(r.path_to(p)) == path

    s = position(4, 1)
    path = Counter([position(2, 1), position(3, 1), position(4, 1)])
    assert Counter(s.path_to(p)) == path

    t = position(2, 3)
    path = Counter([position(2, 3)])
    assert Counter(t.path_to(p)) == path

@pytest.mark.parametrize('position', position_constructors)
def test_hash_py(position):
    p = position(1, 1)
    #001001 = 9
    assert hash(p) == int(0b0001001)

@pytest.mark.parametrize('position', position_constructors)
def test_repr_py(position):
    p = position(1, 1)
    assert str(p) == "B2"

    q = position(7, 7)
    assert str(q) == "H8"

@pytest.mark.parametrize('position', position_constructors)
def test_consistency_py(position):
    p = position("A1")
    q = position(0, 0)
    assert p == q

def test_lpc_py_equality():
    p = position_constructors[0](0, 0)
    q = position_constructors[1](0, 0)
    assert p == q



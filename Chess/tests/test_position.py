from collections import Counter

from Chess.coordinate import Vec
from Chess.coordinate import Position as pypos
from libpychess import Position as cpppos

def test_init_py():
    p = pypos((0, 0))
    assert p.i == 0
    assert p.j == 0

def test_init_lpc():
    p = cpppos(0, 0)
    assert p.i == 0
    assert p.j == 0

def test_valid_py():
    p = pypos((0, 0))
    assert p.is_valid() == True

    q = pypos((-1, 0))
    assert q.is_valid() == False

    r = pypos((0, -1))
    assert r.is_valid() == False

    s = pypos((2, 8))
    assert s.is_valid() == False

    t = pypos((8, 2))
    assert t.is_valid() == False

def test_valid_lpc():
    p = cpppos((0, 0))
    assert p.is_valid() == True

    q = cpppos((-1, 0))
    assert q.is_valid() == False

    r = cpppos((0, -1))
    assert r.is_valid() == False

    s = cpppos((2, 8))
    assert s.is_valid() == False

    t = cpppos((8, 2))
    assert t.is_valid() == False

def test_add_py():
    p = pypos((1, 1))
    v = Vec(1, 1)
    q = p + v
    assert q == pypos((2, 2))

    u = Vec(-1, -1)
    r = p + u
    assert r == pypos((0, 0))

# Not supported adding python Vec to C++ position yet.
# def test_add_lpc():
#     p = cpppos((1, 1))
#     v = Vec(1, 1)
#     q = p + v
#     assert q == cpppos((2, 2))
# 
#     u = Vec(-1, -1)
#     r = p + u
#     assert r == cpppos((0, 0))

def test_path_py():
    p = pypos((1, 1))
    q = pypos((3, 3))
    path = Counter([pypos((2, 2)), pypos((3, 3))])
    assert Counter(q.path_to(p)) == path

    r = pypos((1, 4))
    path = Counter([pypos((1, 2)), pypos((1, 3)), pypos((1, 4))])
    assert Counter(r.path_to(p)) == path

    s = pypos((4, 1))
    path = Counter([pypos((2, 1)), pypos((3, 1)), pypos((4, 1))])
    assert Counter(s.path_to(p)) == path

    t = pypos((2, 3))
    path = Counter([pypos((2, 3))])
    assert Counter(t.path_to(p)) == path

def test_path_lpc():
    p = cpppos((1, 1))
    q = cpppos((3, 3))
    path = Counter([cpppos((2, 2)), cpppos((3, 3))])
    assert Counter(q.path_to(p)) == path

    r = cpppos((1, 4))
    path = Counter([cpppos((1, 2)), cpppos((1, 3)), cpppos((1, 4))])
    assert Counter(r.path_to(p)) == path

    s = cpppos((4, 1))
    path = Counter([cpppos((2, 1)), cpppos((3, 1)), cpppos((4, 1))])
    assert Counter(s.path_to(p)) == path

    t = cpppos((2, 3))
    path = Counter([cpppos((2, 3))])
    assert Counter(t.path_to(p)) == path

def test_hash_py():
    p = pypos((1, 1))
    #001001 = 9
    assert hash(p) == int(0b0001001)

def test_hash_lpc():
    p = cpppos((1, 1))
    #001001 = 9
    assert hash(p) == int(0b0001001)

def test_repr_py():
    p = pypos((1, 1))
    assert str(p) == "B2"

    q = pypos((7, 7))
    assert str(q) == "H8"

def test_repr_lpc():
    p = cpppos((1, 1))
    assert str(p) == "B2"

    q = cpppos((7, 7))
    assert str(q) == "H8"

def test_consistency_py():
    p = pypos("A1")
    q = pypos((0, 0))
    assert p == q

def test_consistency_lpc():
    p = cpppos("A1")
    q = cpppos((0, 0))
    r = cpppos(0, 0)
    assert p == q == r

def test_lpc_py_equality():
    p = pypos((0, 0))
    q = cpppos(0, 0)
    assert p == q


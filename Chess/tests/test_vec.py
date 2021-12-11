from Chess.coordinate import Vec

def test_init():
    v = Vec(1, 1)

def test_eq():
    v = Vec(1, 1)
    r = Vec(1, 1)
    assert v == r

def test_neq():
    v = Vec(1, 1)
    r = Vec(2, 1)
    assert v != r

    s = Vec(1, 2)
    assert v != s

    t = Vec(2, 2)
    assert v != t

def test_add():
    v = Vec(1, 1)
    r = Vec(-1, 1)
    x = v + r

    assert x == Vec(0, 2)

def test_sub():
    v = Vec(1, 1)
    r = Vec(1, 1)
    x = v - r
    assert x == Vec(0, 0)

def test_mul():
    v = Vec(1, 1)
    s = 5
    x = v * s
    
    assert x == Vec(5, 5)

import pytest
from itertools import product
from Chess.coordinate import Vec
from Chess.exceptions import InvalidVector

valid_vectors = [(0, 0), (1, 0), (5, 0), (0, 5), (1, 1), (-1, -1)]

@pytest.mark.parametrize("i,j", valid_vectors)
def test_vec_instantiation(i, j):
    Vec(i, j)

invalid_vectors = [(-10, -10), ("", ""), (1, None), (10, 10)]
@pytest.mark.parametrize("i,j", invalid_vectors)
def test_vec_invalid_instantiation(i, j):
    with pytest.raises(InvalidVector):
        Vec(i, j)

valid_sum_vectors = [(0, 0), (1, 0), (4, 4), (0, -4), (1, 1), (-1, -1)]

@pytest.mark.parametrize("i,j", valid_sum_vectors)
def test_vec_add(i, j):
    v1 = Vec(i, j)
    v2 = Vec(i, j)

    sum_i = 2 * i
    sum_j = 2 * j
    sum_v = v1 + v2

    assert sum_v.i == sum_i
    assert sum_v.j == sum_j

@pytest.mark.parametrize("i,j", valid_sum_vectors)
def test_vec_sub(i, j):
    v1 = Vec(i, j)
    v2 = Vec(i, j)

    sum_i = 0
    sum_j = 0
    sum_v = v1 - v2

    assert sum_v.i == sum_i
    assert sum_v.j == sum_j

def test_vec_add_1():
    assert Vec(1, 1) + Vec(2, 1) == Vec(3, 2)

def test_vec_sub_1():
    assert Vec(1, 1) - Vec(2, 1) == Vec(-1, 0)


vec = [(0, 0), (1, 0), (-1, 1), (2, 0)]
scalar = [1, 2, 3, -1, -2]

@pytest.mark.parametrize("vec,scalar", product(vec, scalar))
def test_vec_mul(vec, scalar):
    vec_product = Vec(*vec) * scalar
    i_component = scalar * vec[0]
    j_component = scalar * vec[1]
    assert vec_product == Vec(i_component, j_component)

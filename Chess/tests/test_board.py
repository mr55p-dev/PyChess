from Chess.coordinate import Position
from Chess.exceptions import InvalidFormat
from Chess.constants import CART_COORD
import pytest
from itertools import product

ALL_CART_COORD = list(product(CART_COORD, CART_COORD))

@pytest.mark.parametrize("rank,file",
                        [(1, "A"),
                         (1, "H"),
                         (8, "A"),
                         (8, "H")])
def test_pos_init_algebraic(rank, file):
    Position(rank=rank, file=file)

@pytest.mark.parametrize("rank,file",
                         [(1, "a"),
                          (1, " "),
                          ("a", "A"),
                          ("z", "A"),
                          (-1, "A"),
                          (1, ""),
                          (1, None),
                          (1, "I")])
def test_pos_init_algebraic_fail(rank, file):
    with pytest.raises(InvalidFormat):
        Position(rank=rank, file=file)

@pytest.mark.parametrize("rank,file", ALL_CART_COORD)
def test_pos_init_cart(rank, file):
    Position(rank=rank, file=file)

@pytest.mark.parametrize("rank,file",
                         [(-1, 2),
                          (8, 2),
                          ("hello", 2),
                          (0, -1),
                          (2, 8),
                          (3, 100),
                          (4, "None"),
                          (None, 2)])
def test_pos_init_cart_fail(rank, file):
    with pytest.raises(InvalidFormat):
        Position(rank=rank, file=file)

@pytest.mark.parametrize("rank,file",
                        [(1, "A"),
                         (1, "H"),
                         (8, "A"),
                         (8, "H")])
def test_pos_algebraic(rank, file):
    v = Position(rank, file)
    assert v.algebraic == file + str(rank)

@pytest.mark.parametrize("rank, file", ALL_CART_COORD)
def test_pos_cart(rank, file):
    v = Position(rank, file)
    assert v.cartesian == (rank, file)

            


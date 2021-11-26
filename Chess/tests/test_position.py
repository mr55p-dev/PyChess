from Chess.coordinate import Position, Vec
from Chess.exceptions import InvalidFormat, InvalidVector
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
    Position(f"{file}{rank}")

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
        Position(f"{file}{rank}")

@pytest.mark.parametrize("rank,file", ALL_CART_COORD)
def test_pos_init_cart(rank, file):
        Position((rank, file))

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
        Position((rank, file))

@pytest.mark.parametrize("rank,file",
                        [(1, "A"),
                         (1, "H"),
                         (8, "A"),
                         (8, "H")])
def test_pos_algebraic(rank, file):
    v = Position(f"{file}{rank}")
    assert v.algebraic == file + str(rank)

@pytest.mark.parametrize("rank, file", ALL_CART_COORD)
def test_pos_cart(rank, file):
    v = Position((rank, file))
    assert v.grid == (rank, file)


@pytest.mark.parametrize("rank, file", ALL_CART_COORD)
def test_pos_equality(rank, file):
    position1 = Position((rank, file))
    position2 = Position((rank, file))
    assert position1 == position2

@pytest.mark.parametrize("rank, file", ALL_CART_COORD[1:])
def test_pos_inequality(rank, file):
    position1 = Position((0,0))
    position2 = Position((rank, file))
    assert position2 != position1

    
valid_vec = [(-1,-1), (0, 0), (1, 1), (0, 1), (-1, 0)]
valid_pos = [(4, 4)]

# @pytest.mark.parametrize("board,vec", product(valid_pos, valid_vec))
# def test_pos_vec_add_valid(board, vec):
#     init_pos = Position(board)
#     step_vec = Vec(vec[0], vec[1])
# 
#     new_i = board[0] + vec[0]
#     new_j = board[1] + vec[1]
#     new_pos = Position((new_i, new_j))
#     assert new_pos == init_pos + step_vec
# 
# 
# invalid_vec = [(-1,1), (-1, 2), (1, 1)]
# invalid_pos = [(0, 7)]
# 
# @pytest.mark.parametrize("board,vec", product(invalid_pos, invalid_vec))
# def test_pos_vec_add_invalid(board, vec):
#     init_pos = Position(board)
#     step_vec = Vec(vec[0], vec[1])
#     with pytest.raises(InvalidFormat):
#         final_pos = init_pos + step_vec
# 
# p1s = [(0, 0), (1, 0), (0, 1)]
# p2s = [(2, 2), (2, 0), (5, 0)]
# ans = [[(

# @pytest.mark.parametrize("p1,p2,ans", zip(p1s,p2s,ans))
# def test_pos_pos_sub(p1, p2):
#     start = Position(p1)
#     end = Position(p2)
#     result = end - start






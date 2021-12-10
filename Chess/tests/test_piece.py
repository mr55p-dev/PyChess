import pytest
from Chess.constants import PIECE_TYPES, WHITE, BLACK
from Chess.pieces import Piece, King, Queen, Knight, Rook, Bishop, Pawn
from itertools import product

try:
    from libpychess import Position
except ImportError:
    from Chess.coordinate import Position

colours = [WHITE, BLACK]

@pytest.mark.parametrize("colour,kind", product(colours, PIECE_TYPES))
def test_base_piece(colour, kind):
    piece = Piece(colour, Position((0, 0)), kind)

    # assert str(piece) == kind
    assert piece.colour == colour
    assert piece.active == True

    piece.capture()

    assert piece.active == False

@pytest.mark.parametrize("colour", colours)
def test_king(colour):
    piece = King(colour, Position((0, 0)))

    assert piece.kind == "K"
    # assert str(piece) == "K"
    assert piece.active == True


@pytest.mark.parametrize("colour", colours)
def test_queen(colour):
    piece = Queen(colour, Position((0, 0)))

    assert piece.kind == "Q"
    # assert str(piece) == "Q"
    assert piece.active == True


@pytest.mark.parametrize("colour", colours)
def test_rook(colour):
    piece = Rook(colour, Position((0, 0)))

    assert piece.kind == "R"
    # assert str(piece) == "R"
    assert piece.active == True


@pytest.mark.parametrize("colour", colours)
def test_bishop(colour):
    piece = Bishop(colour, Position((0, 0)))

    assert piece.kind == "B"
    # assert str(piece) == "B"
    assert piece.active == True


@pytest.mark.parametrize("colour", colours)
def test_knight(colour):
    piece = Knight(colour, Position((0, 0)))

    assert piece.kind == "N"
    # assert str(piece) == "N"
    assert piece.active == True


@pytest.mark.parametrize("colour", colours)
def test_pawn(colour):
    piece = Pawn(colour, Position((0, 0)))

    assert piece.kind == "P"
    # assert str(piece) == "P"
    assert piece.active == True



from Chess.coordinate import Vec
from Chess.pieces import King, Queen, Rook, Knight, Bishop, Pawn
from Chess.constants import WHITE, BLACK

def new_game():
    # Change to FEN strings at some point
    # construct white:
    white_pieces = {
        Vec(0,0): Rook(colour=WHITE),
        Vec(0,1): Knight(colour=WHITE),
        Vec(0,2): Bishop(colour=WHITE),
        Vec(0,3): Queen(colour=WHITE),
        Vec(0,4): King(colour=WHITE),
        Vec(0,5): Bishop(colour=WHITE),
        Vec(0,6): Knight(colour=WHITE),
        Vec(0,7): Rook(colour=WHITE),
        Vec(1,0): Pawn(colour=WHITE),
        Vec(1,1): Pawn(colour=WHITE),
        Vec(1,2): Pawn(colour=WHITE),
        Vec(1,3): Pawn(colour=WHITE),
        Vec(1,4): Pawn(colour=WHITE),
        Vec(1,5): Pawn(colour=WHITE),
        Vec(1,6): Pawn(colour=WHITE),
        Vec(1,7): Pawn(colour=WHITE),
    }

    black_pieces = {
        Vec(7,0): Rook(colour=BLACK),
        Vec(7,1): Bishop(colour=BLACK),
        Vec(7,2): Knight(colour=BLACK),
        Vec(7,3): Queen(colour=BLACK),
        Vec(7,4): King(colour=BLACK),
        Vec(7,5): Bishop(colour=BLACK),
        Vec(7,6): Knight(colour=BLACK),
        Vec(7,7): Rook(colour=BLACK),
        Vec(6,0): Pawn(colour=BLACK),
        Vec(6,1): Pawn(colour=BLACK),
        Vec(6,2): Pawn(colour=BLACK),
        Vec(6,3): Pawn(colour=BLACK),
        Vec(6,4): Pawn(colour=BLACK),
        Vec(6,5): Pawn(colour=BLACK),
        Vec(6,6): Pawn(colour=BLACK),
        Vec(6,7): Pawn(colour=BLACK),
    }

    return (white_pieces, black_pieces)


from Chess.coordinate import Position
from Chess.pieces import King, Queen, Rook, Knight, Bishop, Pawn
from Chess.constants import WHITE, BLACK

def new_game():
    # Change to FEN strings at some point
    # construct white:
    white_pieces = [
        Rook(colour=WHITE, position=Position((0,0))),
        Knight(colour=WHITE, position=Position((0,1))),
        Bishop(colour=WHITE, position=Position((0,2))),
        Queen(colour=WHITE, position=Position((0,3))),
        King(colour=WHITE, position=Position((0,4))),
        Bishop(colour=WHITE, position=Position((0,5))),
        Knight(colour=WHITE, position=Position((0,6))),
        Rook(colour=WHITE, position=Position((0,7))),
        Pawn(colour=WHITE, position=Position((1,0))),
        Pawn(colour=WHITE, position=Position((1,1))),
        Pawn(colour=WHITE, position=Position((1,2))),
        Pawn(colour=WHITE, position=Position((1,3))),
        Pawn(colour=WHITE, position=Position((1,4))),
        Pawn(colour=WHITE, position=Position((1,5))),
        Pawn(colour=WHITE, position=Position((1,6))),
        Pawn(colour=WHITE, position=Position((1,7))),
    ]

    black_pieces = [
        Rook(colour=BLACK, position=Position((7,0))),
        Bishop(colour=BLACK, position=Position((7,1))),
        Knight(colour=BLACK, position=Position((7,2))),
        Queen(colour=BLACK, position=Position((7,3))),
        King(colour=BLACK, position=Position((7,4))),
        Bishop(colour=BLACK, position=Position((7,5))),
        Knight(colour=BLACK, position=Position((7,6))),
        Rook(colour=BLACK, position=Position((7,7))),
        Pawn(colour=BLACK, position=Position((6,0))),
        Pawn(colour=BLACK, position=Position((6,1))),
        Pawn(colour=BLACK, position=Position((6,2))),
        Pawn(colour=BLACK, position=Position((6,3))),
        Pawn(colour=BLACK, position=Position((6,4))),
        Pawn(colour=BLACK, position=Position((6,5))),
        Pawn(colour=BLACK, position=Position((6,6))),
        Pawn(colour=BLACK, position=Position((6,7))),
    ]

    return (white_pieces, black_pieces)


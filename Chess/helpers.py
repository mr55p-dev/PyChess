from Chess.coordinate import Position
from Chess.pieces import King, Queen, Rook, Knight, Bishop, Pawn
from Chess.constants import PIECE_TYPES, WHITE, BLACK

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

def create_piece(kind, colour, index):
    position = Position(index)
    if kind == "K":
        return King(colour=colour, position=position)
    elif kind == "Q":
        return Queen(colour=colour, position=position)
    elif kind == "R":
        return Rook(colour=colour, position=position)
    elif kind == "N":
        return Knight(colour=colour, position=position)
    elif kind == "B":
        return Bishop(colour=colour, position=position)
    elif kind == "P":
        return Pawn(colour=colour, position=position)

def pieces_from_fen(fen_string: str):
    fields = fen_string.split(' ')
    if len(fields) != 6: raise ValueError("A FEN string must be space delimited with 6 arguments")
    
    placement = fields[0]
    ranks = placement.split("/")
    # The ranks are given in reverse order, so index 0
    # of this corresponds to i=7, or the 8th rank.
    white_pieces = []
    black_pieces = []
    for rank, squares in enumerate(ranks):
        i = 7 - rank
        # Split the rank into its characters, 
        encoding = list(squares)
        j = 0
        for char in encoding:
            if char.isdigit():
                j += int(char)
                continue
            elif char in PIECE_TYPES:
                white_pieces.append(create_piece(char, WHITE, (i, j)))
            else:
                black_pieces.append(create_piece(char.upper(), BLACK, (i, j)))
            
            if j < 8:
                j += 1
            else:
                break

    # Decode the next turn
    next_turn = WHITE if fields[1] == 'w' else BLACK

    # Castling information
    castle = fields[2]

    # Valid enpassant moves
    en_passant = fields[3]

    # Halfmove clock 2 x moves since last pawn move or capture
    half_moves = fields[4]

    # Number of moves
    n_moves = fields[5]

    return [(white_pieces, black_pieces), next_turn]


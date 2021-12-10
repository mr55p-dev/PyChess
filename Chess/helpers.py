import re
from typing import List
from Chess.coordinate import Move
from Chess.pieces import King, Queen, Rook, Knight, Bishop, Pawn
from Chess.constants import PIECE_TYPES, WHITE, BLACK

try:
    from libpychess import Position
except ImportError:
    from Chess.coordinate import Position

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
        Knight(colour=BLACK, position=Position((7,1))),
        Bishop(colour=BLACK, position=Position((7,2))),
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
    """pieces_from_fen.
    Returns list containing:
        (white_pieces, black_pieces)
        next_turn
        castle
        en_passant
        half_moves
        n_moves
    :param fen_string:
    :type fen_string: str
    """
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
    half_moves = int(fields[4])

    # Number of moves
    n_moves = int(fields[5])

    return [(white_pieces, black_pieces), next_turn, castle, en_passant, half_moves, n_moves]

def parse_match(move_repr: List[str]):
    if move_repr[0] == '':
        piece = 'P'
    else:
        piece = move_repr[0]

    start = move_repr[1]
    if len(start) == 2:
        ## ALG_POS
        start = Position(start.upper())

    if move_repr[2] == '':
        takes = False
    else:
        takes = True

    if move_repr[3] == '': raise ValueError("No destination supplied")
    ## ALG_POS
    end = Position(move_repr[3].upper())

    return (start, end, piece, takes)

def lookup_move(board, start, end, piece, takes):
    moves = board.allied_moves

    # Rewrite with result set.
    # Filter out only the pieces of correct kind.
    filt = {board_piece: move for board_piece, move in moves.items() if board_piece.kind == piece}
    target = "captures" if takes else "passive"

    # Select only pieces which have the destination in either their "passive" or "captures"
    # list (dependent on if takes).
    candidates = [piece for piece, movelist in filt.items() if end in movelist[target]]

    if len(candidates) == 0: raise ValueError(f"Piece moving to {end} could not be found")
    elif len(candidates) > 1:
        # Hacky way to check if the file is the same
        if start:
            candidates = [i for i in candidates if str(board.piece_map[i])[0] == start.upper()]
        if len(candidates) != 1:
            raise ValueError(f"Multiple pieces may move to {end}: {candidates}.")
    
    return board.piece_map[candidates[0]]

def move_from_str(move_str: str, board):
    pattern = r'([KQRNB])?([a-h]\d?)?(x)?([a-z]\d)$'
    matches = re.findall(pattern, move_str)
    print(matches)

    if not matches: raise ValueError("A valid move could not be found")
    move_repr = matches[0]
    
    start, end, piece, takes = parse_match(move_repr)
    if not isinstance(start, Position): start = lookup_move(board, start, end, piece, takes)

    return Move(start, end, takes)
    

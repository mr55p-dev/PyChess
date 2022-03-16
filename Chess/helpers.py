from Chess.coordinate import PositionFactory
from Chess.constants import PIECE_TYPES, WHITE, BLACK
from Chess.pieces import PieceFactory

Position = PositionFactory().get_position()
Pieces = PieceFactory()

def new_game():
    return ([
        Pieces.get_piece("R")(WHITE, Position(0,0)),
        Pieces.get_piece("N")(WHITE, Position(0,1)),
        Pieces.get_piece("B")(WHITE, Position(0,2)),
        Pieces.get_piece("Q")(WHITE, Position(0,3)),
        Pieces.get_piece("K")(WHITE, Position(0,4)),
        Pieces.get_piece("B")(WHITE, Position(0,5)),
        Pieces.get_piece("N")(WHITE, Position(0,6)),
        Pieces.get_piece("R")(WHITE, Position(0,7)),
        Pieces.get_piece("P")(WHITE, Position(1,0)),
        Pieces.get_piece("P")(WHITE, Position(1,1)),
        Pieces.get_piece("P")(WHITE, Position(1,2)),
        Pieces.get_piece("P")(WHITE, Position(1,3)),
        Pieces.get_piece("P")(WHITE, Position(1,4)),
        Pieces.get_piece("P")(WHITE, Position(1,5)),
        Pieces.get_piece("P")(WHITE, Position(1,6)),
        Pieces.get_piece("P")(WHITE, Position(1,7)),
    ], [
        Pieces.get_piece("R")(BLACK, Position(7,0)),
        Pieces.get_piece("N")(BLACK, Position(7,1)),
        Pieces.get_piece("B")(BLACK, Position(7,2)),
        Pieces.get_piece("Q")(BLACK, Position(7,3)),
        Pieces.get_piece("K")(BLACK, Position(7,4)),
        Pieces.get_piece("B")(BLACK, Position(7,5)),
        Pieces.get_piece("N")(BLACK, Position(7,6)),
        Pieces.get_piece("R")(BLACK, Position(7,7)),
        Pieces.get_piece("P")(BLACK, Position(6,0)),
        Pieces.get_piece("P")(BLACK, Position(6,1)),
        Pieces.get_piece("P")(BLACK, Position(6,2)),
        Pieces.get_piece("P")(BLACK, Position(6,3)),
        Pieces.get_piece("P")(BLACK, Position(6,4)),
        Pieces.get_piece("P")(BLACK, Position(6,5)),
        Pieces.get_piece("P")(BLACK, Position(6,6)),
        Pieces.get_piece("P")(BLACK, Position(6,7)),
    ])



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
            elif char in PIECE_TYPES: # White pieces in upper case
                white_pieces.append(
                    Pieces.get_piece(char.upper())(WHITE, Position(i, j))
                )
            else: # Black pieces in lower case
                black_pieces.append(
                    Pieces.get_piece(char.upper())(BLACK, Position(i, j))
                )

            if j < 8:
                j += 1
            else:
                break

    # Decode the next turn
    next_turn = WHITE if fields[1] == 'w' else BLACK
    # Castling informataion
    castle = fields[2]
    # Valid enpassant moves
    en_passant = fields[3]
    # Halfmove clock 2 x moves since last pawn move or capture
    half_moves = int(fields[4])
    # Number of moves
    n_moves = int(fields[5])

    return [(white_pieces, black_pieces), next_turn, castle, en_passant, half_moves, n_moves]
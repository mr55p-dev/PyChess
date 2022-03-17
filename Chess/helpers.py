from Chess.constants import PIECE_TYPES, WHITE, BLACK
from Chess import types

class NewGame():

    def __init__(self, use_acceleration):
        if use_acceleration:
            from libpychess import Position, WHITE, BLACK, pieces
        else:
            from Chess.coordinate import Position
            from Chess.constants import WHITE, BLACK
            from Chess import pieces

        self.Position: types.Position = Position
        self.Pieces = pieces
        self.WHITE: int = WHITE
        self.BLACK: int = BLACK
        self.mapping = {
            "R": self.Pieces.Rook,
            "B": self.Pieces.Bishop,
            "N": self.Pieces.Knight,
            "P": self.Pieces.Pawn,
            "Q": self.Pieces.Queen,
            "K": self.Pieces.King,
        }

    def new_game(self):
        return ([
            self.Pieces.Rook(self.WHITE, self.Position(0,0)),
            self.Pieces.Knight(self.WHITE, self.Position(0,1)),
            self.Pieces.Bishop(self.WHITE, self.Position(0,2)),
            self.Pieces.Queen(self.WHITE, self.Position(0,3)),
            self.Pieces.King(self.WHITE, self.Position(0,4)),
            self.Pieces.Bishop(self.WHITE, self.Position(0,5)),
            self.Pieces.Knight(self.WHITE, self.Position(0,6)),
            self.Pieces.Rook(self.WHITE, self.Position(0,7)),
            self.Pieces.Pawn(self.WHITE, self.Position(1,0)),
            self.Pieces.Pawn(self.WHITE, self.Position(1,1)),
            self.Pieces.Pawn(self.WHITE, self.Position(1,2)),
            self.Pieces.Pawn(self.WHITE, self.Position(1,3)),
            self.Pieces.Pawn(self.WHITE, self.Position(1,4)),
            self.Pieces.Pawn(self.WHITE, self.Position(1,5)),
            self.Pieces.Pawn(self.WHITE, self.Position(1,6)),
            self.Pieces.Pawn(self.WHITE, self.Position(1,7)),
        ], [
            self.Pieces.Rook(self.BLACK, self.Position(7,0)),
            self.Pieces.Knight(self.BLACK, self.Position(7,1)),
            self.Pieces.Bishop(self.BLACK, self.Position(7,2)),
            self.Pieces.Queen(self.BLACK, self.Position(7,3)),
            self.Pieces.King(self.BLACK, self.Position(7,4)),
            self.Pieces.Bishop(self.BLACK, self.Position(7,5)),
            self.Pieces.Knight(self.BLACK, self.Position(7,6)),
            self.Pieces.Rook(self.BLACK, self.Position(7,7)),
            self.Pieces.Pawn(self.BLACK, self.Position(6,0)),
            self.Pieces.Pawn(self.BLACK, self.Position(6,1)),
            self.Pieces.Pawn(self.BLACK, self.Position(6,2)),
            self.Pieces.Pawn(self.BLACK, self.Position(6,3)),
            self.Pieces.Pawn(self.BLACK, self.Position(6,4)),
            self.Pieces.Pawn(self.BLACK, self.Position(6,5)),
            self.Pieces.Pawn(self.BLACK, self.Position(6,6)),
            self.Pieces.Pawn(self.BLACK, self.Position(6,7)),
        ])

    def pieces_from_fen(self, fen_string: str):
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
                        self.mapping[char.upper()](self.WHITE, self.Position(i, j))
                    )
                else: # Black pieces in lower case
                    black_pieces.append(
                        self.mapping[char.upper()](self.BLACK, self.Position(i, j))
                    )

                if j < 8:
                    j += 1
                else:
                    break

        # Decode the next turn
        next_turn = int(self.WHITE) if fields[1] == 'w' else int(self.BLACK)
        # Castling informataion
        castle = fields[2]
        # Valid enpassant moves
        en_passant = fields[3]
        # Halfmove clock 2 x moves since last pawn move or capture
        half_moves = int(fields[4])
        # Number of moves
        n_moves = int(fields[5])

        return [(white_pieces, black_pieces), next_turn, castle, en_passant, half_moves, n_moves]
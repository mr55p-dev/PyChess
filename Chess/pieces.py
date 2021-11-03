from Chess.constants import WHITE, BLACK
from Chess.coordinate import Position

class Piece:
    """
	:param colour: 			White|Black
	:param type: 			King|Queen|Rook|Bishop|Knight|Pawn
	:param position: 		ChessVec
							A vector containing piece position
	:method move: 			updates position
	:attr value: 			int
							The value of the piece (based on kind)
    """
    
    def __init__(
            self,
            colour: WHITE|BLACK,
            position: Position
        ) -> None:
        self.colour = colour
        self.position = position



class King(Piece):
    pass


class Queen(Piece):
    pass


class Rook(Piece):
    pass


class Bishop(Piece):
    pass


class Knight(Piece):
    pass


class Pawn(Piece):
    pass

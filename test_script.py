from Chess.constants import BLACK, PIECE_TYPES, WHITE
from Chess.helpers import pieces_from_fen
from Chess.pieces import Bishop, King, Knight, Pawn, Piece, Queen, Rook 
from Chess.state import Board
from Chess.coordinate import Position, Vec
from Chess.view import view_board

if __name__ == "__main__":
    # Old checking.
    fen = input("FEN string >>> ")
    pieces, to_move = pieces_from_fen(fen)
    board = Board(pieces, to_move)
    while True:
        view_board(board)
        t = input("Enter a square to see positions: ")
        visualise = Position(t)
        vp = board.map[visualise]
        view_board(board, show_moves=vp)
        input()



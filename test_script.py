from Chess.constants import BLACK, PIECE_TYPES, WHITE
from Chess.helpers import pieces_from_fen
from Chess.pieces import Bishop, King, Knight, Pawn, Piece, Queen, Rook 
from Chess.state import Board
from Chess.coordinate import Position, Vec
from Chess.view import view_board

if __name__ == "__main__":
    # Old checking.
    fen = input("FEN string >>> ")
    if not fen:
        fen = "r2qk2r/ppp2ppp/5n2/3p1b2/3b1B2/2NN4/PP2PPPP/n1KQ1B1R w kq - 4 11"
    params = pieces_from_fen(fen)
    pieces, to_move, _, _, _, turn = pieces_from_fen(fen)
    board = Board(pieces, turn, to_move, params[2:5])
    while True:
        view_board(board)
        print(f"This position is check: {board.is_check}")
        t = input("Enter a square to see positions: ")
        visualise = Position(t)
        vp = board._loc_map[visualise]
        view_board(board, show_moves=vp)
        print(f"FEN: {board.to_fen()}")
        input()



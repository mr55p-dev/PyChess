from Chess.constants import BLACK, PIECE_TYPES, WHITE
from Chess.helpers import pieces_from_fen
from Chess.__main__ import construct_board
from Chess.pieces import Bishop, King, Knight, Pawn, Piece, Queen, Rook 
from Chess.state import Board
from Chess.coordinate import Position, Vec
from Chess.view import view_board

if __name__ == "__main__":

    board = construct_board("r1bqkbnr/p3pppp/1pP5/3p4/8/8/PPPQPPPP/RN2KBNR b KQkq - 0 11")

    print(f"This position is check: {board.is_check}")
    print(f"This position is stalemate: {board.is_stale}")
    print(f"This position is mate: {board.is_mate}")
    while True:
        view_board(board)
        t = input("Enter a square to see positions: ")
        visualise = Position(t)
        vp = board.loc_map[visualise]
        print(board.get_moves(vp))
        view_board(board, show_moves=vp)
        print(f"FEN: {board.to_fen()}")
        input()



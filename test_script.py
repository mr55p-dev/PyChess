from Chess.constants import BLACK
from Chess.pieces import Pawn
from Chess.state import Board
from Chess.coordinate import Position, Vec
from Chess.view import view_board

if __name__ == "__main__":
    board = Board()
    board._black.append(Pawn(BLACK, Position("A3")))
    board._update_map()
    view_board(board)
    queens_knight = board.map[Position("B1")]
    moves = board._find_piece_moves(queens_knight)
    print(moves)

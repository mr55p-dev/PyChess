from Chess.helpers import pieces_from_fen
from Chess.state import Board  # type: ignore
from Chess.view import view_board  # type: ignore
from Chess.coordinate import Vec # type: ignore

def construct_board(fen):
    params = pieces_from_fen(fen)
    board = Board(params[0], params[1], params[5])
    return board

if __name__ == "__main__":
    # A new game loop
    #crent_state = board setup
    # while state is not (checkmate or resigned):
    #     if current_state.is_check?
    #         disp(check)
    #     valid moves = current_state.valid_moves
    #     best move = current_state.best_move
    #     disp(best move)
    #     input(>> move)
    #     move = Move
    #     if Move.is_valid?
    #     history.append(current_state)
    #     new_state = current_state.next(move) # make a new position collection
    #     turn ++

    test_board = Board()
    view_board(test_board)
    
    pass

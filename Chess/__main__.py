from .coordinate import *
from .state import *
from .pieces import Piece


if __name__ == "__main__":
    # A new game loop
    current_state = board setup
    while state is not (checkmate or resigned):
        if current_state.is_check?
            disp(check)
        valid moves = current_state.valid_moves
        best move = current_state.best_move
        disp(best move)
        input(>> move)
        move = Move
        if Move.is_valid?
        history.append(current_state)
        new_state = current_state.next(move) # make a new position collection
        turn ++
pass

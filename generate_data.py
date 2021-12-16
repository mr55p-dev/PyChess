"""I, Ellis Lunnon, have read and understood the School's Academic Integrity Policy, as well as guidance relating to this
module, and confirm that this submission complies with the policy. The content of this file is my own original work,
with any significant material copied or adapted from other sources clearly indicated and attributed."""

import os
import re
import pickle
from itertools import repeat
from re import Pattern
from typing import List
from Chess import state
from Chess.state import Board
from Chess.game import Game
from Chess.helpers import pieces_from_fen
from tqdm import tqdm
import logging, logging.handlers

gamelog = logging.getLogger("Game")
statelog = logging.getLogger("State")

handler = logging.handlers.WatchedFileHandler("logs/gen_data.log")
handler.setFormatter(logging.Formatter("%(asctime)-15s %(levelname)-8s %(name)s %(message)s"))
handler.setLevel(logging.DEBUG)

gamelog.setLevel(logging.DEBUG)
statelog.setLevel(logging.DEBUG)

gamelog.addHandler(handler)
statelog.addHandler(handler)


def read_pgn_file(filename: str):
    """ Open a file of type pgn and extract a 2d list of games -> moves in the standard algebraic notation"""
    with open(filename, 'r') as pgn_file:
        data = pgn_file.readlines()

    games = [i for i in data if i[0] == "1"]
    moves_expr = re.compile(r"([RNBQK])?([a-h]\d?)?x?([a-h]\d)(=[RNBQ])?|(O-O)(-O)?")
    # Breakdown of the regex: ([RNBQK])? matches an optional piece identifier (pawn if not present)
    # ([a-h]\d?)? optionally matches any letter a-h with a digit next to it or not.
    # x? optionally inculdes "x" in its own match group if present
    #([a-h]\d) matches the "destination" of the piece which must be present
    # (=[RNBQ])? includes matches for "promotions" ie c8=Q meaning the c pawn promotes to a queen.
    # |(O-O)(-O)? means also consider matching O-O and O-O-O which are the strings to represent castling. 
    return map(get_game_moves, games, repeat(moves_expr))

def get_game_moves(move_str: str, expr: Pattern):
    """Match using the compiled regex and return a list of the moves extracted"""
    return ["".join(i) for i in expr.findall(move_str)]

def get_random_boards(move_set):
    boards = list(map(get_board_fen, move_set))
    return boards

def get_board_fen(moves: List[str]) -> str:
    """Calculate the FEN string of a game after applying a sequence of moves"""
    # Instantiate a new game, and stop applying the moves so we do not end up with an imbalance
    # of checkmates
    game = Game()
    end = -12 if len(moves) > 20 else len(moves)
    moves = moves[:end]
    for move in moves:
        # If the move executor does not return True then the move failed,
        # this can happen due to :
        # - Existing bug in castling
        # - Piece promotion (not supported)
        # - Pawns doing en-passant (most frequent)
        # These things will be supported soon, for now we just break from the calculation
        # and keep the game in its last "good" state
        if not game.execute_move_str(move):
            break
    return game.peek.to_fen()

if __name__ == "__main__":
    # Create the games data if it does not exist
    pgn_input_path = "imported_games/lichess_db_standard_rated_2013-01.pgn"
    move_sequence_path = "generated_data/lichess_db_standard_rated_2013-01.pickle"
    games_output_csv_path = "generated_data/lichess_db_standard_rated_2013-01.txt"

    if not os.path.exists(move_sequence_path):
        games = read_pgn_file(pgn_input_path)
        with open(move_sequence_path, 'wb') as f:
            # convert games to a list to exhaust the map
            pickle.dump(list(games), f)
 
    # Load the set of moves back into memory (just quicker than using a CSV)
    with open(move_sequence_path, 'rb') as f:
        games = pickle.load(f)

    # Write the converted games into a txt file, newline delimeted.
    # Each "final position" is stored as a FEN string.
    with open(games_output_csv_path, 'w', newline='') as f:
        # Use tqdm to get a nice status bar
        for game in tqdm(games):
            fen = get_board_fen(game)
            f.write(fen + '\n')

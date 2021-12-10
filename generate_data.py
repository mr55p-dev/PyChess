import re
import pickle
from itertools import repeat
from re import Pattern
from typing import List
from Chess.state import Board
from Chess.game import Game
from Chess.helpers import pieces_from_fen
from tqdm import tqdm

def read_pgn_file(filename: str) -> List[str]:
    with open(filename, 'r') as pgn_file:
        data = pgn_file.readlines()

    games = [i for i in data if i[0] == "1"]
    moves_expr = re.compile(r"([RNBQK])?([a-h]\d?)?x?([a-h]\d)(=[RNBQ])?|(O-O)(-O)?")
    return map(get_game_moves, games, repeat(moves_expr))

def get_game_moves(move_str: str, expr: Pattern) -> List[str]:
    return ["".join(i) for i in expr.findall(move_str)]

def get_random_boards(move_set: List[str]) -> List[str]:
    boards = list(map(get_board_fen, move_set))
    return boards

def get_board_fen(moves: List[str]) -> str:
    game = Game()
    end = -20 if len(moves) > 12 else len(moves)
    moves = moves[:end]
    for move in moves:
        if not game.execute_move_str(move):
            break
    return game.peek.to_fen() 

def make_board(fen: str) -> Board:
    params = pieces_from_fen(fen)
    return Board(*params)

# games = read_pgn_file("./imported_games/lichess_db_standard_rated_2013-01.pgn")
# with open("./generated_data/games", 'wb') as f:
#     pickle.dump(list(games), f)
 
with open("./generated_data/games.pickle", 'rb') as f:
    games: List = pickle.load(f)

with open("./generated_data/all_boards.txt", 'w', newline='') as f:
    for game in tqdm(games):
        fen = get_board_fen(game)
        f.write(fen + '\n')

with open("./generated_data/all_boards.pickle", 'wb') as f:
    pickle.dump(fen_boards, f)

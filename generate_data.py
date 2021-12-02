import re
import pickle
from itertools import repeat
from re import Pattern
from typing import List
from random import randint
from Chess.__main__ import construct_board
from Chess.state import Board
from Chess.game import Game
from Chess.helpers import pieces_from_fen
from Chess.view import view_board_colour, view_board_mono

def read_pgn_file(filename: str) -> List[str]:
    with open(filename, 'r') as pgn_file:
        data = pgn_file.readlines()

    games = [i for i in data if i[0] == "1"]
    moves_expr = re.compile(r"([RNBQK])?([a-h]\d?)?x?([a-h]\d)(=[RNBQ])?|(O-O)(-O)?")
    return map(get_game_moves, games, repeat(moves_expr))

def get_game_moves(move_str: str, expr: Pattern) -> List[str]:
    return ["".join(i) for i in expr.findall(move_str)]

def get_random_boards(move_set: List[str]) -> List[Board]:
    boards = list(map(get_board_fen, move_set))
    return boards

def get_board_fen(moves: List[str]) -> Board:
    game = Game()
    end = -10 if len(moves) > 12 else len(moves)
    moves = moves[:end]
    for move in moves:
        if not game.execute_move_str(move):
            break
    fen = game.peek.to_fen()
    print(fen)
    return game.peek

def make_board(fen: str) -> Board:
    params = pieces_from_fen(fen)
    return Board(*params)

# games = read_pgn_file("./imported_games/lichess_db_standard_rated_2013-01.pgn")
# with open("./generated_data/games", 'wb') as f:
#     pickle.dump(list(games), f)
# 
with open("./generated_data/games", 'rb') as f:
    games: List = pickle.load(f)

games = games[:100]
fen_boards = list(get_random_boards(games))

with open("./generated_data/all_boards.pickle", 'wb') as f:
    pickle.dump(fen_boards, f)

with open("./generated_data/all_boards.pickle", 'rb') as f:
    boards = pickle.load(f)

for i in boards:
    print(i.to_fen())

from Chess.game import Game

import cProfile, pstats
from functools import wraps
import datetime
import pickle

def profile(output_file=None, sort_by='cumulative', strip_dirs=False):
    """A time profiler decorator.
    From https://towardsdatascience.com/how-to-profile-your-code-in-python-e70c834fad89
    Inspired by and modified the profile decorator of Giampaolo Rodola:
    http://code.activestate.com/recipes/577817-profile-decorator/
    """

    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            t = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
            _output_file = output_file or "profile_logs/" + func.__name__ + "-" + t + '.prof'
            pr = cProfile.Profile()
            pr.enable()
            retval = func(*args, **kwargs)
            pr.disable()
            pr.dump_stats(_output_file)

            ps = pstats.Stats(pr)
            if strip_dirs:
                ps.strip_dirs()
            if isinstance(sort_by, (tuple, list)):
                ps.sort_stats(*sort_by)
            else:
                ps.sort_stats(sort_by)
            ps.print_stats()

            return retval

        return wrapper

    return inner

@profile(sort_by=["cumulative", "ncalls"], strip_dirs=True)
def make_board(games):
    for game in games:
        g = Game()
        for move in game:
            g.execute_move_str(move)

with open("./generated_data/lichess_db_standard_rated_2013-01.pickle", "rb") as f:
    li = pickle.load(f)

games = li[:5]

make_board(games)

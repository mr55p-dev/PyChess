from typing import List, Tuple
from Chess.helpers import NewGame

from libpychess import MoveAnalyser, Position

from Chess.result import Result, ResultSet
from Chess.state import Board
from Chess import types

class CBoard(Board):
    def __init__(self, fen: str = None) -> None:
        ng = NewGame(True)
        self.new_game = ng.new_game
        params = ng.pieces_from_fen(fen) if fen else []
        self.Position: types.Position = Position
        super().__init__(*params)

    def _psuedolegal_moves(self, pieces: List[types.Piece]) -> ResultSet:
        """__psuedolegal_moves.
        Wraps function calls to convert and retrieve data from the libpychess module.

        :param self:
        :param pieces:
        :type pieces: List[Piece]
        :rtype: ResultSet
        """
        analysis = MoveAnalyser(pieces)
        colour_to_analyse = pieces[0].colour
        c_result = analysis.PsuedolegalMoves(colour_to_analyse)

        return ResultSet({
            k: Result(v) for k, v in c_result.items()
        })
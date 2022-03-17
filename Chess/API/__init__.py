from Chess import types

class BaseChess():
    def __init__(self, use_acceleration: bool):
        self.accelerated = use_acceleration
        if use_acceleration:
            from libpychess import Position, pieces, Vec, BLACK, WHITE
        else:
            from Chess.coordinate import Position, Vec
            from Chess.constants import BLACK, WHITE
            from Chess import pieces

        self.Position: types.Position  = Position
        self.Vec: types.Vec = Vec
        self.Pieces = pieces
        self.black = BLACK
        self.white = WHITE


class Chess(BaseChess):
    def __init__(self, use_acceleration: bool):
        super().__init__(use_acceleration)
        if self.accelerated:
            from Chess.cState import CBoard as Board
        else:
            from Chess.pState import PyBoard as Board

        self.Board = Board
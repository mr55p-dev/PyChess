class BaseChess():
    def __init__(self, use_acceleration: bool):

        self.accelerated = use_acceleration
        if use_acceleration:
            from libpychess import Position, pieces

        else:
            from Chess.coordinate import Position
            from Chess import pieces

        self.Position = Position
        self.Pieces = pieces



class Chess(BaseChess):
    def __init__(self, use_acceleration: bool):
        super().__init__(use_acceleration)
        if self.accelerated:
            from Chess.cState import CBoard as Board
        else:
            from Chess.pState import PyBoard as Board

        self.Board = Board
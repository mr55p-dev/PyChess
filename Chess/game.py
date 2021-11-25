import re
from typing import Callable, List, Optional
from Chess import Board
from Chess.coordinate import Move, Position


class Game():
    def __init__(self, view_callback: Optional[Callable]) -> None:
        self.__history: List[Board]
        pass

    def __parse_move_match(self, move_repr: List[str]):
        if move_repr[0] == '':
            piece = 'P'
        else:
            piece = move_repr[0]

        start = move_repr[1]
        if len(start) == 2:
            start = Position(start.upper())

        if move_repr[2] == '':
            takes = False
        else:
            takes = True

        if move_repr[3] == '': raise ValueError("No destination supplied")
        end = Position(move_repr[3].upper())

        return (start, end, piece, takes)

    def __parse_move(self, move_str: str) -> Move:
        pattern = r'([KQRNB])?([a-h]\d?)?(x)?([a-z]\d)$'
        matches = re.findall(pattern, move_str)
        print(matches)

        if not matches:
            raise ValueError("A valid move could not be found")
        move_repr = matches.pop()

        takes = False
        if move_repr[2]:
            takes = True

        if not move_repr[3]: raise ValueError("A valid move could not be found")
        end = Position(move_repr[3].upper())

        start = move_repr[1]
        if len(start) == 2:
            start = Position(start.upper())
        elif len(start) == 1:
            self.state: Board
            moves = self.state.allied_moves
            moves.by_kind_str(start.lower())
            moves.filter_all(lambda x: end in x)
            candidates = list(moves.keys())
            if not candidates:
                raise ValueError(f"Not enough information to move to {end}")
            elif len(candidates) > 1:
                # Hacky way to check the same file
                candidates = [i for i in candidates if str(self.state.piece_map[i])[0] == start.upper()]
                if not candidates or len(candidates) > 1:
                    raise ValueError(f"Multiple pieces may move to {end}")

        return Move(start, end, takes)


    def __parse_pgn(self, move) -> List[Move]:
        pass

    def execute_pgn(self, pgn) -> bool:
        pass

    def execute_move(self, move) -> bool:
        pass

    def show_board(self):
        pass

    def fetch_moves(self, piece):
        pass

    def next(self) -> None:
        pass

    def prev(self) -> None:
        pass

    def play(self):
        # Begin a game loop
        # while running: 
        #   # renderer
        #   view_callback(self.state)
        #   wait(input)
        #   # event handler
        #   self.execute_move(input)
        #   self.handle_signal(signal)
        pass

    @property
    def state(self) -> Board:
        pass

    @property
    def turn(self) -> int:
        pass

    @property
    def to_move(self) -> int:
        pass



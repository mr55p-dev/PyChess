import re
from typing import Callable, Optional
from Chess.state import Board
from Chess.coordinate import Move
from Chess.exceptions import MoveParseError
from Chess.constants import USE_CPP

try: 
    from libpychess import Position
except ImportError: 
    from Chess.coordinate import Position

class Game():
    def __init__(self,
                 view_callback: Optional[Callable] = None,
                 start_state: Board = None
                 ) -> None:
        self.__state: Optional[Board] = None
        self.__view_callback = view_callback

        if start_state: board = start_state
        else: board = Board()

        self.__state = board
        self.move_hist = [];

    def __check_termination(self) -> int:
        if self.peek.is_check:
            return 1
        elif self.peek.is_mate:
            return 0
        elif self.peek.is_stale:
            return 0
        else:
            return 1
    
    def __parse_castle(self, castle_type: str) -> Move:
        if castle_type == "long":
            long = True
        elif castle_type == "short":
            long = False
        else:
            raise ValueError("Matched for a castle but with no group contents")

        if self.peek.to_move:
            start_i = 0
            end_i = 0
        else:
            start_i = 7
            end_i = 7

        if long:
            start_j = 4
            end_j = 2
            castles = 'long'
        else:
            start_j = 4
            end_j = 6
            castles = 'short'

        start = Position((start_i, start_j))
        end = Position((end_i, end_j))
        takes = False

        return Move(start, end, takes, castles)

    def __parse_move(self, move_str: str) -> Move:
        pattern = r'([KQRNB])?([a-h]\d?)?(x)?([a-z]\d)|(O-O)(-O)?'
        matches = re.findall(pattern, move_str)

        if not matches:
            raise ValueError("Invalid move")
            
        move_repr = matches.pop()

        if move_repr[4] and move_repr[5]:
            return self.__parse_castle('long')
        elif move_repr[4] and not move_repr[5]:
            return self.__parse_castle('short')

        takes = False
        if move_repr[2]:
            takes = True

        if not move_repr[3]: raise MoveParseError("A valid move could not be found")
        end = Position(move_repr[3].upper())

        if end in self.peek.loc_map:
            takes = True

        start = move_repr[1]
        if len(start) == 2:
            ## ALG_POS
            start = Position(start.upper())
        else:
            piece = move_repr[0]
            if not piece: piece = "P"
            moves = self.peek.allied_moves
            moves_filt = moves.filter_all_by_value(lambda x: x == end)
            init_piece_candidates = [k for k in moves_filt if moves_filt[k].has_passive_or_capture]
            piece_candidates = [p for p in init_piece_candidates if p.kind == piece]

            if not piece_candidates:
                # Add logging here
                print("poo")
                return False 
                raise MoveParseError(f"Not enough information to move to {end}")
            elif len(piece_candidates) > 1:
                # Hacky way to check the same file
                piece_candidates = [i \
                              for i in piece_candidates \
                              if str(self.peek.piece_map[i])[0] == start.upper()
                            ]
                if not len(piece_candidates) == 1:
                    # Add logging
                    # return None
                    raise MoveParseError(f"Multiple pieces may move to {end}")
            start = self.peek.piece_map[piece_candidates.pop()]

        return Move(start, end, takes)

    def __move(self, move) -> bool:
        return self.peek.move(move)

    @property
    def peek(self) -> Board:
        if self.__state: 
            return self.__state
        else: 
            raise ValueError("No state to show")

    def execute_move(self, move: Move) -> bool:
        return self.__move(move)

    def execute_move_str(self, move_str: str) -> bool:
        self.move_hist.append(move_str)
        move = self.__parse_move(move_str)
        if not move: 
            print(f"Failed to parse move {move_str}")
            return False
        return self.__move(move)

    def show_board(self):
        if not isinstance(self.__view_callback, Callable):
            raise TypeError("view_callback must implement __call__")
        self.__view_callback(self.peek)

    def play(self):
        while self.__check_termination():
            self.show_board()
            worked = False
            while not worked:
                move = input("Please enter a move>> ")
                worked = self.execute_move_str(move)
                print(worked)


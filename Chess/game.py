from copy import copy
import re
from typing import Callable, List, Optional
from Chess import Board
from Chess.constants import BLACK, PIECE_TYPES, WHITE
from Chess.coordinate import Move, Position
from Chess.helpers import create_piece


class Game():
    def __init__(self,
                 view_callback: Optional[Callable],
                 start_state: str = ''
                 ) -> None:
        self.__history: List[Board] = []
        self.__future:  List[Board] = []
        self.__view_callback = view_callback

        if start_state: board = self.__parse_fen(start_state)
        else: board = Board()

        self.push(board)

    def __check_termination(self) -> int:
        if self.peek.is_check:
            return 0
        elif self.peek.is_mate:
            return 0
        elif self.peek.is_stale:
            return 0
        else:
            return 1

    @staticmethod
    def __parse_fen(fen_string: str) -> Board:
        fields = fen_string.split(' ')
        if len(fields) != 6: raise ValueError("A FEN string must be space delimited with 6 arguments")
        placement = fields[0]
        ranks = placement.split("/")
        # The ranks are given in reverse order, so index 0
        # of this corresponds to i=7, or the 8th rank.
        white_pieces = []
        black_pieces = []
        # Go through and decode each rank, skipping by the necessary amount of squares each time.
        for rank, squares in enumerate(ranks):
            i = 7 - rank
            encoding = list(squares)
            j = 0
            for char in encoding:
                if char.isdigit():
                    j += int(char)
                    continue
                elif char in PIECE_TYPES:
                    white_pieces.append(create_piece(char, WHITE, (i, j)))
                else:
                    black_pieces.append(create_piece(char.upper(), BLACK, (i, j)))

                if j < 8:
                    j += 1
                else:
                    break

        next_turn = WHITE if fields[1] == 'w' else BLACK # next player to move
        castle = fields[2] # Castling information
        en_passant = fields[3 ]# Valid enpassant moves
        half_moves = int(fields[4]) # Halfmove clock 2x moves since last pawn move or capture
        n_moves = int(fields[5]) # Number of full moves

        return Board((white_pieces, black_pieces), next_turn, half_moves, castle)

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
        else:
            moves = self.peek.allied_moves
            moves.filter_all_by_key(lambda x: x.kind == start.lower())
            moves.filter_all_by_value(lambda x: end in x)
            piece_candidates = list(moves.keys())

            if not piece_candidates:
                raise ValueError(f"Not enough information to move to {end}")
            elif len(piece_candidates) > 1:
                # Hacky way to check the same file
                piece_candidates = [i \
                              for i in piece_candidates \
                              if str(self.peek.piece_map[i])[0] == start.upper()]
                if not piece_candidates or len(piece_candidates) > 1:
                    raise ValueError(f"Multiple pieces may move to {end}")

        return Move(start, end, takes)

    def __move(self, move) -> bool:
        self.push(copy(self.peek))
        return self.peek.move(move)

    def __parse_pgn(self, move) -> List[Move]:
        pass

    @property
    def peek(self) -> Board:
        if self.__history: return self.__history[-1]
        else: raise ValueError("No history to show")

    def push(self, state: Board) -> None:
        self.__history.append(state)

    def pop(self) -> Board:
        if self.__history: return self.__history.pop()
        else: raise ValueError("No history to pop")

    def execute_pgn(self, pgn) -> bool:
        pass

    def execute_move(self, move: Move) -> bool:
        return self.__move(move)

    def execute_move_str(self, move_str: str) -> bool:
        move = self.__parse_move(move_str)
        return self.__move(move)

    def show_board(self):
        if not isinstance(self.__view_callback, Callable):
            raise TypeError("view_callback must implement __call__")
        self.__view_callback(self.peek)

    def fetch_moves(self, piece):
        pass

    def next(self) -> None:
        pass

    def prev(self) -> None:
        pass

    def play(self):
        while self.__check_termination():
            self.show_board()
            move = input("Please enter a move>> ")
            self.execute_move_str(move)
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



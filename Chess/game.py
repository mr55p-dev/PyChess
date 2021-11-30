from copy import copy
import re
from typing import Callable, List, Optional
from Chess import Board
from Chess.constants import BLACK, PIECE_TYPES, WHITE
from Chess.coordinate import Move, Position
from Chess.exceptions import MoveParseError
from Chess.helpers import create_piece


class Game():
    def __init__(self,
                 view_callback: Optional[Callable],
                 start_state: Board = None
                 ) -> None:
        self.__history: List[Board] = []
        self.__future:  List[Board] = []
        self.__view_callback = view_callback

        if start_state: board = start_state 
        else: board = Board()

        self.push(board)

    def __check_termination(self) -> int:
        if self.peek.is_check:
            print("CHECK")
            return 1
        elif self.peek.is_mate:
            print("MATE")
            return 0
        elif self.peek.is_stale:
            print("STALEMATE")
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
        en_passant = fields[3 ] # Valid enpassant moves
        half_moves = int(fields[4]) # Halfmove clock 2x moves since last pawn move or capture
        n_moves = int(fields[5]) # Number of full moves

        return Board((white_pieces, black_pieces), next_turn, half_moves, castle)

    def __parse_castle(self, move_str: str) -> Optional[Move]:
        pattern = r'^(O-O)(-O)?$'
        matches = re.findall(pattern, move_str)
        if not matches:
            return None
        match = matches.pop()
        if match[0] and match[1]:
            long = True
        elif match[0] and not match[1]:
            long = False
        else:
            print("Matched for a castle but with no group contents")
            return None

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
        pattern = r'([KQRNB])?([a-h]\d?)?(x)?([a-z]\d)$'
        matches = re.findall(pattern, move_str)

        if not matches:
            castle = self.__parse_castle(move_str) 
            if not castle:
                raise MoveParseError("A valid move could not be found")
            
            return castle
            
        move_repr = matches.pop()

        takes = False
        if move_repr[2]:
            takes = True

        if not move_repr[3]: raise MoveParseError("A valid move could not be found")
        end = Position(move_repr[3].upper())

        start = move_repr[1]
        if len(start) == 2:
            start = Position(start.upper())
        else:
            piece = move_repr[0]
            if not piece: piece = "P"
            moves = self.peek.allied_moves
            moves = moves.filter_all_by_value(lambda x: x == end)
            piece_candidates = [k for k in moves if moves[k].has_passive_or_capture]
            if piece: piece_candidates = [p for p in piece_candidates if p.kind == piece]

            if not piece_candidates:
                raise MoveParseError(f"Not enough information to move to {end}")
            elif len(piece_candidates) > 1:
                # Hacky way to check the same file
                piece_candidates = [i \
                              for i in piece_candidates \
                              if str(self.peek.piece_map[i])[0] == start.upper()
                            ]
                if not len(piece_candidates) == 1:
                    raise MoveParseError(f"Multiple pieces may move to {end}")
            start = self.peek.piece_map[piece_candidates.pop()]

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
        try: move = self.__parse_move(move_str)
        except MoveParseError as e:
            print(e)
            return False
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
            worked = False
            while not worked:
                move = input("Please enter a move>> ")
                worked = self.execute_move_str(move)
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



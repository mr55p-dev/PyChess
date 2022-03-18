import re
from typing import Callable, Optional
from Chess.state import Board
from Chess.coordinate import Move, PositionFactory
import logging, logging.handlers

Position = PositionFactory().get_position()

class Game():
    """Game
    Wrapper for Board which tracks the changes applied to state over time and implements a very
    basic game loop."""

    def __init__(self,
                 view_callback: Optional[Callable] = None,
                 start_state: Board = None
                 ) -> None:
        self.log = logging.getLogger("Game")
        self.__state: Optional[Board] = None
        self.__view_callback = view_callback

        board = start_state or Board()
        self.__state = board
        self.move_hist = [];

    def __check_termination(self) -> int:
        """__check_termination.
        Check if the game has ended

        :param self:
        :rtype: int
        """
        if self.peek.is_check or not self.peek.is_mate and not self.peek.is_stale:
            return 1
        else:
            return 0
    
    def __parse_castle(self, castle_type: str) -> Move:
        """__parse_castle.
        Parse a move string which reffers to castling long or short

        :param self:
        :param castle_type:
        :type castle_type: str
        :rtype: Move
        """
        if castle_type == "long":
            long = True
        elif castle_type == "short":
            long = False
        else:
            self.log.error(f"Failed to parse castle '{castle_type}': Matched for a castle but with no group contents")
            raise ValueError("Matched for a castle but with no group contents")

        if self.peek.to_move:
            start_i = 0
            end_i = 0
        else:
            start_i = 7
            end_i = 7

        if long:
            end_j = 2
            castles = 'long'
        else:
            end_j = 6
            castles = 'short'

        start_j = 4
        start = Position(start_i, start_j)
        end = Position(end_i, end_j)
        takes = False

        return Move(start, end, takes, castles)

    def __parse_move(self, move_str: str) -> Optional[Move]:
        """__parse_move.
        Parse a standard chess move (notation such as Qd4, a5, Bxc1... supported).
        Used to parse PGN notation and to allow basic interactivity.

        :param self:
        :param move_str:
        :type move_str: str
        :rtype: Move
        """
        pattern = r'([KQRNB])?([a-h]\d?)?(x)?([a-z]\d)|(O-O)(-O)?'
        matches = re.findall(pattern, move_str)

        if not matches:
            self.log.error(f"Failed to parse {move_str}: no regex match on this string")
            self.log.debug(f"Failed at state: {self.peek.to_fen()}")

        move_repr = matches.pop()

        if move_repr[4]:
            if move_repr[5]:
                return self.__parse_castle('long')
            else:
                return self.__parse_castle('short')

        # if move_repr[2]:
        #     takes = end

        if not move_repr[3]:
            self.log.error(f"Failed to parse {move_str}: no destination square provided")
            self.log.debug(f"Failed at state: {self.peek.to_fen()}")
            return None
        end = Position(move_repr[3].upper())

        takes = end if end in self.peek.loc_map else False
        start = move_repr[1]
        if len(start) == 2:
            start = Position(start.upper())
        else:
            piece = move_repr[0]
            if not piece: piece = "P"
            moves = self.peek.moves
            moves_filt = moves.filter_all_by_value(lambda x: x == end)
            init_piece_candidates = [k for k in moves_filt if moves_filt[k].has_valid]
            piece_candidates = [p for p in init_piece_candidates if p.kind == piece]

            if not piece_candidates:
                self.log.error(f"Failed to parse {move_str}: no candidate pieces found.")
                self.log.debug(f"Failed at state: {self.peek.to_fen()}")
                return None
            elif len(piece_candidates) > 1:
                # Hacky way to check the pieces are in the same file
                piece_candidates = [i \
                              for i in piece_candidates \
                              if str(self.peek.piece_map[i])[0] == start.upper()
                            ]
                if len(piece_candidates) != 1:
                    self.log.warn(f"Failed to parse {move_str}: multiple candidate pieces found.")
                    self.log.debug(f"Failed at state: {self.peek.to_fen()}")
                    return None
            start = self.peek.piece_map[piece_candidates.pop()]

        return Move(start, end, takes)

    @property
    def peek(self) -> Board:
        """peek.
        Legacy from when the game implemeted a stack history and Board did not manipulate its own state.

        :param self:
        :rtype: Board
        """
        if self.__state:
            return self.__state
        else:
            raise ValueError("No state to show")

    def execute_move(self, move: Move) -> bool:
        """execute_move.
        Execute a Move object on the board

        :param self:
        :param move:
        :type move: Move
        :rtype: bool
        """
        return self.peek.move(move)

    def execute_move_str(self, move_str: str) -> bool:
        """execute_move_str.
        Execute a move given in standard chess notation on the board

        :param self:
        :param move_str:
        :type move_str: str
        :rtype: bool
        """
        self.move_hist.append(move_str)
        move = self.__parse_move(move_str)
        if not move: return False
        return self.peek.move(move)

    def show_board(self):
        """show_board.
        Callback to the view function requesting a redraw.

        :param self:
        """
        if not isinstance(self.__view_callback, Callable):
            raise TypeError("view_callback must implement __call__")
        self.__view_callback(self.peek)

    def play(self):
        """play.
        Game loop for interactive play.

        :param self:
        """
        while self.__check_termination():
            self.show_board()
            worked = False
            while not worked:
                move = input("Please enter a move>> ")
                worked = self.execute_move_str(move)
                print(worked)


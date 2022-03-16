from copy import copy
from typing import List, Tuple
from Chess.helpers import pieces_from_fen

import libpychess.pieces as c_pieces
from libpychess import MoveAnalyser
from libpychess import Position as c_Position

import Chess.pieces as py_pieces
from Chess.constants import WHITE
from Chess.result import Result, ResultSet
from Chess.state import Board
from Chess.coordinate import Position as py_Position
from Chess.coordinate import Move
from Chess.exceptions import InvalidMoveError

class CBoard(Board):
    def __init__(self,
        starting_position: Tuple[List[py_pieces.Piece], List[py_pieces.Piece]] = None,
        to_move: int = WHITE,
        can_castle: str = "KQkq",
        en_passant_opts: str = "-",
        half_moves_since_pawn: int = 0, turn: int = 1) -> None:

        """Definition of a mapping from pychess pieces to libpychess pieces"""
        self._cpp_py_piece_conversion = {
            "K" : c_pieces.king,
            "Q" : c_pieces.queen,
            "R" : c_pieces.rook,
            "N" : c_pieces.knight,
            "B" : c_pieces.bishop,
            "P" : c_pieces.pawn,
        }

        self._py_cpp_conv = {
            "k" : py_pieces.King,
            "q" : py_pieces.Queen,
            "r" : py_pieces.Rook,
            "n" : py_pieces.Knight,
            "b" : py_pieces.Bishop,
            "p" : py_pieces.Pawn
        }
        super().__init__(starting_position, to_move, can_castle, en_passant_opts, half_moves_since_pawn, turn)

    def _get_position(self):
        return c_Position

    def _psuedolegal_moves(self, pieces: List[py_pieces.Piece]) -> ResultSet:
        """__psuedolegal_moves.
        Wraps function calls to convert and retrieve data from the libpychess module.

        :param self:
        :param pieces:
        :type pieces: List[Piece]
        :rtype: ResultSet
        """

        # Get the pieces into the correct format (might be helpful to just change all my underlying
        # types lol)
        c_pieces = [
            self._cpp_py_piece_conversion[p.kind](p.colour, c_Position(p.position.i, p.position.j))
            for p in self.all_pieces
        ]
        analysis = MoveAnalyser(c_pieces)

        # This isnt exacltly the same api as the python version
        # Needs to be updated so we instantiate a new MoveAnalyser on each
        # self.calculate (and free the previous)
        # Then we can pass the constructor a list of each piece, and
        # slightly change the PsuedolegalMoves call to take a pointer
        # to a list of pieces to analyse instead of having to go through all the pain
        # For now it works since we only ever look at one colour at a time.
        # Need to account for the edge case of when we check for checkmate and have to
        # evaluate a position without the king there... That relies on the live update of
        # the list and so we might need to define a callback from that function
        # to reinstantiate our analyser object each time - or could try some funkier stuff...
        c_result = analysis.PsuedolegalMoves(pieces[0].colour)

        return ResultSet(
            {
                self._py_cpp_conv[k.kind](
                    k.colour, c_Position(k.position.i, k.position.j)
                ): Result(v)
                for k, v in c_result.items()
            }
        )

def construct_board(fen):
    """construct_board.
    Used to mock a board from a FEN string.

    :param fen:
    """
    params = pieces_from_fen(fen)
    return CBoard(*params)
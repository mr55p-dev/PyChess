from typing import List, Tuple
from Chess import types

from Chess.constants import WHITE, MoveSignal, ResultKeys
from Chess.coordinate import Position
from Chess.helpers import NewGame
from Chess.result import Result, ResultSet
from Chess.state import Board

class PyBoard(Board):
    def __init__(self, fen: str = None) -> None:
        self.Position: types.Position = Position
        ng = NewGame(False)
        self.new_game = ng.new_game
        params = ng.pieces_from_fen(fen) if fen else []

        super().__init__(*params)


    def _allowed_move(self, position, piece) -> MoveSignal:
        """__py_allowed_move.

        Calculates what the "type" of move which has been sent is.

        Returns MoveSignal.empty if a move is allowed
        Returns MoveSignal.blocked if a move is blocked by an allied piece
        Returns MoveSignal.checking_attack if a move is a check
        Returns MoveSignal.capture if a move is a capture
        Returns MoveSignal.disallowed if a move is not allowed (such as pawn push)


        :param self:
        :param position: The position being evaluated (laneded on)
        :param piece: The piece being evaluated
        :rtype: MoveSignal
        """
        capture_allowed = True
        passive_allowed = True
        # Faster than using isinstance calls
        if piece.kind == 'P':
            start_position = self.piece_map[piece]
            # The pieces start at either i=1 or i=6
            start = 1 if piece.colour == WHITE else 6
            has_moved = bool(start - start_position.i)
            if start_position.j - position.j != 0:
                passive_allowed = False
            if start_position.j - position.j == 0:
                capture_allowed = False
            if has_moved and start_position.i - position.i in [2, -2]:
                return MoveSignal.disallowed

        occupier = self.loc_map[position] if position in self.loc_map else None
        if not occupier:
            if passive_allowed: return MoveSignal.empty
            elif capture_allowed: return MoveSignal.attacks
        elif occupier.colour == piece.colour:
            if capture_allowed: return MoveSignal.blocked
        elif capture_allowed:
            if occupier.kind == "K":
                return MoveSignal.checking_attack
            else:
                return MoveSignal.capture
        return MoveSignal.disallowed

    def _psuedolegal_moves(self, pieces: List[types.Piece]) -> ResultSet:
        """__py_psuedolegal_moves.
        Calculates the moves each piece could make if not constrained by checks, etc.
        This is designed to separate move calculation out into a two step process, to
        avoid having to create and analyse future states to evaluate check or checkmate.

        This abstraction allows the board to very quickly mock the moves that the enemy could make
        and this approach relies on the rule that only one side may be in check at any one time.

        :param self:
        :param pieces: Pieces to find moves for
        :type pieces: List[Piece]
        :rtype: ResultSet
        """
        # Preallocate the dict to hpoefully speed things up a bit
        results = ResultSet(dict.fromkeys(pieces))
        for piece in pieces:
            result = Result()
            for dir in piece.projections:
                # Iterate over all the directions a piece can move in
                # Reset the pinned marker.
                pinned = None
                for step in range(1, piece.distance + 1):
                    # Count up all the steps the piece can take until it meets
                    # a stop condition
                    loc = self.piece_map[piece]
                    ni = loc.i + (dir.i * step)
                    nj = loc.j + (dir.j * step)
                    if ni > 7 or ni < 0 or nj > 7 or nj < 0: break
                    landed_on = Position(ni, nj)
                    # try: landed_on = self.piece_map[piece] + (dir * step)
                    # except InvalidFormat: break
                    allowed = self._allowed_move(landed_on, piece)

                    # Reordered expressions to make use of short-circuiting
                    if not pinned and allowed == MoveSignal.empty :
                        # Do not store this location if we are searching for a pin
                        # Store this location as a passive, and an attack for pieces which are
                        # not pawns
                        if piece.kind != "P":
                            result[ResultKeys.attack].append(landed_on)
                        result[ResultKeys.passive].append(landed_on)
                    elif not pinned and allowed == MoveSignal.capture:
                        # Do not store a capture on a normal piece if looking for a pin
                        # Store a piece which can be captured as a capture, and an attack
                        # since that square is controlled by the piece so an enemy king could not
                        # move there.
                        result[ResultKeys.capture].append(landed_on)
                        result[ResultKeys.attack].append(landed_on)
                        # Snapshot the current location and check if this piece which can
                        # be captures is pinned to the king.
                        pinned = Position(landed_on.i, landed_on.j)
                    elif not pinned and allowed == MoveSignal.attacks:
                        # Do not save an attack if we are scanning for a pin
                        # This will only ever be pawn attacks (to separate their passive
                        # capturing and non-capturing moves)
                        result[ResultKeys.attack].append(landed_on); break
                    elif allowed == MoveSignal.checking_attack:
                        # Store a check if we are not looking for a pin
                        if pinned:
                            result[ResultKeys.pin].append(pinned) 
                            break
                        result[ResultKeys.capture].append(landed_on) 
                        break
                    elif allowed == MoveSignal.blocked:
                        # Do not consider a piece defended if we are looking at a pin
                        if pinned: break
                        # Store a piece as defended if an allied piece sees it
                        result[ResultKeys.defend].append(landed_on)
                        break
                    elif allowed == MoveSignal.disallowed:
                        # Do not continue looking if a move is disallowed
                        break

            results[piece] = result

        return results

import math
from copy import copy
from itertools import chain, repeat
from typing import Dict, Tuple, List, Optional
from Chess.constants import BLACK, RANKS, WHITE
from Chess.pieces import Bishop, King, Knight, Pawn, Piece, Queen, Rook
from Chess.coordinate import Move, Position
from Chess.exceptions import InvalidFormat
from Chess.helpers import new_game

class Board():
    """Contains a state of the board"""
    """
	Representation for the game.
	Stores the "active" and "inactive" (captured) pieces,
	the valid continuations (only moves which will not put the king in check)
	and the next piece to move.

	:param white_active:	[ChessPiece]
	:param black_active:	[ChessPiece]
							List of the active pieces for each side
	:attr to_move: 			White|Black
	:attr is_check: 		bool
	:attr is_mate: 			bool
	:attr evaluation: 		int
							The material evaluation (difference in value between active pieces)
	:method calc_moves: 	ChessMove
							All the valid moves for each piece
	:method do_move
		:param move_from: 	Piece starting position
		:param move_to: 	Piece ending position
		:returns: 			ChessBoard
	:method best_move: 		ChessMove
							The best continuting move (based on pieces which can be captured).

    """
    BLOCKED         = 0
    CAPTURE         = 1
    EMPTY           = 2
    CHECKING_ATTACK = 3
    DISALLOWED      = 4
    ATTACKS         = 5

    CHECKMATE = 10
    STALEMATE = 20
    CONTINUE  = 30
    gametype = Tuple[List[Piece], List[Piece]]

    def __init__(self,
                 starting_position: gametype=new_game(),  # type: ignore
                 to_move: int = WHITE,
                 turn: int = 0,
                 can_castle: str = "-",
                 other_fen_params = []) -> None:
        """__init__.

        :param starting_position:
        :param to_move:
        :type to_move: int
        :rtype: None
        """
        # Store the fen information given and piece representations
        # Construct a map of location: piece
        self._white, self._black = starting_position
        self._turn = turn

        # Define convenient variables so we know which pieces are moving
        self._to_move = to_move
        self._opposition = WHITE if to_move == BLACK else BLACK

        # Setup properties which we will later bind in the `calculate` function
        self._is_check = None
        self._is_mate = None
        self._evaluation = None
        self._allowed_moves = None

        # This is just while castling and en-passant is not implemented
        self._castle = self.__parse_castle(can_castle) # castle[4] : white kingside, queenside, black kingside, queenside
        self.other_FEN_params = other_fen_params

        self.calculate()

    def __hash__(self) -> int:
        """__hash__.
        Allow the game state to be stored in a hashmap

        :rtype: int
        """
        return hash(self.to_fen())

    def __repr__(self) -> str:
        """__repr__.
        Provide a very basic string representation of the board.

        :rtype: str
        """

        board = [[" " for _ in range(8)] for _ in range(8)]
        for loc, piece in self.loc_map.items():
            board[loc.i][loc.j] = piece.kind  # type: ignore
        return "\n".join([" ".join([cell for cell in row]) for row in board])

    def __parse_castle(self, castle_str) -> List[bool]:
        castling = [False, False, False, False]
        if castle_str == "-": return castling

        for i in castle_str:
            if i == "K": castling[0]    = True
            elif i == "Q": castling[1]  = True
            elif i == "k": castling[2]  = True
            elif i == "q": castling[3]  = True
            
        return castling


    def __allowed_move(self, position, piece):
        """__allowed_move.
        Decides if a move is valid and what type of move it is if so.
        Also expanded to tell if a piece is checking the king, or if it is defending
        another piece.

        Returns self.EMPTY if a move is allowed
        Returns self.BLOCKED if a move is blocked by an allied piece
        Returns self.CHECKING_ATTACK if a move is a check
        Returns self.CAPTURE if a move is a capture
        Returns self.DISALLOWED if a move is not allowed (such as pawn push)

        :param position:
        :param piece:
        """
        capture_allowed = True
        passive_allowed = True
        if isinstance(piece, Pawn):

            start_position = self.piece_map[piece]
            # The pieces start at either i=1 or i=6
            start = 1 if piece.colour == WHITE else 6
            has_moved = bool(start - start_position._i)
            if start_position._j - position._j != 0:
                passive_allowed = False
            if start_position._j - position._j == 0:
                capture_allowed = False
            if has_moved and start_position._i - position._i in [2, -2]:
                return self.DISALLOWED

        if position in self.loc_map.keys():
            occupied_by = self.loc_map[position]
            if occupied_by.colour == piece.colour: return self.BLOCKED
            else:
                if isinstance(occupied_by, King): return self.CHECKING_ATTACK
                else:
                    if capture_allowed: return self.CAPTURE
                    else: return self.DISALLOWED
        else:
            if passive_allowed: return self.EMPTY
            elif capture_allowed: return self.ATTACKS
            else: return self.DISALLOWED

    def __find_moves(self, piece) -> Dict[str, List[Piece]]:
        """__find_moves.
        All-knowing function which just gets every "semivalid" move for a piece.
        It essentially casts a ray from each projection of a piece to its specified
        max_distance and stores the results of each step until termination in `results`.

        Returns a dict with keys:
            - passive   -> the passive moves for that piece
            - captures  -> the captures this piece can make
            - attacks   -> the squares this piece attacks (controls)
            - defending -> the allied pieces this is defending
            - pin       -> the location of a pin this piece is exerting

        :param piece:
        :rtype: Dict[str, List[Piece]]
        """
        results = {}
        results["passive"] = []
        results["captures"] = []
        results["attacks"] = []
        results["defending"] = []
        results["pin"] = None

        for dir in piece.projections:
            # Iterate over all the directions a piece can move in
            # Reset the pinned marker.
            pinned = None
            for step in range(1, piece.distance + 1):
                # Count up all the steps the piece can take until it meets
                # a stop condition; capturing or moving onto an allied piece,
                # or exiting the bounds of the board which will throw an InvalidFormat
                # exception.
                try: landed_on = self.piece_map[piece] + (dir * step)
                except InvalidFormat: break
                
                                
                if (allowed:=self.__allowed_move(landed_on, piece)) == self.EMPTY:
                    # Store empty squares if we are not looking for a pin
                    if pinned == None: results["passive"].append(landed_on)
                elif allowed == self.CAPTURE:
                    # Store a capture if we are not looking for a pin
                    if pinned == None: results["captures"].append(landed_on); pinned = landed_on
                    # Stop looking for a pin if we encounter a piece that isnt the king
                    else: break
                elif allowed == self.CHECKING_ATTACK:
                    # Store a check if we are not looking for a pin
                    if pinned == None: results["captures"].append(landed_on); break
                    # Store a pin if we found one
                    else: results["pin"] = pinned; break
                elif allowed == self.BLOCKED:
                    # Store a piece as defended if we are not looking for a pin
                    if pinned == None: results["defending"].append(landed_on); break
                    # Stop looking if there is another piece before the king
                    else: break
                elif allowed == self.ATTACKS and pinned == None: 
                    # Store a pawns attacks in a separate list
                    results["attacks"].append(landed_on); break
                elif allowed == self.DISALLOWED:
                    break

        return results

    def __find_move_set(self, pieces: List[Piece]):
        """__find_move_set.
        Wrapper for __find_moves which gives a dict of all the moves for a list of pieces.

        :param pieces:
        """
        move_list = map(self.__find_moves, pieces)
        return {piece: moves for piece, moves in zip(pieces, move_list)}

    def __find_king_moves(self, king):
        """__find_king_moves.
        Looks for the valid moves of a king.

        :param king:

        Only moves will be to unguarded squares - either passive or capture moves.
        The board is evaluated from the opposing perspective as though the moving king
        is not there, so squares which are defended "through the king" such as bishops 
        diagonal do not come up as undefended. The kings captures must only be on 
        undefended pieces.
        """
        candidates = self.__find_moves(king)
        valid = {}

        # Remove the allied king from the state
        moving_pieces = self._get_moving()
        king_index = moving_pieces.index(king)
        temp_king = moving_pieces.pop(king_index)
        
        # Calculate the moves for the enemy pieces without the king there
        moves_without_king = self.__find_move_set(self._get_opposing())
        moving_pieces.insert(king_index, temp_king)

        # Get a flat list of the squares which are passively controlled by enemy pieces.
        opposing_passives = [attack for moves_dict in moves_without_king.values()\
                                  for attack in moves_dict["passive"] + moves_dict["attacks"]]


        valid["passive"] = [i for i in candidates["passive"] if i not in opposing_passives]

        # Get a list of the pieces marked as defended and only keep the moves
        # which are NOT in the defended list
        defended_pieces = [i for moves in moves_without_king.values() for i in moves["defending"]]

        # Calculate castling moves.
        """
        1. Check right to castle string
        1.1 Check if the king or rooks have moved.
        2. If it has; break
           If not: 
            3. For each rook on the A and H files.
                4. Find the squares from rook -> king (including king, excluding rook)
                5. If any are attacked, disable
                6. If not, add the move to passives. Do this as a move object with mov.castle = side
        In move()
        Check the castle property of move.
        If not none: pass off to a handle_castle method.
        Create something to watch 
        """

        # Construct the same response as candidates
        valid["captures"] = [i for i in candidates["captures"] if i not in defended_pieces]
        valid["defending"] = []
        valid["pin"] = None
        return valid
        
    def __filter_moves(self, piece):
        """__filter_moves.
        Will filter out illegal moves from __find_moves(piece).

        :param piece:

        Following the procedure:
        1. If there is more than one piece delivering check then only the king may move.
        2. If there is exactly one piece delivering check then pieces may only move to resolve
            the check.
        3. If a piece is pinned to the king then it may not move in any way to cause check on its
            own king.
        These rules are used to filter out the space of valid moves sequentially.
        """
        results = {}
        results["passive"] = []
        results["captures"] = []
        results["defending"] = []
        results["pin"] = None

        attackers = self._evaluate_check()
        piece_moves = self.__find_moves(piece)
        king = self._get_king()
        
        if len(attackers) > 1:
            if piece != king: return results 
            else: return self.__find_king_moves(king)

        elif len(attackers) == 1:
            # Find the path of the attacking piece to the king
            # Only moves which intercept this path are allowed
            path = self.piece_map[attackers[0]] - self.piece_map[king]
            piece_moves = self.__intersection(piece_moves, path)
        
        # Finally we resolve pins
        # Find the opposing piece pinning the allied piece (pinned_by, piece)
        opposing_moves = self.__find_move_set(self._get_opposing())
        pinned_by = [
            enemy_piece for enemy_piece, moves in opposing_moves.items()\
            if moves["pin"] == self.piece_map[piece]
        ]

        if pinned_by:
            # Update the moves to be only those which maintain the pin AND resolve the check.
            # Note a piece may only be pinned by one other since there is only one king...
            path = self.piece_map[pinned_by.pop()] - self.piece_map[king]
            piece_moves = self.__intersection(piece_moves, path) 
        
        return piece_moves

    def _get_moving(self) -> List[Piece]:
        """_get_moving.
        Returns the active pieces moving in this state.

        :rtype: List[Piece]
        """
        if self._to_move == BLACK:
            return [i for i in self._black if i.is_active]
        else:
            return [i for i in self._white if i.is_active]

    def _get_opposing(self) -> List[Piece]:
        """_get_opposing.
        Returns the active pieces not moving in this state.

        :rtype: List[Piece]
        """
        if self._to_move == WHITE:
            return [i for i in self._black if i.is_active]
        else:
            return [i for i in self._white if i.is_active]

    def _get_king(self) -> King:
        """_get_king.
        Returns the king of the side moving this turn.

        :rtype: King
        """
        return [i for i in self._get_moving() if isinstance(i, King)].pop()

    def __intersection(self, 
                      moves: Dict[str, List[Position]], 
                      by: List[Position]
                      ) -> Dict[str, List[Position]]:
        """_filter_moves.
        Will filter a dictionary of moves to contain only results which appear in `by`.
        The intersection of moves and by.
        Very opinionated to the object returned by `__find_moves()`

        :param moves: List[Position]
        :param by: List[Position]
        """
        valid_moves = {}
        # valid_moves = {type: [move for move in move_list if move in by] for type, move_list in moves.items()}
        for type, move_list in moves.items():
            if not isinstance(move_list, list): continue
            else: valid_moves[type] = [move for move in move_list if move in by]
        return valid_moves

    def _evaluate_check(self) -> List[Optional[Piece]]:
        """_evaluate_check.
        Evaluates if the current position is check.
        Returns a list of all the pieces which currently attack the king.

        :rtype: List[Optional[Piece]]
        """
        moves = self.__find_move_set(self._get_opposing())
        king = self._get_king()

        # Extract all the attacks from the move
        attacks = {piece: move_list["captures"] for piece, move_list in moves.items()}

        # Return a list of all the pieces which have the king as a valid attack
        return [
            piece for piece, attack_list in attacks.items()\
            if self.piece_map[king] in attack_list
        ]

    def _evaluate_mate(self) -> int:
        """_evaluate_mate.
        Will evaluate if the position is checkmate or stalemate.
        Returns one of self.CONTINUE, self.STALEMATE or self.CHECKMATE

        :rtype: int
        """
        all_moves = self.get_move_set(self._get_moving())
        move_types = ["passive", "captures"]
        moves_list = []
        for all_piece_moves in all_moves.values():
            for move_key, move_list in all_piece_moves.items():
                if move_key in move_types:
                    for i in move_list:
                        moves_list.append(i)

        all_moves_list = moves_list

        if not all_moves_list: 
            if self.is_check: return self.CHECKMATE
            else: return self.STALEMATE
        return self.CONTINUE

    def _evaluate_score(self):
        """_evaluate_score."""
        pass

    def get_moves(self, piece: Piece):
        """get_moves.
        Responds with a dict containing the valid moves for a piece.

        :param piece:

        The keys are :
        - "passive": the moves a piece can make to empty squares.
        - "captures": the moves a piece can make to capture an enemy
        - "defending": the allied pieces that this piece defends
        """
        if piece == self._get_king():
            return self.__find_king_moves(piece)
        return self.__filter_moves(piece)

    def get_move_set(self, pieces: list[Piece]):
        """get_move_set.
        Wrapper to get a set of moves instead of just those for a singular piece
        Returns a dict[Piece: moves] where moves is the return type of self.get_moves

        :param pieces:
        :type pieces: list[Piece]
        """
        return {piece: moves for piece, moves in zip(pieces, list(map(self.get_moves, pieces)))}
    
    def allied_moves(self):
        pieces = self._get_moving()
        return {piece: moves for piece, moves in zip(pieces, list(map(self.get_moves, pieces)))}

    def opposing_moves(self):
        pieces = self._get_opposing()
        return {piece: moves for piece, moves in zip(pieces, list(map(self.get_moves, pieces)))}

    @property
    def loc_map(self):
        return { piece.position: piece for piece in self._get_moving() + self._get_opposing() }
    
    @property
    def piece_map(self):
        return { piece: piece.position for piece in self._get_moving() + self._get_opposing() }

    @property 
    def turn(self) -> int:
        return self._turn

    @property
    def pos_map(self) -> dict:
        """Convenience attribute
        Returns a hash map of each occupied position and its associated piece"""
        return self.loc_map

    @property
    def pieces(self) -> list:
        return self._black + self._white

    @property
    def is_check(self) -> Optional[List[Piece]]:
        return self._is_check

    @property
    def is_mate(self) -> bool:
        return self._is_mate
    
    @property
    def is_stale(self) -> bool:
        return self._is_stale
    
    @property
    def to_move(self):
        """to_move."""
        return self._to_move

    def calculate(self):
        # Work out if the current state is check?
        self._is_check = bool(self._evaluate_check()) 

        mate = self._evaluate_mate()
        if mate == self.CHECKMATE: self._is_mate = True; self._is_stale = False
        elif mate == self.STALEMATE: self._is_stale = True; self._is_mate = False
        elif mate == self.CONTINUE: self._is_mate = self._is_stale = False

        # Calculate the possible moves
        self._allowed_moves = self.get_move_set(self._get_moving())


    def move(self, mov: Move):
        """
        """
        moving_piece = self.loc_map[mov.start]

        new_piece = copy(moving_piece)
        new_piece._position = mov.end

        new_moving = self._get_moving()
        new_moving = [i for i in new_moving if i != moving_piece]
        new_moving.append(new_piece)

        new_opposition = self._get_opposing()
        if mov.takes:
            captured = self.loc_map[mov.end]
            idx = new_opposition.index(captured)
            new_opposition[idx].is_active = False

        if self._to_move == WHITE:
            new_white = new_moving
            new_black = new_opposition
        elif self._to_move == BLACK:
            new_white = new_opposition
            new_black = new_moving
        else:
            raise ValueError(f"We have a problem, self._turn = {self._to_move}")

        next_moving = BLACK if self._to_move == WHITE else WHITE
        next_turn = int(self._turn) + 1

        castle_rep = ["K", "Q", "k", "q"]
        can_castle = [v for i, v in enumerate(castle_rep) if self._castle[i]] 
        can_castle = "".join(can_castle)

        return Board((new_white, new_black), next_moving, next_turn, can_castle)


    def to_fen(self):
        fields = []
        ranks = [["" for i in range(8)] for _ in range(8)]
        # The rank of a piece will be calculated as 7 - i; 
        # In FEN the 8th rank (list index 7) is at i=0
        for position, piece in self.loc_map.items():
            symbol = piece.kind
            if piece.colour == BLACK: symbol = symbol.lower()
            ranks[7-position.i][position.j] = symbol
        # Reduce the ranks down to proper notation
        # Hacky but itll do
        irreducable_ranks = []
        for rank in ranks:
            new_rank = []
            counter = 0
            for iter, char in enumerate(rank):
                if not char:
                    counter += 1
                if char and counter:
                    new_rank.append(str(counter))
                    counter = 0
                elif iter == 7 and counter > 0:
                    new_rank.append(str(counter))
                    continue
                new_rank.append(char)
            irreducable_ranks.append("".join(new_rank))
        
        fields.append("/".join(irreducable_ranks))
        
        next_move = "w" if self._to_move == WHITE else 'b'
        fields.append(next_move)

        castle_rep = ["K", "Q", "k", "q"]
        can_castle = [v for i, v in enumerate(castle_rep) if self._castle[i]] 

        # Since i am not ready to finish FEN we will add default data to the end
        fields.append("".join(can_castle))
        fields.append("-") # En-passant right
        fields.append(str(math.ceil(self._turn/2))) # Full move clock
        fields.append(str(self._turn - 1)) # Half move clock ish...
        return " ".join(fields)

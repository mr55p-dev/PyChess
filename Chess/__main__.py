from copy import copy
from Chess.constants import WHITE
from Chess.helpers import pieces_from_fen
from Chess.state import Board  # type: ignore
from Chess.view import view_board  # type: ignore
from Chess.coordinate import Position, Vec # type: ignore

def construct_board(fen):
    params = pieces_from_fen(fen)
    board = Board(params[0], params[1], params[5])
    return board

def game_end(board: Board):
    if board.is_mate or board.is_stale:
        return True
    else:
        return False

if __name__ == "__main__":
    def ng():
        hist = []
        board = Board()
        
        while not game_end(board):
            moving = "white" if board.to_move == WHITE else "black"
            print(f"Turn {board.turn} - {moving} to move.")
            valid_moves = board.get_move_set(board._get_moving())
            exec_move = None
            while not exec_move:
                view_board(board)
                piece_to_move = input("Select a piece to move>>> ")
                try: 
                    piece = board.loc_map[Position(piece_to_move)]
                    piece_moves = valid_moves[piece]
                except KeyError: print("Not a valid piece to select"); continue
                except KeyError: print("Not a valid square"); continue
                print(f"Moves for {piece_to_move}")
                for type, move in piece_moves.items():
                    print(f"{type}: {move}")
                view_board(board, show_moves=piece)
                dest = input("Select a destination square>>> ")
                try: dest_loc = Position(dest)
                except: print("Invalid destination"); continue
                if dest_loc in piece_moves["passive"] or dest_loc in piece_moves["captures"]:
                    exec_move = dest_loc
                else: continue
            new_state = board.move(Position(piece_to_move), dest_loc)
            hist.append(copy(board))
            board = new_state


        
    ng()


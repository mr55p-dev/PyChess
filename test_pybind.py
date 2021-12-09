import sys
sys.path.append("vendor/pychessbinds/build")
import libpychess as lpc

king_w = lpc.pieces.king(lpc.WHITE, lpc.Position(1, 1))
king_b = lpc.pieces.king(lpc.BLACK, lpc.Position(7, 1))
queen_w = lpc.pieces.queen(lpc.WHITE, lpc.Position(1, 2))
queen_b = lpc.pieces.queen(lpc.BLACK, lpc.Position(7, 2))

piece_list = [king_w, king_b, queen_w, queen_b]

psl_analyser = lpc.MoveAnalyser(piece_list)
moves = psl_analyser.PsuedolegalMoves(lpc.WHITE)


for piece in moves:
    print(piece)
    print("Captures: ")
    print(moves[piece].captures)
    print("------")

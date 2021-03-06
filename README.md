# Scientific Programming in Python – submission 1

### Project title: PyChess

### Student name: Ellis Lunnon

I, Ellis Lunnon, have read and understood the School's Academic Integrity Policy, as well as guidance relating to this
module, and confirm that this submission complies with the policy. The content of this project is my own original work,
with any significant material copied or adapted from other sources clearly indicated and attributed.

This repository contains two separate codebases:
- A notebook detailing the implementation of a neural network trained to predict the valid moves of a given chess position using only the location of the pieces on the board.
- A module containing the tools to rapidly generate training data from chess games written in PGN notation.

The notebook leverages Tensorflow 2.5 and several of the modules in the Python data science ecosystem to train neural networks on the training data we can mine from archived online chess games.

## Install instructions
- Clone this repository with `git clone --recursive https://github.com/mpags-python/coursework2021-sub3-mr55p-dev.git`
- Create the anaconda environment `chess-env` with `conda env create -f=environment.yml`
- Optionally build the `libpychess` module with the instructions [here](https://github.com/mr55p-dev/pychessbinds).
- Run a chess game using `python3 -m Chess`
- Create training data with `python3 ./generate_data.py`
- Open the notebook `task.ipynb` using `jupyter notebook` at the command line.

To run a profile of the app, run `python3 ./profile_app` which will generate a file `make_board` appended by the date.
To visualise this file run `snakeviz path/to/file` and a browser window will open with an interactive visualisation of
the call stack for a set of example chess games.

The module is an implementation of Chess in Python (for 3.7) designed to enable computing the end state of a Chess game given a sequence of moves quickly. The core implementation has no external dependencies and is written entirely on top of the standard library. Several parts of the underlying module have been rewritten in C++ and interface using the pybind11 module to improve the speed. 

## Current progress
- [x] Standard piece moves
- [x] Game loop
- [x] Checks
- [x] Checkmate
- [x] Stalemate
- [x] Castling
- [ ] Three-fold repetition
- [ ] 50-half move timeout
- [ ] En-passant
- [ ] Piece promotion

# Initial project outline

## Classes, functions, etc
```
class ChessPiece
	:param colour: 			White|Black
	:param type: 			King|Queen|Rook|Bishop|Knight|Pawn
	:param position: 		ChessVec
							A vector containing piece position
	:method move: 			updates position
	:attr value: 			int
							The value of the piece (based on kind)

class ChessVec
	Wrapper for the positions on a chess board.
	Can convert to/from algebraic ("A1", "B2"..."H8") notation.

	:param rank: 			0-7
	:param file: 			A-H|0-7
	:attr coord: 			[0-7, 0-7]
	:attr algebraic: 		"[A-H][0-7]"

class ChessMove
	Wrapper for a move on the board between two positions.
	Stores reference to the piece moving, start and end squares,
	if the move is check or checkmate.

	:param start: 			ChessVec
	:param end: 			ChessVec
	:param piece: 			ChessPiece
	:param is_check: 		bool
	:param is_mate: 		bool

class ChessBoard
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

class ChessGame
	1. Initialise a new game based on the starting board
	2. Calculate the legal continuations
	3. Monitor for stalemate, checkmate, etc
	4. Monitor for the right to castle, double pawn push
		

	:param starting_board: 	ChessBoard
	:attr full_game: 		[ChessBoard]
	:attr current: 			ChessBoard
	:attr turn: 			int > 0


func from_algebraic
	:param move_str: 		str
							The move to be made in the form (Piece[takes]?Destination[check|mate]?)
							eg. "Qxc5#", "c3", "Na4+"
	:returns move: 			ChessMove

func evaluate_board
	Could be a function or class method.
	1. Get the legal moves
	2. Evaluate the responses to a depth d
	3. Choose the move which leads to the best evaluation in d moves time.

	:param depth: 			int
	:param board: 			ChessBoard
	:returns move: 			ChessMove

	This will look something like:

	d = 0
	evaluations = {value: move}
	def do_evaluate(board, move):
		val = board->evaluate * (-1)**d \\ so the valuation is always in the "right direction"
		new_moves = board->legal moves
		if d < depth:
			d ++
			for candidate in new_moves:
				new_board = board.move(candidate)
				do_evaluate new_board
		elif d = depth:
			evaluations[val] = last move
```

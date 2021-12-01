---
Introduction

- This project aims to implement the game of chess in python, and leverage this game to teach a neural network the rules.
- There is a large library of chess games published by lichess.org, which can be used as training data for this project.
- Although the task of writing chess in python has been done before, I believe there is a lot to learn from approaching this from the ground up.

---
Game

- The implementation is mostly based on object oriented patterns.
- The bare minimum in terms of rules is that
	- Each piece can be moved only in the proper directons and by the proper amount
- Approached herirachically:

Vec and Position capture motion on the board and absolute position respectively.
Move is a wrapper for two positions; start and end, and properties such as if the move involves
capturing another piece
ResultSet is a subclassed dictionary with some convenience methods that improves code reusage
Piece is the base class of a chess piece, which is inherited by every piece class such as King...
Board stores a particular position, and can evaluate all the legal moves in that position
Game is a thin wrapper around board which gives a game loop to enable some simple interaction on the
command line
View is a function to output the board to the user.

---
Data

The framework allows for a huge amount of training data to be accumulated.
The smallest dataset published by lichess is over 120,000 games in a text file (pgn)
Only constraining factor is time to generate this data - the framework is currently quite slow and needs some optimisation

Measuring the ability of a network to predict the squares which can be moved to in a given position.
Visualised as following...

---
Model

- Models trained using the Keras sequental design.
- 1x64 input -> 1x64 output
- Currently experimenting with a variety of architectures, and have found some limited success with a basic fully-connected network
- Considering trying a convolutional network approach, however unsure if a kernel would be an appropriate tool since singular pieces can affect positions on the other side of the board.
- Perhaps it would work however if the pieces are separated into layers, like the channels of an image!
- Also considering a generative approach

---
Results

- So far models have achieved around 70% accuracy on the limited subset of ~1000 instances
- In many instances it is clear the long range pieces like queens, bishops and rooks are tough for the network to understand, whereas kings, knights and pawns are much better represented.

---
Next steps

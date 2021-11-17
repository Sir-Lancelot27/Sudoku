# Sudoku
Efficient brute force Python script to solve file full of NxN Sudoku puzzles

Uses Brute force to solve any NxN sudoku puzzle by for a given puzzle by creating a set of neighbors for every position on the puzzle and a set for the constraints created by those neighbors.

The Brute Force method was made more efficient by either filling in the most constrained position first or by finding the most constrained symbol and attempting to insert it into its positions first in the puzzle depending on which conditiion has smaller amount of possibilities. 

To run Sudoku.py either supply a .txt file with a list of puzzles or it will default run on puzzles.txt. Its output comes in the form

Puzzle#: Puzzle

solvedPuzzle time checkSum
 

checkSum is the sum of every position in the solved sudoku puzzle. For a 9x9 puzzle it would equal 405. Quick way to verify correctness of the sudoku solver.

Puzzles must come in the form of a string that is NxN long filled with '.'s to represent empty spots in the puzzle or a number between 1-N.

Puzzle files come from Dr. Csaba Gabor from my time at TJHSST.

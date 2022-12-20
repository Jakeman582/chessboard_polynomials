# chessboard_polynomials
A Python script for calculating chessboard polynomials

Load chessboard data from a text file and compute its Rook Polynomial
Reads in chessboard data from a text file.
Only symbols 0 and 1 have meaning. 0 means a restricted cell, and 1 
represents an available cell. Any other symbols (including spaces) 
are ignored.
Each row must have the same number of 0s and 1s in order for the 
board to be loaded properly.
Example: To represent the 3-by-3 board without corners
  []  
[][][]
  []  
The text file needs to look like this:
010
111
010
It could also look like this:
0 1 0
1 1 1
0 1 0
This script will print out the board (for the user's visual inspection), as 
well as the polynomial with all powers of x shown in ascending order.
For the example above, this script will print the following:
1x^0 + 5x^1 + 4x^2
Parameters:
----------
This script only excepts one command line argument, a .txt file with chessboard data
Example Usage:
--------------
>python chessboard_polynomials.py board_1.txt
Example Output:
---------------
For the chessboard example above, the output will look like this:
  []
[][][]
  []
1x^0 + 5x^1 + 4x^2


# chessboard_polynomials.py
A Python script used to calculate the rook polynomial, bishop polynomial, and queen polynomial of a given chessboard, represented as a lists of lists.

A rook polynomial is a type of generating function that encodes the number of ways to place any number of rooks on a given chess board such that no rook can be captured by any other rook. For example, consider the 3 by 3 chessboard given below:

[ ][ ][ ]  
[ ][ ][ ]  
[ ][ ][ ]

The rook polynomial of this chessboard is 1 + 9x + 18x^2 + 6x^3. Here, the exponent of x represents the number of rooks being placed on the chess board, and the coefficient tells you how many ways there are to place those rooks such that no rook can be captured. Becuase the coefficient of x^3 is 6, there are 6 ways to place 3 rooks on the 3 by 3 chessboard such that no rook is attacked by any other rook.

Suppose we want to calculate the Rook Polynomial of 3 by 3 board, we need a text file (which we'll call board_1.txt)
that looks like this:  
111  
111  
111

To do this calculation, use the following code:

#Calculating the rook polynomial of the standard 3 by 3 chess board
> python chessboard_polynomials.py board_1.txt

The result will look like this:  
[ ][ ][ ]  
[ ][ ][ ]  
[ ][ ][ ]  
1x^0 + 9x^1 + 18x^2 + 6x^3

A chess board does not have to be square. For example, consider the 3 by 4 chessboard below:

[ ][ ][ ][ ]  
[ ][ ][ ][ ]  
[ ][ ][ ][ ]

The rook polynomial of this board is 1 + 12x + 36x^2 + 24x^3.

Chess boards are also allowed to have holes, or gaps. For example, we can have a 3 by 3 chess board with the center removed, pictured below:

[ ][ ][ ]  
[ ]&nbsp;&nbsp;&nbsp;[ ]  
[ ][ ][ ]

The rook polynomial of this board is 1 + 8x + 14x^2 + 4x^3.

In order to represent holes in these boards, use 0 when defining the matrix. To encode the above example in a text file, use the following code:  
111  
101  
111

As another example, consider a 3 by 3 board with the corners removed:

&nbsp;&nbsp;&nbsp;[ ]  
[ ][ ][ ]  
&nbsp;&nbsp;&nbsp;[ ]  
  
To encode this matrix, use this text file:

010  
111  
010

This code does not take into account any color scheme of the chess board. The color of the squares will not affect the calculation of the rook polynomials. The important thing to remember when defining your board representation is that holes must be represented as 0. Any 1 component will be treated as a plain square.

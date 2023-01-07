
"""Load chessboard data from a text file and compute its Rook Polynomial

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

"""

import sys  # sys.argv
import copy # copy.deepcopy

def load_board(file_name):

    board_file = open(file_name)

    # Our design requires a list of lists to store chessboard data
    # This means we'll need to keep track of the current row to properly
    board = []
    row_number = 0

    for row in board_file:

        # For each row, we'll need to add a list to store each entry
        board.append([])

        # We'll read the file row by row
        for symbol in row:
            # we'll only recognize symbols '0' and '1', ignore al;l otehrs
            if symbol == '0' or symbol == '1':
                board[row_number].append(symbol)
        
        row_number += 1

    board_file.close()

    return board

def count_cells(board):

    count = 0

    rows = len(board)
    columns = len(board[0])

    for row in range(rows):
        for column in range(columns):
            # Only '1' represents a permissible cell, '0' represents a restricted cell
            if board[row][column] == '1':
                count += 1
    return count

def find_first_open_cell(board):

    rows = len(board)
    columns = len(board[0])

    for row in range(rows):
        for column in range(columns):
            if board[row][column] == '1':
                return [row, column]

    # At this point, there are no vacant, permissible cells
    return [-1, -1]

def restrict_row(board, row):

    for column in range(len(board[0])):
        board[row][column] = '0'

def restrict_column(board, column):

    for row in range(len(board)):
        board[row][column] = '0'

def add_polynomials(polynomial_1, polynomial_2):

    sum = []

    for term in range(len(polynomial_1)):
        sum.append(polynomial_1[term] + polynomial_2[term])

    return sum

def print_board(board):

    for row in range(len(board)):
        for column in range(len(board[0])):
            if board[row][column] == '0':
                print("  ", end="")
            if board[row][column] == '1':
                print("[]", end="")
        # We waqnt to keep each row on the same line of output, so now we can 
        # move to the next line
        print("")

def print_polynomial(polynomial):

    for index in range(len(polynomial)):
        if index != 0:
            print(" + ", end="")
        print(str(polynomial[index]) + "x^" + str(index), end="")
    print("")

def rook_polynomial(board):

    if count_cells(board) == 0:
        # Base Case: No cells available (1 + 0x = 1)
        return [1]
    elif count_cells(board) == 1:
        # Base Case: Only one cell available (1 + x)
        return [1, 1]
    else:

        # We need to find the first available cell for decomposition
        cell = find_first_open_cell(board)

        # We'll still need to reference this board, so make copies that we 
        # can modify
        yes_rook = copy.deepcopy(board)
        no_rook = copy.deepcopy(board)

        # When placing a rook, restrict it's row and column
        restrict_row(yes_rook, cell[0])
        restrict_column(yes_rook, cell[1])

        # When not placing a rook, prevent this cell from being used
        no_rook[cell[0]][cell[1]] = '0'

        # We'll need the rook polynomials for both sub-boards
        polynomial_with_rook = rook_polynomial(yes_rook)
        polynomial_without_rook = rook_polynomial(no_rook)

        # Increment the exponents of the rook polynomial for the board we put a rook on
        polynomial_with_rook.insert(0, 0)

        # We should make sure both lists have the same length to make adding the polynomials 
        # easy
        length_rook = len(polynomial_with_rook)
        length_no_rook = len(polynomial_without_rook)
        if length_rook > length_no_rook:
            for i in range(length_rook - length_no_rook):
                polynomial_without_rook.append(0)

        if length_no_rook > length_rook:
            for i in range(length_no_rook - length_rook):
                polynomial_with_rook.append(0)

        # Now we can just return the sum, which will be the final answer
        return add_polynomials(polynomial_with_rook, polynomial_without_rook)

def diagonalize_coordinate(board, row, column):

    rows = len(board)
    columns = len(board[0])

    positive_diagonal = -1
    negative_diagonal = -1

    # Identifying which positive diagonal this cell is on
    positive_diagonal = column + row

    # Identifying the negative diagonal this cell is on
    negative_diagonal = (rows - 1 - row) + column

    return (positive_diagonal, negative_diagonal)

def diagonalize_board(board):

    rows = len(board)
    columns = len(board[0])

    number_positive_diagonals = rows + columns - 1
    number_negative_diagonals = rows + columns - 1

    diagonal_board = []
    for i in range(number_positive_diagonals):
        diagonal_board.append([])
        for j in range(number_negative_diagonals):
            diagonal_board[i].append('0')

    for row in range(rows):
        for column in range(columns):
            if board[row][column] == '1':
                coordinates = diagonalize_coordinate(board, row, column)
                diagonal_board[coordinates[0]][coordinates[1]] = '1'

    return diagonal_board

def restrict_diagonals(board, row, column):

    rows = len(board)
    columns = len(board[0])

    # Restrict cells going diagonally down to the right
    i = 1
    while row + i < rows and column + i < columns:
        board[row + i][column + i] = '0'
        i = i + 1

    # Restrict cells going diagonally down to the left
    i = 1
    while row + i < rows and column - i >= 0:
        board[row + i][column - i] = '0'
        i = i + 1

    # Restrict cells going diagonally up to the left
    i = 1
    while row - i >= 0 and column - i >= 0:
        board[row - i][column - i] = '0'
        i = i + 1

    # Restrict cells going diagonally up to the right
    i = 1
    while row - i >= 0 and column + i < columns:
        board[row - i][column + i] = '0'
        i = i + 1

    # Finally, restrict the given cell
    board[row][column] = '0'

def bishop_polynomial(board):

    if count_cells(board) == 0:
        # Base Case: No cells available (1 + 0x = 1)
        return [1]
    elif count_cells(board) == 1:
        # Base Case: Only one cell available (1 + x)
        return [1, 1]
    else:

        # We need to find the first available cell for decomposition
        cell = find_first_open_cell(board)

        # We'll still need to reference this board, so make copies that we 
        # can modify
        yes_bishop = copy.deepcopy(board)
        no_bishop = copy.deepcopy(board)

        # When placing a rook, restrict it's row and column
        restrict_diagonals(yes_bishop, cell[0], cell[1])

        # When not placing a rook, prevent this cell from being used
        no_bishop[cell[0]][cell[1]] = '0'

        # We'll need the rook polynomials for both sub-boards
        polynomial_with_bishop = bishop_polynomial(yes_bishop)
        polynomial_without_bishop = bishop_polynomial(no_bishop)

        # Increment the exponents of the rook polynomial for the board we put a rook on
        polynomial_with_bishop.insert(0, 0)

        # We should make sure both lists have the same length to make adding the polynomials 
        # easy
        length_bishop = len(polynomial_with_bishop)
        length_no_bishop = len(polynomial_without_bishop)
        if length_bishop > length_no_bishop:
            for i in range(length_bishop - length_no_bishop):
                polynomial_without_bishop.append(0)

        if length_no_bishop > length_bishop:
            for i in range(length_no_bishop - length_bishop):
                polynomial_with_bishop.append(0)

        # Now we can just return the sum, which will be the final answer
        return add_polynomials(polynomial_with_bishop, polynomial_without_bishop)

if __name__ == "__main__":

    board = load_board(sys.argv[1])

    #print_board(board)
    #print_polynomial(rook_polynomial(board))

    #diagonal_board = diagonalize_board(board)
    #print_board(diagonal_board)

    #restrict__diagonals(board, 1, 1)
    #board[1][1] = '0'
    #print_board(board)

    #restrict_diagonals(board, 2, 2)
    #print_board(board)

    print_board(board)
    print_polynomial(bishop_polynomial(board))

    print()
    diagonal_board = diagonalize_board(board)
    print_board(diagonal_board)
    print_polynomial(rook_polynomial(diagonal_board))
    
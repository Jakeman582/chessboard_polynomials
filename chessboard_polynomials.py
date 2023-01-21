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
            # '1', 'R', and 'B' represent permissable cells
            # Only '0' represents a full restricted cell
            if board[row][column] != '0':
                count += 1
    return count

def find_cell(board):
    rows = len(board)
    columns = len(board[0])

    for row in range(rows):
        for column in range(columns):
            # As soon as we find a cell that's not fully restricted, 
            # we found a cell we can decompose on
            if board[row][column] != '0':
                return [row, column]

    # At this point, there are no vacant, permissible cells
    return [-1, -1]

def find_first_open_cell(board):

    rows = len(board)
    columns = len(board[0])

    for row in range(rows):
        for column in range(columns):
            if board[row][column] == '1':
                return [row, column]

    # At this point, there are no vacant, permissible cells
    return [-1, -1]

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
        # We want to keep each row on the same line of output, so now we can 
        # move to the next line
        print("")

def print_polynomial(polynomial):

    for index in range(len(polynomial)):
        if index != 0:
            print(" + ", end="")
        print(str(polynomial[index]) + "x^" + str(index), end="")
    print("")

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

def restrict_rook(board, row, column):

    for c in range(len(board[0])):
        board[row][c] = '0'

    for r in range(len(board)):
        board[r][column] = '0'

def restrict_bishop(board, row, column):

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

def restrict_bishop_from_rooks(board, row, column):

    rows = len(board)
    columns = len(board[0])

    # Any cells that are marked 'R' should not be opened up
    # to bishops after being restricted from them
    for c in range(columns):
        if board[row][c] == '1':
            board[row][c] = 'B'
        if board[row][c] == 'R':
            board[row][c] = '0'

    for r in range(rows):
        if board[r][column] == '1':
            board[r][column] = 'B'
        if board[r][column] == 'R':
            board[r][column] = '0'

    board[row][column] == '0'

def restrict_rook_from_bishops(board, row, column):

    # Any cells that are marked 'B' should not be opened up
    # to rooks after being restricted from them
    rows = len(board)
    columns = len(board[0])

    # Restrict cells going diagonally down to the right
    i = 1
    while row + i < rows and column + i < columns:
        if board[row + i][column + i] == '1':
            board[row + i][column + i] = 'R'
        if board[row + i][column + i] == 'B':
            board[row + i][column + i] = '0'
        i = i + 1

    # Restrict cells going diagonally down to the left
    i = 1
    while row + i < rows and column - i >= 0:
        if board[row + i][column - i] == '1':
            board[row + i][column - i] = 'R'
        if board[row + i][column - i] == 'B':
            board[row + i][column - i] = '0'
        i = i + 1

    # Restrict cells going diagonally up to the left
    i = 1
    while row - i >= 0 and column - i >= 0:
        if board[row - i][column - i] == '1':
            board[row - i][column - i] = 'R'
        if board[row - i][column - i] == 'B':
            board[row - i][column - i] = '0'
        i = i + 1

    # Restrict cells going diagonally up to the right
    i = 1
    while row - i >= 0 and column + i < columns:
        if board[row - i][column + i] == '1':
            board[row - i][column + i] = 'R'
        if board[row - i][column + i] == 'B':
            board[row - i][column + i] = '0'
        i = i + 1

def chess_polynomial(board, restrict):
    if count_cells(board) == 0:
        # Base Case: No cells available (1 + 0x = 1)
        return [1]
    elif count_cells(board) == 1:
        # We need to know what restrictions this cell has to return the appropriate multinomial


        # Base Case: Only one cell available (1 + x)
        return [1, 1]
    else:

        # We need to find the first available cell for decomposition
        cell = find_first_open_cell(board)

        # We'll still need to reference this board, so make copies that we 
        # can modify
        yes_piece = copy.deepcopy(board)
        no_piece = copy.deepcopy(board)

        # When placing a rook, restrict it's row and column
        restrict(yes_piece, cell[0], cell[1])

        # When not placing a rook, prevent this cell from being used
        no_piece[cell[0]][cell[1]] = '0'

        # We'll need the rook polynomials for both sub-boards
        polynomial_with_piece = chess_polynomial(yes_piece, restrict)
        polynomial_without_piece = chess_polynomial(no_piece, restrict)

        # Increment the exponents of the rook polynomial for the board we put a rook on
        polynomial_with_piece.insert(0, 0)

        # We should make sure both lists have the same length to make adding the polynomials 
        # easy
        length_piece = len(polynomial_with_piece)
        length_no_piece = len(polynomial_without_piece)
        if length_piece > length_no_piece:
            for i in range(length_piece - length_no_piece):
                polynomial_without_piece.append(0)

        if length_no_piece > length_piece:
            for i in range(length_no_piece - length_piece):
                polynomial_with_piece.append(0)

        # Now we can just return the sum, which will be the final answer
        return add_polynomials(polynomial_with_piece, polynomial_without_piece)

def multinomial_dimension(m0, m1, m2):

    # Get the number of rows needed for each multinomial
    rows_0 = len(m0)
    rows_1 = len(m1)
    rows_2 = len(m2)
    rows = max(rows_0, rows_1, rows_2)

    # Get the number of columns needed for each multinomial
    columns_0 = len(m0[0])
    columns_1 = len(m1[0])
    columns_2 = len(m2[0])
    columns = max(columns_0, columns_1, columns_2)

    return [rows, columns]

def normalize_multinomial(m, dimension):

    # Determine how many rows and columns are needed to match the dimension
    rows = dimension[0]
    columns = dimension[1]

    rows_to_add = rows - len(m)
    columns_to_add = columns - len(m[0])

    # Add the appropriate number of columns
    for row in m:
        for c in range(columns_to_add):
            row.append(0)

    # Each row added must be the same length of the already existant rows in the multinomial
    blank = []
    for i in range(len(m[0])):
        blank.append(0)

    # Add the necessary number of blank lines to the multinomial to get the correct number of 
    # rows
    for i in range(rows_to_add):
        m.append(blank)

def add_multinomials(m0, m1, m2):

    # Initialize an empty multinomial to hold the coefficients
    s = []
    dimension = multinomial_dimension(m0, m1, m2)
    for r in range(dimension[0]):
        s.append([])
        for c in range(dimension[1]):
            s[r].append(0)

    # Perform the addition
    for r in range(dimension[0]):
        for c in range(dimension[1]):
            s[r][c] = m0[r][c] + m1[r][c] + m2[r][c]

    return s

def chess_multinomial(board, restrict_1, restrict_2):

    # Base case: No cells left (1 + 0x + 0y + 0xy)
    if count_cells(board) == 0:

        return [[1]]

    # With only one cell left, we know what the Chess Polynomial will be
    elif count_cells(board) == 1:

        # We'll need to know what ipeces this cell is open to
        [row, column] = find_cell(board)

        if board[row][column] == 'R':
            return [
                [1, 1]
            ]

        elif board[row][column] == 'B':
            return [
                [1, 0], 
                [1, 0]
            ]

        else:
            return [
                [1, 1], 
                [1, 0]
            ]
    else:

        # We need to find an open cell on whioch to decompose
        # We could decompose on a '1', 'R', or a 'B'
        cell = find_cell(board)

        # Regardless of what kind of open cell we find, we can always 
        # choose to restrict it from any pieces in the future
        no_piece = copy.deepcopy(board)
        no_piece[cell[0]][cell[1]] = '0'
        m0 = chess_multinomial(no_piece, restrict_1, restrict_2)

        # If the cell we decompose on is only open to bishops, 
        # we can't place a rook, so return the 0 multinomial
        m1 = [[0]]
        if board[cell[0]][cell[1]] != 'B':
            piece_1 = copy.deepcopy(board)
            restrict_1(piece_1, cell[0], cell[1])
            restrict_rook_from_bishops(piece_1, cell[0], cell[1])
            m1 = chess_multinomial(piece_1, restrict_1, restrict_2)
            for polynomial in m1:
                polynomial.insert(0, 0)

        # If the cell we decompose on is only open to rooks, 
        # we can't place a bishop, so return the 0 multinomial
        m2 = [[0]]
        if board[cell[0]][cell[1]] != 'R':
            piece_2 = copy.deepcopy(board)
            restrict_2(piece_2, cell[0], cell[1])
            restrict_bishop_from_rooks(piece_2, cell[0], cell[1])
            m2 = chess_multinomial(piece_2, restrict_1, restrict_2)
            blank_2 = []
            for z in range(len(m2[0])):
                blank_2.append(0)
            m2.insert(0, blank_2)

        # Make sure all multinomials have the same dimension
        dimension = multinomial_dimension(m0, m1, m2)
        normalize_multinomial(m0, dimension)
        normalize_multinomial(m1, dimension)
        normalize_multinomial(m2, dimension)

        # Add the multinomials together
        multinomial = add_multinomials(m0, m1, m2)

    return multinomial

def print_multinomial(m):

    [rows, columns] = multinomial_dimension(m, m, m)

    for row in range(rows):
        for column in range(columns):
            if row != 0 or column != 0:
                print(" + ", end = "")
            if m[row][column] != 0:
                print(str(m[row][column]) + "(r^" + str(column) + ")(b^" + str(row) + ")", end = "")

    print()

if __name__ == "__main__":
    board = load_board(sys.argv[1])
    print_multinomial(chess_multinomial(board, restrict_rook, restrict_bishop))
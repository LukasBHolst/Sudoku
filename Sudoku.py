# Build a sudoku solver using a backtracking algorithm

# Nice sudoku print
def print_board(board):
    # Print string for formatting
    s = ""
    for i in range(len(board)):
        # Roof
        if i == 0:
            s += "-------------------------\n"
        # Every 3 squares Vertically
        if i % 3 == 0 and not i == 0:
            s += "|-------+-------+-------|\n"
        for j in range(len(board)):
            # Beginning wall
            if j % 3 == 0:
                s += "| "
            # Print square and ending wall
            if j == 8:
                s += str(board[i][j]) + " |\n"
            # Print squares
            else:
                s += str(board[i][j]) + " "
    # Floor
    s += "-------------------------"
    print(s)


# Find row and column of an unassigned square.
# If empty then assign the (row, col) accordingly and return true
def find_empty(board, pos):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                pos[0] = i
                pos[1] = j
                return True
    return False


# Is a number in the same row
def is_digit_in_row(board, row, digit):
    for i in range(len(board)):
        if board[row][i] == digit:
            return True
    return False


# Is a number in the same column
def is_digit_in_col(board, col, digit):
    for i in range(len(board)):
        if board[i][col] == digit:
            return True
    return False


# Is a number in the same 3*3 box
def is_digit_in_box(board, pos, digit):
    row, col = pos
    for i in range(len(board) // 3):
        for j in range(len(board) // 3):
            if board[i + (row - row % 3)][j + (col - col % 3)] == digit:
                return True
    return False


# Is it safe to assign a given number on the board at the (row, col))
def is_safe_to_assign(board, pos, digit):
    if is_digit_in_row(board, pos[0], digit) or \
       is_digit_in_col(board, pos[1], digit) or \
       is_digit_in_box(board, pos, digit):
        return False
    return True


# Using the functions above, we solve the sudoku using backtracking
def solve_sudoku(board):
    # Temp value (row, col)
    pos = [0, 0]

    # If there are no more empty squares left, we are done
    if not find_empty(board, pos):
        return True

    # For a number between and including 1 to 9
    # See if the number is safe to assign
    # Append the safe number to the board
    for digit in range(1, 10):
        if is_safe_to_assign(board, pos, digit):
            row, col = pos
            board[row][col] = digit

            # Recurse the function until True
            if solve_sudoku(board):
                return True

            # Or go back and try new solution
            board[row][col] = 0

    return False


# Test board with 0's to be filled
test = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
        [5, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 7, 0, 0, 0, 0, 3, 1],
        [0, 0, 3, 0, 1, 0, 0, 8, 0],
        [9, 0, 0, 8, 6, 3, 0, 0, 5],
        [0, 5, 0, 0, 9, 0, 6, 0, 0],
        [1, 3, 0, 0, 0, 0, 2, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 7, 4],
        [0, 0, 5, 2, 0, 6, 3, 0, 0]]

""" 
    Result:
    -------------------------
    | 3 1 6 | 5 7 8 | 4 9 2 |
    | 5 2 9 | 1 3 4 | 7 6 8 |
    | 4 8 7 | 6 2 9 | 5 3 1 |
    |-------+-------+-------|
    | 2 6 3 | 4 1 5 | 9 8 7 |
    | 9 7 4 | 8 6 3 | 1 2 5 |
    | 8 5 1 | 7 9 2 | 6 4 3 |
    |-------+-------+-------|
    | 1 3 8 | 9 4 7 | 2 5 6 |
    | 6 9 2 | 3 5 1 | 8 7 4 |
    | 7 4 5 | 2 8 6 | 3 1 9 |
    -------------------------
"""

# Make the sudoku solver generate a solved board with random board placement
# and make a generated game of sudoku with 0's so you can play

def make_empty_board():
    return [[0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]]

# Creates a fully solved board
def make_solved_board():
    import random

    # Empty board
    board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    # Plug in random values (0 - 9) at random places (0 - 8)
    # on the x and y axis in the board
    for i in range(9):
        randval = random.randint(1, 9)
        randval2 = random.randint(1, 9)
        pos = [0, i]

        # If the values at the position is valid
        if is_safe_to_assign(board, pos, randval):
            board[pos[0]][pos[1]] = randval
        pos = [i, 0]
        if is_safe_to_assign(board, pos, randval2):
            board[pos[0]][pos[1]] = randval2

    # With the random values in place
    # We can use the backtracking algorithm to solve the board
    if solve_sudoku(board):
        return board

    # This case is highly unlikely, but here nonetheless
    # Recurse if the board is not possible to create
    else:
        print("making new board")
        make_solved_board()


# Creates a new board with empty squares
# Difficulty between 1 and 3 where:
# 1 = easy, 2 = medium, 3 = hard
def make_new_board(difficulty=1):
    import random

    # Amount of squares to set to 0
    # and the fully solved board we have to manipulate
    amount_to_remove = 0
    board = make_solved_board()

    # Set amount to remove
    if difficulty == 1:
        amount_to_remove = 20
    elif difficulty == 2:
        amount_to_remove = 40
    elif difficulty == 3:
        amount_to_remove = 60
    else:
        print("Invalid difficulty")

    # Randomly remove squares from the board
    for i in range(amount_to_remove):
        randpos = random.randint(0, 8)
        randpos2 = random.randint(0, 8)
        randposbackup = random.randint(0, 8)

        if board[randpos][randpos2] == 0:
            board[randpos2][randposbackup] = 0
        else:
            board[randpos][randpos2] = 0
    return board



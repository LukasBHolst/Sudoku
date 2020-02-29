
import pygame

from Squares import Squares
from Sudoku import make_new_board, is_safe_to_assign, find_empty
from GUI import BLACK


# The Board class
class Board:
    # The sudoku board to be shown
    # The parameter used is the difficulty from 1 to 3, where 1 is the default
    boardy = make_new_board(2)

    # Constructor
    # We want to know about the rows and columns and the size of the board to display.
    # We also want to update the display
    # The squares are initialized as a part of the class.
    # We also want to update the model of the board, to be shown.
    # Lastly we want to know which square is selected, f.x from a mouse click.
    def __init__(self, rows, cols, width, height, display):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.display = display
        self.squares = [[Squares(self.boardy[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.model = None
        self.update_model()
        self.selected = None

    # Method for updating the model after assigning new values to the board
    def update_model(self):
        self.model = [[self.squares[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    # This method checks if the value is safe to assign to the selected square on the board.
    # If it is not safe we, as a precaution, set the value to 0 and the temporary value locked in to 0
    def place(self, val):
        row, col = self.selected
        if self.squares[row][col].value == 0:
            self.squares[row][col].set_value(val)
            pos = (row, col)

            if is_safe_to_assign(self.model, pos, val):
                print("safe")
                self.update_model()
                return True
            else:
                print("not safe")
                self.squares[row][col].set_value(0)
                self.squares[row][col].set_temp(0)
                self.update_model()
                return False

    # Sets the temp value at the selected square
    def temporary(self, val):
        row, col = self.selected
        self.squares[row][col].set_temp(val)

    # Draw
    def draw(self):
        gap = self.width / 9

        # Draw the lines in the board
        for i in range(self.rows+1):
            if i % 3 == 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.display, BLACK, (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(self.display, BLACK, (i * gap, 0), (i * gap, self.height), thick)

        # Draw the squares
        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].draw(self.display)

    # Sets the selected pos to selected on the board
    def select(self, pos):
        row, col = pos
        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].selected = False
        self.squares[row][col].selected = True
        self.selected = pos

    # Clears the temp value in the selected square
    def clear(self):
        row, col = self.selected
        if self.squares[row][col].value == 0:
            self.squares[row][col].set_temp(0)

    # Gets the square the mouse has clicked on, if it is inside the board.
    # This does not include the display.
    def click(self, pos):
        row = pos[1]
        col = pos[0]
        if row < self.width and col < self.height:
            gap = self.width // 9
            x = row // gap
            y = col // gap
            return x, y
        else:
            return None

    # Checks whether the game is finished or not
    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.squares[i][j].value == 0:
                    return False
        return True

    # Uses the backtracking algorithm to solve the sudoku board in a brute force manner
    def solve_gui(self):

        # Temp value (row, col)
        pos = [0, 0]

        if not find_empty(self.model, pos):
            return True

        # Checks to see whether the current number is safe to assign or not,
        # updating the model and uses a delay to view the algorithm in action.
        for digit in range(1, 10):
            if is_safe_to_assign(self.model, pos, digit):
                row, col = pos
                self.model[row][col] = digit
                self.squares[row][col].set_value(digit)
                self.squares[row][col].draw_change(self.display, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(60)

                # Backtracking occuring
                if self.solve_gui():
                    return True

                # Undo
                self.model[row][col] = 0
                self.squares[row][col].set_value(0)
                self.update_model()
                self.squares[row][col].draw_change(self.display, False)
                pygame.display.update()
                pygame.time.delay(60)
        return False


import pygame
import time

import Board

pygame.init()

# Global Constants

# Height and Width of display
WIDTH = 540
HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
SILVER = (185, 185, 185)
LSILVER = (200, 200, 200)

# Font
font = pygame.font.SysFont('italics', 40)


# Function for coloring the solve button a certain color
def color_solve_button(display, color):
    pygame.draw.rect(display, color, (135, 550, 140, 40))
    text = font.render("Solve", True, BLACK)
    display.blit(text, (135 + 32, 558))


# Function to see whether the position of the mouse is inside the solve button object
def inside_solve_button(pos):
    return 135 < pos[0] < 135 + 140 and 550 < pos[1] < 550 + 40


# Function to see whether the position of the mouse is inside the reset button object
def inside_reset_button(pos):
    start_x = (WIDTH // 2 - 100) + 40
    start_y = (HEIGHT // 2 - 50) + 100
    end_x = start_x + 120
    end_y = start_y + 50
    return start_x < pos[0] < start_y and end_x < pos[1] < end_y


# Function for coloring the reset button a certain color
def color_reset_button(display, color):
    box_x = WIDTH // 2 - 100
    box_y = HEIGHT // 2 - 50

    # Draw box
    pygame.draw.rect(display, color, (box_x + 40, box_y + 100, 120, 50))

    # Draw text
    box_x = box_x + 50
    box_y = box_y + 105
    text = font.render("Restart", True, BLACK)
    display.blit(text, (box_x, box_y + 5))


# Redraws the display panel under the board
def redraw_display(display, board, timer, strikes):
    # Draw over old frame
    display.fill(WHITE)

    # The time display
    text = font.render("Time:" + format_time(timer), 1, BLACK)
    display.blit(text, (350, 560))

    # The strike display
    text = font.render(("X*" + str(strikes)), True, RED)
    display.blit(text, (20, 560))

    # Solve button display
    color_solve_button(display, SILVER)

    # Redraw board
    board.draw()


# Formats the time to "min : sec"
def format_time(secs):
    sec = secs % 60
    min = secs // 60
    form = str.format("{}m : {}s", min, sec)
    return form


# Game over function which starts when you lose or win the game
def game_over(display, is_win):
    # GUI coords
    box_x = WIDTH // 2 - 100
    box_y = HEIGHT // 2 - 50

    # Grey transparent screen
    s = pygame.Surface((WIDTH, HEIGHT))
    s.fill(GREY)
    s.set_alpha(8)
    display.blit(s, (0, 0))

    # Checks whether you won or lost, drawing accordingly
    if is_win:
        # Green box
        pygame.draw.rect(display, GREEN, (box_x, box_y, 200, 100))

        # You Win text
        text = font.render("You Win", True, WHITE)
        display.blit(text, (box_x + 45, box_y + 35))

        color_reset_button(display, GREY)

    else:
        # Red box
        pygame.draw.rect(display, RED, (box_x, box_y, 200, 100))

        # Game Over text
        text = font.render("Game Over", True, WHITE)
        display.blit(text, (box_x + 25, box_y + 35))

        color_reset_button(display, GREY)


# Game function
def game():
    # Sets up local variables and game display/screen
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Sudoku')
    board = Board.Board(9, 9, 540, 540, display)
    key = None
    is_running = True
    is_game_over = False
    is_win = True
    start = time.time()
    strikes = 0

    # The game is running
    while is_running:
        game_time = round(time.time() - start)

        # Check for which game events are happening
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                is_running = False
            # Keyboard numbers
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9

                # Clear current square for temporary value with delete key
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None

                # Algorithm and game over with space
                if event.key == pygame.K_SPACE:
                    if board.solve_gui():
                        is_running = False
                        is_game_over = True
                        is_win = True

                # Press enter to validate whether the temp key is a valid sudoku move
                # If it's not valid, you get 1 strike
                if event.key == pygame.K_RETURN:
                    row, col = board.selected
                    if not board.squares[row][col].temp == 0:
                        if board.place(board.squares[row][col].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        # 10 strikes and you're out
                        if strikes > 9:
                            is_running = False
                            is_game_over = True
                            is_win = False
                            print("Game over")

            # Mouse press handler
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # Gets the clicked square
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked)
                    key = None

                # Press the solve button on the display panel
                if inside_solve_button(pos):
                    color_solve_button(display, GREY)
                    if board.solve_gui():
                        is_running = False
                        is_game_over = True
                        is_win = True

        #
        if board.selected and key is not None:
            board.temporary(key)
        redraw_display(display, board, game_time, strikes)
        pygame.display.update()

    while is_game_over:
        game_over(display, is_win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_game_over = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if inside_reset_button(pos):
                    color_reset_button(display, LSILVER)
                    game()

        pygame.display.update()


if __name__ == '__main__':
    game()
    pygame.quit()

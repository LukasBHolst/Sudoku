
import pygame

from GUI import font, BLACK, GREY, WHITE, RED, GREEN

# The class for the individual squares
class Squares:
    rows = 9
    cols = 9

    # Constructor
    # We need the value but also a temporary value if we want to highlight the "to-be" input value.
    # We also need the width and height to define the squares size.
    # We also need to check whether the square has been selected or not
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    # Draw the actual value and the temporary value on the square
    def draw(self, display):
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if not self.temp == 0 and self.value == 0:
            text = font.render(str(self.temp), 1, GREY)
            display.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = font.render(str(self.value), 1, BLACK)
            display.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(display, RED, (x, y, gap, gap), 3)

    # Update the square
    def draw_change(self, display, is_correct):
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(display, WHITE, (x, y, gap, gap), 0)

        text = font.render(str(self.value), 1, (0, 0, 0))
        display.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if is_correct:
            pygame.draw.rect(display, GREEN, (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(display, RED, (x, y, gap, gap), 3)

    # Setter for the value
    def set_value(self, val):
        self.value = val

    # Setter for the temporary value
    def set_temp(self, val):
        self.temp = val

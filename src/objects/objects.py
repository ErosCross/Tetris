import pygame

class Button:
    def __init__(self, text, center_position, font, default_color, hover_color):
        self.text = text
        self.center_position = center_position
        self.font = font
        self.default_color = default_color
        self.hover_color = hover_color
        self.rect = None
        self.rendered_text = None

    def render(self, mouse_cursor):
        # Render the text with the default color
        color = self.default_color

        # Check if the mouse is over the button and change color if hovering
        if self.rect.collidepoint(mouse_cursor):
            color = self.hover_color

        # Render the button text with the current color
        self.rendered_text = self.font.render(self.text, True, color)
        self.rect = self.rendered_text.get_rect(center=self.center_position)

    def draw(self, screen):
        # Draw the button on the screen
        screen.blit(self.rendered_text, self.rect)

class Block:
    def __init__(self,color, cords):
        self.color = color
        self.x = cords.x
        self.y = cords.y
    def draw(self):
        pass




class Tetromino:
    def __init__(self, color, direction):

        self.color = color
        self.direction = direction
        self.shape = []  # To be defined by subclasses

    def rotate(self):

        self.shape = [list(row) for row in zip(*self.shape[::-1])]


class OTetromino(Tetromino):
    def __init__(self, color=(255, 255, 0), direction=0):

        super().__init__(color, direction)
        self.shape = [
            [1, 1],
            [1, 1]
        ]

    def rotate(self):

        pass


class TTetromino(Tetromino):
    def __init__(self, color=(128, 0, 128), direction=0):

        super().__init__(color, direction)
        self.shape = [
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0]
        ]


class SZTetromino(Tetromino):
    def __init__(self, color=(0, 255, 0), direction=0, is_s=True):

        super().__init__(color, direction)
        if is_s:
            self.shape = [
                [0, 1, 1],
                [1, 1, 0],
                [0, 0, 0]
            ]
        else:
            self.shape = [
                [1, 1, 0],
                [0, 1, 1],
                [0, 0, 0]
            ]


class JLTetromino(Tetromino):
    def __init__(self, color=(0, 0, 255), direction=0, is_j=True):
        """
        J and L Tetrominoes.
        :param is_j: If True, represents J-shape; if False, represents L-shape.
        """
        super().__init__(color, direction)
        if is_j:
            self.shape = [
                [1, 0, 0],
                [1, 1, 1],
                [0, 0, 0]
            ]
        else:
            self.shape = [
                [0, 0, 1],
                [1, 1, 1],
                [0, 0, 0]
            ]


class ITetromino(Tetromino):
    def __init__(self, color=(0, 255, 255), direction=0):
        """
        I-Tetromino (Line shape).
        """
        super().__init__(color, direction)
        self.shape = [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

    def rotate(self):
        """
        Rotate the I-Tetromino considering its specific behavior in the grid.
        """
        super().rotate()






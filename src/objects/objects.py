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
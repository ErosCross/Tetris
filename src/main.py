import pygame, sys
from src.objects.objects import Button


# COLOR PALETTE -> https://www.schemecolor.com/light-gray-all-the-way-color-combination.php


pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound
pygame.font.init()

# DECLARE SCREEN SIZE

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

# Define clock for game

clock = pygame.time.Clock()

icon = pygame.image.load('../src/images/game-icon.png')
# Set the window icon
pygame.display.set_icon(icon)

# Click button sound

click_sound = pygame.mixer.Sound('sounds/button_pressed.wav')


class StartMenu:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bg_image = pygame.image.load("../src/images/background_image.png")
        self.header_font = pygame.font.Font('../src/fonts/guardener.ttf', 100)
        self.header_font_outline = pygame.font.Font('../src/fonts/guardener.ttf', 102)
        self.button_font = pygame.font.Font('../src/fonts/guardener.ttf', 50)
        pygame.display.set_caption('TETRIS - BY AMIT SHAVIV')

    def draw_text(self, mytext):
        # Get text content
        text = self.header_font.render(mytext, True, (255, 255, 255))
        outline = self.header_font_outline.render(mytext, True, (0, 255, 0))
        # Position it in the center
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 225))
        outline_rect = outline.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 225))

        self.screen.blit(outline, outline_rect)
        self.screen.blit(text, text_rect)

    # Function to render button text
    def render_button(self, text, font, color, center_position):
        button_text = font.render(text, True, color)
        button_rect = button_text.get_rect(center=center_position)
        return button_text, button_rect

    def draw_buttons(self):
        mouse_cursor = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()

        # Define button positions
        start_button_center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 120)
        options_button_center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40)
        exit_button_center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40)

        buttons = [
            {"text": "START", "center": start_button_center, "color": (255, 255, 255), "hover_color": (180, 180, 180)},
            {"text": "OPTIONS", "center": options_button_center, "color": (255, 255, 255), "hover_color": (180, 180, 180)},
            {"text": "EXIT", "center": exit_button_center, "color": (255, 255, 255), "hover_color": (180, 180, 180)}
        ]

        # Loop through buttons
        for button in buttons:
            text, rect = self.render_button(button["text"], self.button_font, button["color"], button["center"])

            # Hover effect
            if rect.collidepoint(mouse_cursor):
                text, rect = self.render_button(button["text"], self.button_font, button["hover_color"], button["center"])

                # Play sound when button is clicked
                if mouse_buttons[0]:  # Left mouse button is clicked
                    click_sound.play()

                    # If the "EXIT" button is clicked, quit the game
                    if button["text"] == "EXIT":
                        pygame.time.delay(100)
                        pygame.quit()
                        sys.exit()

                    # If the "START" button is clicked, start the game
                    if button["text"] == "START":
                        self.start_game()

            # Draw the button
            self.screen.blit(text, rect)

    def draw_screen(self):
        # Fill the screen with a background image
        self.screen.blit(self.bg_image, (0, 0))
        self.draw_buttons()

    def show_menu(self):
        running = True
        while running:
            # Poll for events (like quitting the game)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Fill the screen with background and draw other elements
            self.draw_screen()
            self.draw_text("TETRIS")

            # Flip the display (update the screen with what we drew)
            pygame.display.flip()

            # Limit FPS to 60
            clock.tick(60)

        # Quit Pygame after the loop is done
        pygame.quit()

    def start_game(self):
        # Create an instance of the Game class and start the game
        game = Game()
        game.show_game()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.text_font = pygame.font.Font('../src/fonts/guardener.ttf', 100)
        pygame.display.set_caption('TETRIS - GAME')

    def draw_screen(self):

        canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Define the dimensions for the game and UI portions
        game_height = int(SCREEN_HEIGHT * 0.85)  # 85% of the screen height for the game
        ui_height = SCREEN_HEIGHT - game_height  # Remaining 15% for the UI
        # Camera rectangles for sections of the canvas
        game_portion = pygame.Rect(0, 0, SCREEN_WIDTH, game_height)
        ui_portion = pygame.Rect(0, game_height, SCREEN_WIDTH, ui_height)
        # Draw game portion
        pygame.draw.rect(canvas, (0, 128, 255), game_portion)  # Blue for the game portion
        # Draw UI portion
        pygame.draw.rect(canvas, (128, 128, 128), ui_portion)  # Gray for the UI portion
        # Define dimensions and positions for the time and score boxes
        box_width = SCREEN_WIDTH // 4  # Each box takes 1/4 of the screen width
        box_height = ui_height - 10  # Slight padding from the top and bottom
        padding = 10  # Padding between the boxes and screen edges
        # Time box
        time_box = pygame.Rect(padding, game_height + 5, box_width, box_height)
        pygame.draw.rect(canvas, (255, 255, 255), time_box)  # White background
        pygame.draw.rect(canvas, (0, 0, 0), time_box, 2)  # Black border
        # Score box
        score_box = pygame.Rect(SCREEN_WIDTH - box_width - padding, game_height + 5, box_width, box_height)
        pygame.draw.rect(canvas, (255, 255, 255), score_box)  # White background
        pygame.draw.rect(canvas, (0, 0, 0), score_box, 2)  # Black border
        # Example text (replace with dynamic values)
        font = pygame.font.Font(None, 36)  # Adjust font and size as needed
        time_text = font.render("Time: 00:00", True, (0, 0, 0))
        score_text = font.render("Score: 0", True, (0, 0, 0))
        # Center the text in the boxes
        canvas.blit(time_text, (time_box.x + (time_box.width - time_text.get_width()) // 2,
                                time_box.y + (time_box.height - time_text.get_height()) // 2))
        canvas.blit(score_text, (score_box.x + (score_box.width - score_text.get_width()) // 2,
                                 score_box.y + (score_box.height - score_text.get_height()) // 2))
        # Blit the canvas to the display
        self.screen.blit(canvas, (0, 0))

        # Add more game-related drawings here

    def show_game(self):
        running = True
        while running:
            # Poll for events (like quitting the game)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Draw the game screen
            self.draw_screen()

            # Flip the display (update the screen with what we drew)
            pygame.display.flip()

            # Limit FPS to 24 (or adjust for your game)
            clock.tick(24)

        # Quit Pygame after the game loop is done
        pygame.quit()


# Defining the main function
def main():
    menu = StartMenu()  # Create an instance of StartMenu
    menu.show_menu()    # Call the show_menu method on the instance


if __name__ == "__main__":
    main()

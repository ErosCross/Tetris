import pygame, sys
from src.objects.objects import Button


# COLOR PALETTE -> https://www.schemecolor.com/light-gray-all-the-way-color-combination.php


pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound
pygame.font.init()

# DECLARE SCREEN SIZE

SCREEN_WIDTH = 700
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
        self.blocksize = 40  # Set the size of the grid block
        self.padding = 40
        self.box_height = 50
        self.box_font = pygame.font.Font('../src/fonts/Gamer.ttf', 70)
        self.header_font = pygame.font.Font('../src/fonts/ARCADE_R.TTF', 16)
        pygame.display.set_caption('TETRIS - GAME')

    def draw_screen(self):
        # Create the main canvas
        canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        canvas.fill((90,90,90))

        # define size for the UI

        game_canvas = (360, int(SCREEN_HEIGHT * 0.9))

        game_portion = pygame.Rect(self.padding + 10,self.padding, game_canvas[0], game_canvas[1])

        next_canvas = (200, int(SCREEN_HEIGHT * 0.35))

        next_portion = pygame.Rect(460, 40, next_canvas[0], next_canvas[1])

        information_canvas = (200, int(SCREEN_HEIGHT * 0.5))

        information_portion = pygame.Rect(460, next_canvas[1] + 80, information_canvas[0], information_canvas[1])







        # Draw the ui
        pygame.draw.rect(canvas, (25,25,25), next_portion)
        pygame.draw.rect(canvas, (90,90,90), next_portion, 2)


        pygame.draw.rect(canvas, (25,25,25),information_portion)
        pygame.draw.rect(canvas, (90,90,90), information_portion, 2)



        pygame.draw.rect(canvas, (25, 25, 25), game_portion)


        # Example text (replace with dynamic values)

        time_text = self.box_font.render("00:00", True, (180,180,180))
        score_text = self.box_font.render("00000", True, (180,180,180))
        highscore_text = self.box_font.render("00000", True, (180,180,180))


        # draw grid
        self.draw_grid(canvas.subsurface(game_portion), game_canvas[0], game_canvas[1])


        # Time Box
        time_box = pygame.Rect(480, next_canvas[1] + 115, 160, self.box_height)
        pygame.draw.rect(canvas, (25,25,25), time_box)
        pygame.draw.rect(canvas, (120,120,120), time_box, 2)

        # Time Header
        time_header_text = self.header_font.render("TIME", True, (180,180,180))
        time_header_pos = (time_box.x + (time_box.width - time_header_text.get_width()) // 2,
                           time_box.y - time_header_text.get_height() - 5)  # Position above the box
        canvas.blit(time_header_text, time_header_pos)

        canvas.blit(time_text, (time_box.x + (time_box.width - time_text.get_width()) // 2,
                                time_box.y + (time_box.height - time_text.get_height()) // 2 - 5))

        # Score Box
        score_box = pygame.Rect(480, next_canvas[1] + 195, 160, self.box_height)
        pygame.draw.rect(canvas, (25,25,25), score_box)  # White background
        pygame.draw.rect(canvas, (120,120,120), score_box, 2)  # Black border

        # Score Header
        score_header_text = self.header_font.render("SCORE", True, (180,180,180))
        score_header_pos = (score_box.x + (score_box.width - score_header_text.get_width()) // 2,
                            score_box.y - score_header_text.get_height() - 5)  # Position above the box
        canvas.blit(score_header_text, score_header_pos)

        canvas.blit(score_text, (score_box.x + (score_box.width - score_text.get_width()) // 2,
                                 score_box.y + (score_box.height - score_text.get_height()) // 2 - 5))

        # HighScore Box
        highscore_box = pygame.Rect(480, next_canvas[1] + 275, 160, self.box_height)
        pygame.draw.rect(canvas, (25,25,25), highscore_box)  # White background
        pygame.draw.rect(canvas, (120,120,120), highscore_box, 2)  # Black border

        # HighScore Header
        highscore_header_text = self.header_font.render("HIGHSCORE", True, (180,180,180))
        highscore_header_pos = (highscore_box.x + (highscore_box.width - highscore_header_text.get_width()) // 2,
                            highscore_box.y - highscore_header_text.get_height() - 5)  # Position above the box
        canvas.blit(highscore_header_text, highscore_header_pos)

        canvas.blit(highscore_text, (highscore_box.x + (highscore_box.width - highscore_text.get_width()) // 2,
                                 highscore_box.y + (highscore_box.height - highscore_text.get_height()) // 2 - 5))


        # Blit the canvas to the display
        self.screen.blit(canvas, (0, 0))

    def draw_grid(self, canvas, width, height):
        # Calculate the adjusted width and height to avoid cut-off blocks
        adjusted_width = (width // self.blocksize) * self.blocksize
        adjusted_height = (height // self.blocksize) * self.blocksize

        # Loop through each grid position
        for x in range(0, adjusted_width, self.blocksize):
            for y in range(0, adjusted_height, self.blocksize):
                rect = pygame.Rect(x, y, self.blocksize, self.blocksize)
                pygame.draw.rect(canvas, color=(80, 80, 80), rect=rect, width=1)

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


            clock.tick(60)

        # Quit Pygame after the game loop is done
        pygame.quit()


# Defining the main function
def main():
    menu = StartMenu()  # Create an instance of StartMenu
    menu.show_menu()    # Call the show_menu method on the instance


if __name__ == "__main__":
    main()

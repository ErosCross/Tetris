import pygame, sys
from src.objects.objects import *
import time
from random import choice


# Initialize pygame and its modules
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound effects
pygame.font.init()    # Initialize font rendering

# DECLARE SCREEN SIZE
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 800

# Define the clock for managing game frame rate
clock = pygame.time.Clock()

# Set the window icon
icon = pygame.image.load('../src/images/game-icon.png')
pygame.display.set_icon(icon)

# Load sound effect for button clicks
click_sound = pygame.mixer.Sound('sounds/button_pressed.wav')

class StartMenu:
    def __init__(self):
        # Initialize the start menu screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.header_font = pygame.font.Font('../src/fonts/Gamer.ttf', 200)  # Main header font

        self.button_font = pygame.font.Font('../src/fonts/Gamer.ttf', 90)  # Button font
        pygame.display.set_caption('TETRIS - BY AMIT SHAVIV')  # Set the game window title

    def draw_text(self, mytext):
        # Render the main title text
        text = self.header_font.render(mytext, True, (180, 180, 180))  # text

        # Position the text in the center of the screen
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 250))

        # Draw a line below the text
        line_start_x = SCREEN_WIDTH / 2 - text.get_width() / 2  # Left edge of the text
        line_end_x = SCREEN_WIDTH / 2 + text.get_width() / 2  # Right edge of the text
        line_y = text_rect.bottom   # Position the line 10 pixels below the text

        # Draw the line below the text
        pygame.draw.line(self.screen, (45, 45, 45), (line_start_x, line_y), (line_end_x, line_y), 2)

        self.screen.blit(text, text_rect)

    def render_button(self, text, font, color, center_position):
        # Helper method to render button text and return its position
        button_text = font.render(text, True, color)
        button_rect = button_text.get_rect(center=center_position)
        return button_text, button_rect

    def draw_buttons(self):
        # Render the menu buttons and handle their interactions
        mouse_cursor = pygame.mouse.get_pos()  # Get mouse cursor position
        mouse_buttons = pygame.mouse.get_pressed()  # Check if mouse buttons are pressed

        # Define button positions and their properties
        start_button_center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100)
        options_button_center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        exit_button_center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2  + 100)

        buttons = [
            {"text": "START", "center": start_button_center, "color": (180, 180, 180), "hover_color": (47,79,79)},
            {"text": "OPTIONS", "center": options_button_center, "color": (180, 180, 180), "hover_color": (47,79,79)},
            {"text": "EXIT", "center": exit_button_center, "color": (180, 180, 180), "hover_color": (47,79,79)}
        ]

        # Loop through all buttons and render them
        # Loop through all buttons and render them
        for button in buttons:
            # Render button text and rectangle
            text, rect = self.render_button(button["text"], self.button_font, button["color"], button["center"])


            # Check if the mouse is hovering over the button
            if rect.collidepoint(mouse_cursor):
                # Change button color on hover
                text, rect = self.render_button(button["text"], self.button_font, button["hover_color"],
                                                button["center"])

                # Play a click sound and handle button functionality when clicked
                if mouse_buttons[0]:  # Left mouse button is clicked
                    click_sound.play()

                    # Handle the EXIT button
                    if button["text"] == "EXIT":
                        pygame.time.delay(100)  # Add a small delay
                        pygame.quit()  # Quit pygame
                        sys.exit()  # Exit the script

                    # Handle the START button
                    if button["text"] == "START":
                        self.start_game()

            # Draw the button text
            self.screen.blit(text, rect)

    def draw_screen(self):
        # Set the background color to gray
        self.screen.fill((25, 25, 25))  # Gray background
        self.draw_buttons()

    def show_menu(self):
        # Main loop for displaying the start menu
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Handle quit event
                    running = False

            # Draw the menu screen
            self.draw_screen()
            self.draw_text("TETRIS")  # Draw the title text

            # Update the display
            pygame.display.flip()

            # Cap the frame rate to 60 FPS
            clock.tick(60)

        pygame.quit()  # Quit pygame after exiting the loop

    def start_game(self):
        # Start the main game by creating an instance of the Game class
        game = Game()
        game.show_game()

class Game:
    def __init__(self):
        # Initialize the game class with necessary attributes and objects
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Set up the main game window
        self.score = 0  # Initialize the score to 0
        self.blocksize = 40  # Size of each grid block
        self.padding = 40  # Padding around the game grid
        self.sprites = pygame.sprite.Group()  # Group to manage all sprite objects
        self.box_height = 50  # Height of UI boxes for score, time, etc.

        # Initialize the stopwatch (game time) variable
        self.start_time = pygame.time.get_ticks()  # Store the time when the game started
        self.elapsed_time = 0  # Initialize elapsed time

        # Load fonts for UI text
        self.box_font = pygame.font.Font('../src/fonts/Gamer.ttf', 70)
        self.header_font = pygame.font.Font('../src/fonts/ARCADE_R.TTF', 16)
        # shapes

        self.next_shapes = choice(list(TETROMINOS.keys()))

        # Initialize the field data (game grid) with zeros
        self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]

        # shapes previews

        self.shape_surfaces = {shape: load(path.join('..', 'src','images', 'graphics', f'{shape}.png')).convert_alpha() for
                               shape
                               in TETROMINOS.keys()}

        # Create the first Tetromino
        self.tetromino = Tetromino(
            choice(list(TETROMINOS.keys())),
            self.sprites,
            self.create_new_tetromino,
            self.field_data
        )

        # Initialize timers for tetromino movement
        self.timers = {
            'vertical move': Timer(UPDATE_START_SPEED, True, self.move_down),  # Timer for automatic downward movement
            'horizontal move': Timer(MOVE_WAIT_TIME), # Timer for horizontal movement delay
            'rotate' : Timer(ROTATE_WAIT_TIME) # Timer for rotations

        }
        self.timers['vertical move'].activate()  # Activate the vertical movement timer


    def display_stopwatch(self):
        # Convert elapsed time (in milliseconds) to seconds and minutes
        seconds = self.elapsed_time // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        # Format time
        time_string = f"{minutes:02}:{seconds:02}"
        return time_string


    def get_next_shape(self):
        # get next shape
        next_shape = self.next_shapes
        self.next_shapes = (choice(list(TETROMINOS.keys())))
        return next_shape

    def create_new_tetromino(self):
        # Create a new Tetromino after the current one is placed
        self.check_finished_rows()  # Check and clear completed rows
        self.tetromino = Tetromino(
            self.get_next_shape(),
            self.sprites,
            self.create_new_tetromino,
            self.field_data
        )

    def check_finished_rows(self):
        # Check for and clear any completed rows in the game grid
        delete_rows = []  # List to store indices of completed rows
        for i, row in enumerate(self.field_data):
            if all(row):  # If all blocks in a row are filled
                delete_rows.append(i)

        if delete_rows:
            for delete_row in delete_rows:
                for block in self.field_data[delete_row]:
                    block.kill()  # Remove blocks in the completed row

                # Move blocks above the completed row down
                for row in self.field_data:
                    for block in row:
                        if block and block.pos.y < delete_row:
                            block.pos.y += 1

                # Rebuild the field data
                self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
                for block in self.sprites:
                    self.field_data[int(block.pos.y)][int(block.pos.x)] = block


    def timer_update(self):
        # Update all timers to manage movement and delays
        for timer in self.timers.values():
            timer.update()
        # Update stopwatch (elapsed time)
        current_time = pygame.time.get_ticks()
        self.elapsed_time = current_time - self.start_time

    def move_down(self):
        # Move the current Tetromino down by one row
        self.tetromino.move_down()

    def game_function(self, game_surface, preview_surface):
        # Main game logic and rendering
        self.input()  # Process player input
        self.timer_update()  # Update timers
        self.sprites.draw(game_surface)  # Draw all Tetromino blocks
        self.sprites.update()  # Update movement for all sprites
        self.display_next_tetromino(preview_surface) # Show the next Tetromino



    def display_next_tetromino(self, sur):
        # Get the surface of the shape
        shape_surface = self.shape_surfaces[self.next_shapes] # Assuming shape_surfaces contains the shape to display

        # Calculate the center position
        x = (sur.get_width() - shape_surface.get_width()) // 2
        y = (sur.get_height() - shape_surface.get_height()) // 2

        # Blit the shape surface onto the given surface at the calculated position
        sur.blit(shape_surface, (x, y))

    def input(self):
        # Handle player input for Tetromino movement
        keys = pygame.key.get_pressed()


        # HORIZONTAL MOVEMENT
        if not self.timers['horizontal move'].active:
            if keys[pygame.K_LEFT]:  # Move left
                self.tetromino.move_horizontal(-1)
                self.timers['horizontal move'].activate()
            if keys[pygame.K_RIGHT]:  # Move right
                self.tetromino.move_horizontal(1)
                self.timers['horizontal move'].activate()

        # ROTATIONS
        if not self.timers['rotate'].active:
            if keys[pygame.K_UP]:
                self.tetromino.rotate()
                self.timers['rotate'].activate()

    def draw_screen(self):
        # Create and render the game screen
        canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # Main canvas
        canvas.fill((90, 90, 90))  # Background color

        # Define dimensions for different UI sections
        game_canvas = (360, int(SCREEN_HEIGHT * 0.9))
        game_portion = pygame.Rect(self.padding + 10, self.padding, game_canvas[0], game_canvas[1])
        next_canvas = (200, int(SCREEN_HEIGHT * 0.35))
        next_portion = pygame.Rect(460, 40, next_canvas[0], next_canvas[1])
        information_canvas = (200, int(SCREEN_HEIGHT * 0.5))
        information_portion = pygame.Rect(460, next_canvas[1] + 80, information_canvas[0], information_canvas[1])

        # Draw the UI sections
        pygame.draw.rect(canvas, (25, 25, 25), next_portion)
        pygame.draw.rect(canvas, (90, 90, 90), next_portion, 2)

        pygame.draw.rect(canvas, (25, 25, 25), information_portion)
        pygame.draw.rect(canvas, (90, 90, 90), information_portion, 2)
        pygame.draw.rect(canvas, (25, 25, 25), game_portion)

        self.game_function(canvas.subsurface(game_portion),canvas.subsurface(next_portion))  # Draw game components inside the game area


        # creating the texts on the screen
        time_text = self.box_font.render(self.display_stopwatch(), True, (180, 180, 180))
        score_text = self.box_font.render("00000", True, (180, 180, 180))
        highscore_text = self.box_font.render("00000", True, (180, 180, 180))
        return_text = self.box_font.render("RETURN", True, (212, 178, 178))


        hovered_return_text = self.box_font.render("RETURN", True, (230, 200, 200))

        # Draw the grid overlay
        self.draw_grid(canvas.subsurface(game_portion), game_canvas[0], game_canvas[1])

        # Draw time box
        time_box = pygame.Rect(480, next_canvas[1] + 115, 160, self.box_height)
        pygame.draw.rect(canvas, (25, 25, 25), time_box)
        pygame.draw.rect(canvas, (120, 120, 120), time_box, 2)
        time_header_text = self.header_font.render("TIME", True, (180, 180, 180))
        time_header_pos = (time_box.x + (time_box.width - time_header_text.get_width()) // 2,
                           time_box.y - time_header_text.get_height() - 5)
        canvas.blit(time_header_text, time_header_pos)
        canvas.blit(time_text, (time_box.x + (time_box.width - time_text.get_width()) // 2,
                                time_box.y + (time_box.height - time_text.get_height()) // 2 - 5))

        # Draw score box
        score_box = pygame.Rect(480, next_canvas[1] + 195, 160, self.box_height)
        pygame.draw.rect(canvas, (25, 25, 25), score_box)
        pygame.draw.rect(canvas, (120, 120, 120), score_box, 2)
        score_header_text = self.header_font.render("SCORE", True, (180, 180, 180))
        score_header_pos = (score_box.x + (score_box.width - score_header_text.get_width()) // 2,
                            score_box.y - score_header_text.get_height() - 5)
        canvas.blit(score_header_text, score_header_pos)
        canvas.blit(score_text, (score_box.x + (score_box.width - score_text.get_width()) // 2,
                                 score_box.y + (score_box.height - score_text.get_height()) // 2 - 5))

        # Draw high score box
        highscore_box = pygame.Rect(480, next_canvas[1] + 280, 160, self.box_height)
        pygame.draw.rect(canvas, (25, 25, 25), highscore_box)
        pygame.draw.rect(canvas, (120, 120, 120), highscore_box, 2)
        highscore_header_text = self.header_font.render("HIGHSCORE", True, (180, 180, 180))
        highscore_header_pos = (highscore_box.x + (highscore_box.width - highscore_header_text.get_width()) // 2,
                                highscore_box.y - highscore_header_text.get_height() - 5)
        canvas.blit(highscore_header_text, highscore_header_pos)
        canvas.blit(highscore_text, (highscore_box.x + (highscore_box.width - highscore_text.get_width()) // 2,
                                     highscore_box.y + (highscore_box.height - highscore_text.get_height()) // 2 - 5))

        # Draw return button
        mouse_cursor = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        return_box = pygame.Rect(472.5, next_canvas[1] + 400, 175, self.box_height)
        pygame.draw.rect(canvas, (255, 41, 41), return_box)
        pygame.draw.rect(canvas, (245, 83, 83), return_box, 2)
        canvas.blit(return_text, (return_box.x + (return_box.width - return_text.get_width()) // 2 + 2,
                                  return_box.y + (return_box.height - return_text.get_height()) // 2 - 5))

        # Add hover effect for return button
        if return_box.collidepoint(mouse_cursor):
            canvas.blit(hovered_return_text, (return_box.x + (return_box.width - return_text.get_width()) // 2 + 2,
                                              return_box.y + (return_box.height - return_text.get_height()) // 2 - 5))
            if mouse_buttons[0]:  # Check if left mouse button is clicked
                click_sound.play()
                self.return_back()


        # Add "Next Shape" text
        next_shape_text = self.header_font.render("NEXT SHAPE", True, (180, 180, 180))

        # Calculate the position for the text
        text_x = next_portion.x + (next_portion.width - next_shape_text.get_width()) // 2  # Center horizontally
        text_y = next_portion.y + 12  # Slightly above the next_portion rectangle



        # Blit the text onto the canvas

        canvas.blit(next_shape_text, (text_x, text_y))



        # Blit the canvas to the display
        self.screen.blit(canvas, (0, 0))

    def draw_grid(self, canvas, width, height):
        # Draw grid lines on the game canvas
        adjusted_width = (width // self.blocksize) * self.blocksize
        adjusted_height = (height // self.blocksize) * self.blocksize
        for x in range(0, adjusted_width, self.blocksize):
            for y in range(0, adjusted_height, self.blocksize):
                rect = pygame.Rect(x, y, self.blocksize, self.blocksize)
                pygame.draw.rect(canvas, color=(80, 80, 80), rect=rect, width=1)

    def return_back(self):
        # Handle return to the main menu
        menu = StartMenu()  # Create an instance of StartMenu
        menu.show_menu()

    def show_game(self):
        # Main game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Quit the game if the close button is clicked
                    running = False

            self.draw_screen()  # Draw the game screen
            pygame.display.flip()  # Update the display
            clock.tick(60)  # Maintain 60 FPS

        pygame.quit()  # Quit Pygame after the game loop


# Main function to start the game

def main():
    menu = StartMenu()  # Create an instance of StartMenu
    menu.show_menu()  # Display the main menu


if __name__ == "__main__":
    main()

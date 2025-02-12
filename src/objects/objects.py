import pygame
import os
from pygame.image import load
from os import path
import pickle


pygame.mixer.init()  # Initialize the mixer module.

CELL_SIZE = 40
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 800


SCORE_ADDITION = 10

BLOCK_OFFSET = pygame.Vector2(4,3)

YELLOW = '#f1e60d'
RED = '#e51b20'
BLUE = '#204b9b'
GREEN = '#65b32e'
PURPLE = '#7b217f'
CYAN = '#6cc6d9'
ORANGE = '#f07e13'
GRAY = '#1C1C1C'

# game behaviour
UPDATE_START_SPEED = 400 # 400
MOVE_WAIT_TIME = 200
ROTATE_WAIT_TIME = 200

# sounds

LANDING_SOUND = pygame.mixer.Sound('../src/sounds/landing.wav')  # Load the landing sound


# adjusting volume

LANDING_SOUND.set_volume(0.1)

# grid

COLUMNS = 9
ROWS = 18



TETROMINOS = {
	'T': {'shape': [(0,0), (-1,0), (1,0), (0,-1)], 'color': PURPLE},
	'O': {'shape': [(0,0), (0,-1), (1,0), (1,-1)], 'color': YELLOW},
	'J': {'shape': [(0,0), (0,-1), (0,1), (-1,1)], 'color': BLUE},
	'L': {'shape': [(0,0), (0,-1), (0,1), (1,1)], 'color': ORANGE},
	'I': {'shape': [(0,0), (0,-1), (0,-2), (0,1)], 'color': CYAN},
	'S': {'shape': [(0,0), (-1,0), (0,-1), (1,-1)], 'color': GREEN},
	'Z': {'shape': [(0,0), (1,0), (0,-1), (-1,-1)], 'color': RED}
}



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


class Slider:
    def __init__(self, x, y, width=400, height=10, initial_value=0.5, min_value=0.0, max_value=1.0, label = None, settings = None):
        """Initialize the slider with its position, size, and initial value."""
        self.settings = settings
        self.rect = pygame.Rect(x, y, width, height)
        self.value = self.settings.volume  # Current value of the slider (between min_value and max_value)
        self.min_value = min_value  # Minimum value of the slider
        self.max_value = max_value  # Maximum value of the slider
        self.handle_radius = 10  # Radius of the slider handle (circle)
        self.handle_x = self.rect.left + self.value * self.rect.width  # Position of the slider handle
        self.header_pos = [x ,y - 45] # calculating header position
        self.header_text = label # header text
        self.header_font = pygame.font.Font('fonts/Gamer.ttf', 40)


    def draw_header(self , screen):
        """Render the header text"""
        # draw the text above the slider
        text = self.header_font.render(self.header_text, True, (180, 180, 180))
        text_rect = text.get_rect(x=self.header_pos[0] , y=self.header_pos[1])
        screen.blit(text, text_rect)

    def render(self, screen, mouse_cursor, mouse_pressed):
        """Render the slider and handle mouse interaction."""
        # Draw the background slider bar (inactive)
        pygame.draw.rect(screen, (100, 100, 100), self.rect)

        # Draw the active part of the slider bar based on the current value
        active_width = self.rect.width * self.value
        pygame.draw.rect(screen, (255, 255, 250), (self.rect.left, self.rect.top, active_width, self.rect.height))

        # Handle interaction when mouse is clicked or dragged
        if self.rect.collidepoint(mouse_cursor) and mouse_pressed:
            # Calculate the new value based on mouse position on the slider
            new_value = (mouse_cursor[0] - self.rect.left) / self.rect.width
            self.value = max(self.min_value, min(new_value, self.max_value))  # Ensure the value stays within bounds

        # Recalculate handle position based on the current value
        self.handle_x = self.rect.left + self.value * self.rect.width

        # Render the header text
        self.draw_header(screen)

        # Draw the handle (circle)
        pygame.draw.circle(screen, (255, 0, 0), (int(self.handle_x), self.rect.centery), self.handle_radius)

    def get_value(self):
        """Get the current value of the slider."""
        return self.value


class CheckBox:
    def __init__(self, x, y, size=20, initial_state=False, label=None , settings = None):
        """Initialize the checkbox with its position, size, and initial state."""
        self.settings = settings
        self.font = pygame.font.Font('fonts/Gamer.ttf', 40)
        self.label = label  # Label text
        self.text_surface = self.font.render(self.label, True, (180, 180, 180))
        self.text_rect = self.text_surface.get_rect(x=x, y=y)
        self.rect = pygame.Rect(x+192.5 , y+3, size, size)
        self.checked = initial_state  # Current state of the checkbox (True or False)
        self.clicked = False  # Track if the checkbox was clicked to prevent rapid toggling

    def render(self, screen, mouse_cursor, mouse_pressed):
        """Render the checkbox and handle mouse interaction."""
        # Draw the label text above the checkbox
        screen.blit(self.text_surface, self.text_rect)

        # Draw the checkbox border
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        # Fill the checkbox if checked
        if self.checked:
            pygame.draw.rect(screen, (255, 255, 255), self.rect.inflate(-4, -4))

        # Check for interaction with debouncing
        if self.rect.collidepoint(mouse_cursor):
            if mouse_pressed and not self.clicked:
                self.checked = not self.checked  # Toggle state
                self.clicked = True  # Prevent multiple toggles per click
            elif not mouse_pressed:
                self.clicked = False  # Reset click state when mouse is released

    def is_checked(self):
        """Return whether the checkbox is checked or not."""
        return self.checked


class DropMenu:
    def __init__(self, x, y, width=200, height=40, options=None, labels=None, label=None, settings=None):
        """Initialize the dropdown menu with position, size, options, label, and settings instance."""
        self.settings = settings  # Pass the Settings instance
        self.settings.load_settings()
        self.rect = pygame.Rect(x + 140, y, width, height)
        self.options = options if options else []  # List of dropdown options
        self.selected_option = self.settings.difficulty  # Default selection
        self.is_open = False  # Dropdown state
        self.font = pygame.font.Font('fonts/Gamer.ttf', 40)
        self.label = label
        self.labels = labels
        self.label_surface = self.font.render(self.label, True, (180, 180, 180))
        self.label_rect = self.label_surface.get_rect(x=x, y=y)
        self.option_height = height  # Height of each dropdown item


    def text_label(self, option):
        """Return the label for the selected option."""
        if self.labels:
            return self.labels[int(option) - 1]
        return option

    def render(self, screen, mouse_cursor, mouse_pressed):
        """Render the dropdown menu and handle interactions."""
        # Draw the header text
        screen.blit(self.label_surface, self.label_rect)

        # Draw the main button (collapsed state)
        pygame.draw.rect(screen, (100, 100, 100), self.rect)
        text_surface = self.font.render(self.text_label(self.selected_option), True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

        # Draw the dropdown options if open
        if self.is_open:
            for index, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (index + 1) * self.option_height, self.rect.width,
                                          self.option_height)
                pygame.draw.rect(screen, (80, 80, 80), option_rect)
                option_text = self.font.render(self.text_label(option), True, (255, 255, 255))
                option_text_rect = option_text.get_rect(center=option_rect.center)
                screen.blit(option_text, option_text_rect)

                # Check for clicks on dropdown options
                if option_rect.collidepoint(mouse_cursor) and mouse_pressed:
                    self.selected_option = option
                    self.is_open = False  # Close dropdown after selection

                    # Update the settings based on the option selected
                    #if self.label == "Difficulty":
                    #    self.settings.set_difficulty(int(option))

        # Toggle dropdown when clicking the main button (only if cursor is directly over the button)
        if self.rect.collidepoint(mouse_cursor) and mouse_pressed:
            self.is_open = not self.is_open  # Toggle open/close only when the main button is clicked

    def get_selected_option(self):
        """Return the currently selected option."""
        return self.selected_option


class Block(pygame.sprite.Sprite):
    def __init__(self, group , pos, color):
        # general
        super().__init__(group)
        self.image = pygame.Surface((CELL_SIZE,CELL_SIZE))
        self.image.fill(color)
        # position
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        x = self.pos.x * CELL_SIZE
        y = self.pos.y * CELL_SIZE
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.rect.topleft = self.pos * CELL_SIZE

    def horizontal_collide(self,x , field_data):
        if not 0 <= x < COLUMNS:
            return True
        if field_data[int(self.pos.y)][x]:
            return True

    def vertical_collide(self, y , field_data):
        if y >= ROWS:
            return True
        if y >= 0 and field_data[y][int(self.pos.x)]:
            return True

    def rotate(self , pivot_pos):
        # rotate one block for rotation
        distance = self.pos - pivot_pos
        rotated = distance.rotate(90)
        new_pos = pivot_pos + rotated
        return new_pos







class Tetromino:
    def __init__(self , shape ,  group ,create_new_tetromino , field_data):
        # setup
        self.block_positions = TETROMINOS[shape]['shape']
        self.color = TETROMINOS[shape]['color']
        self.field_data = field_data
        self.shape = shape
        #create blocks

        self.blocks = [Block(group,pos,self.color) for pos in self.block_positions]

        # new tetromino
        self.create_new_tetromino = create_new_tetromino

        # settings
        self.settings = Settings()
        self.settings.load_settings()
        self.sfx = self.settings.sound_effects

    # collisions

    def next_move_horizontal_collide(self,blocks,amount):
        collision_list = [block.horizontal_collide(int(block.pos.x) + amount , self.field_data) for block in blocks]
        return True if any(collision_list) else False # CHECKS IF ANY BLOCK IS TRUE IN LIST IF SO RETURN TRUE ELSE RETURNS FALSE

    def next_move_vertical_collide(self,blocks):
        collision_list = [block.vertical_collide(int(block.pos.y) + 1 , self.field_data) for block in blocks]
        return True if any(collision_list) else False # CHECKS IF ANY BLOCK IS TRUE IN LIST IF SO RETURN TRUE ELSE RETURNS FALSE


    # movement

    def move_down(self):
        if not self.next_move_vertical_collide(self.blocks):
            for block in self.blocks:
                block.pos.y += 1
        else:
            for block in self.blocks:
                if self.sfx:
                    LANDING_SOUND.play()
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block
            self.create_new_tetromino()

    def move_horizontal(self, amount):
        # Check if moving horizontally would result in a collision
        if not self.next_move_horizontal_collide(self.blocks, amount):
            # If no collision, move all blocks by the specified amount
            for block in self.blocks:
                block.pos.x += amount


    def rotate(self):
        # Rotate tetromino
        if self.shape != 'O':
            # Take the position to rotate on
            pivot_pos = self.blocks[0].pos

            new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

            # ensure that we are not outside the boundries

            for pos in new_block_positions:
                # horizontal
                if pos.x < 0 or pos.x >= COLUMNS:
                    return

                # vertical / floor check

                if pos.y >= ROWS:
                    return
                # field check - > collision with other pieces

                if self.field_data[int(pos.y)][int(pos.x)]:
                    return


            # apply for all the blocks

            for i,block in enumerate(self.blocks):
                block.pos = new_block_positions[i]




class Timer:
    def __init__(self, duration , repeated = False , func = None):
        self.repeated = repeated
        self.func = func
        self.duration = duration

        self.start_time = 0
        self.active = False


    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration and self.active:

            if self.func and self.start_time != 0:
                self.func()


            # reset timer
            self.deactivate()

            # repeat the timer
            if self.repeated:
                self.activate()




class Settings:
    def __init__(self):
        pygame.mixer.init()
        self.volume = 0.5
        self.sound_effects = True
        self.difficulty = 1
        self.highscore = 0  # Initialize the highscore
        pygame.mixer.music.set_volume(self.volume)

    def adjust_volume(self, volume_level):
        """Adjust the music volume level."""
        if 0.0 <= volume_level <= 1.0:
            self.volume = volume_level
            pygame.mixer.music.set_volume(self.volume)
            print(f"Music Volume set to {self.volume * 100}%")
        else:
            print("Volume level must be between 0.0 and 1.0.")

    def toggle_sound_effects(self):
        """Toggle sound effects on or off."""
        self.sound_effects = not self.sound_effects
        state = "enabled" if self.sound_effects else "disabled"
        self.save_settings()
        print(f"Sound Effects {state}")

    def set_difficulty(self, difficulty_level):
        """Set the difficulty level."""
        if 1 <= difficulty_level <= 4:
            self.difficulty = difficulty_level
            self.save_settings()
            print(f"Difficulty set to {self.difficulty}")
        else:
            print("Difficulty level must be between 1 and 4.")

    def update_highscore(self, score):
        """Update the highscore if the current score is higher."""
        if score > self.highscore:
            self.highscore = score
            self.save_settings()
            print(f"New Highscore: {self.highscore}")
        else:
            print(f"Highscore remains: {self.highscore}")

    def save_settings(self, filename="settings.pkl"):
        """Export settings to a binary pickle file."""
        settings_dict = {
            "volume": self.volume,
            "sound_effects_enabled": self.sound_effects,
            "difficulty": self.difficulty,
            "highscore": self.highscore  # Save the highscore
        }
        try:
            with open(filename, "wb") as f:
                pickle.dump(settings_dict, f)
            print(f"Settings saved to {filename}")
        except Exception as e:
            print(f"Error saving settings: {e}")

    def load_settings(self, filename="settings.pkl"):
        """Load settings from a pickle file."""
        if not os.path.exists(filename):
            print("Settings file not found. Creating default settings file.")
            self.create_default_settings(filename)
            return

        try:
            with open(filename, "rb") as f:
                settings_dict = pickle.load(f)
                self.volume = settings_dict.get("volume", 0.5)
                self.sound_effects = settings_dict.get("sound_effects_enabled", True)
                self.difficulty = settings_dict.get("difficulty", 1)
                self.highscore = settings_dict.get("highscore", 0)  # Load highscore
                pygame.mixer.music.set_volume(self.volume)
                print(
                    f"Settings loaded. Volume: {self.volume * 100}%, Sound Effects: {'Enabled' if self.sound_effects else 'Disabled'}, Difficulty: {self.difficulty}, Highscore: {self.highscore}")
        except (FileNotFoundError, pickle.UnpicklingError) as e:
            print(f"Error loading settings: {e}")
            print("Using default values.")

    def create_default_settings(self, filename="settings.pkl"):
        """Create a default settings file."""
        default_settings = {
            "volume": 0.5,
            "sound_effects_enabled": True,
            "difficulty": 1,
            "highscore": 0
        }
        try:
            with open(filename, "wb") as f:
                pickle.dump(default_settings, f)
            print(f"Default settings created and saved to {filename}.")
        except Exception as e:
            print(f"Error creating default settings: {e}")

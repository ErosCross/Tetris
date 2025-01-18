import pygame



CELL_SIZE = 40
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 800

BLOCK_OFFSET = pygame.Vector2(3,4)

YELLOW = '#f1e60d'
RED = '#e51b20'
BLUE = '#204b9b'
GREEN = '#65b32e'
PURPLE = '#7b217f'
CYAN = '#6cc6d9'
ORANGE = '#f07e13'
GRAY = '#1C1C1C'
LINE_COLOR = '#FFFFFF'

# game behaviour
UPDATE_START_SPEED = 500
MOVE_WAIT_TIME = 300
ROTATE_WAIT_TIME = 200

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

    def horizontal_collide(self,x):
        if not 0 <= x < COLUMNS:
            return True

    def vertical_collide(self, y):
        if y >= ROWS:
            return True







class Tetromino:
    def __init__(self , shape ,  group ,create_new_tetromino):
        # setup
        self.block_positions = TETROMINOS[shape]['shape']
        self.color = TETROMINOS[shape]['color']

        #create blocks

        self.blocks = [Block(group,pos,self.color) for pos in self.block_positions]

        # new tetromino
        self.create_new_tetromino = create_new_tetromino

    # collisions

    def next_move_horizontal_collide(self,blocks,amount):
        collision_list = [block.horizontal_collide(int(block.pos.x) + amount) for block in blocks]
        return True if any(collision_list) else False # CHECKS IF ANY BLOCK IS TRUE IN LIST IF SO RETURN TRUE ELSE RETURNS FALSE

    def next_move_vertical_collide(self,blocks):
        collision_list = [block.vertical_collide(int(block.pos.y) + 1) for block in blocks]
        return True if any(collision_list) else False # CHECKS IF ANY BLOCK IS TRUE IN LIST IF SO RETURN TRUE ELSE RETURNS FALSE


    # movement

    def move_down(self):
        if not self.next_move_vertical_collide(self.blocks):
            for block in self.blocks:
                block.pos.y += 1

    def move_horizontal(self, amount):
        # Check if moving horizontally would result in a collision
        if not self.next_move_horizontal_collide(self.blocks, amount):
            # If no collision, move all blocks by the specified amount
            for block in self.blocks:
                block.pos.x += amount
        else:
            self.create_new_tetromino()



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











import pygame
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Game dimensions
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 8)  # Extra space for score and next piece
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

# Colors for each shape
SHAPE_COLORS = [CYAN, YELLOW, MAGENTA, ORANGE, BLUE, GREEN, RED]

class Tetromino:
    def __init__(self):
        self.rotation = 0
        self.shape_index = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[self.shape_index]
        self.color = SHAPE_COLORS[self.shape_index]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        # Create a new rotated shape
        rows = len(self.shape)
        cols = len(self.shape[0])
        rotated = [[self.shape[rows-1-j][i] for j in range(rows)] for i in range(cols)]
        return rotated

class Game:
    def __init__(self):
        self.reset_game()
        self.clock = pygame.time.Clock()
    
    def reset_game(self):
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = Tetromino()
        self.game_over = False
        self.paused = False
        self.sound_on = True
        self.score = 0
        self.lines_cleared = 0
        self.fall_time = 0
        self.fall_speed = 500  # Time in milliseconds
        self.next_piece = Tetromino()
        self.start_music()
    
    def start_music(self):
        try:
            # Create simple beep sound using pygame only
            sample_rate = 22050
            duration = 0.5
            frequency = 440
            frames = int(duration * sample_rate)
            # Create simple sine wave manually
            import math
            arr = []
            for i in range(frames):
                wave = math.sin(2 * math.pi * frequency * i / sample_rate)
                arr.append([int(wave * 32767 * 0.3), int(wave * 32767 * 0.3)])
            self.music_sound = pygame.sndarray.make_sound(arr)
            if self.sound_on:
                self.music_sound.play(loops=-1)
        except:
            self.music_sound = None
    
    def toggle_music(self):
        if hasattr(self, 'music_sound') and self.music_sound:
            if self.sound_on:
                pygame.mixer.stop()
                self.music_sound.play(loops=-1)
            else:
                pygame.mixer.stop()

    def valid_move(self, piece, x, y):
        for i in range(len(piece)):
            for j in range(len(piece[0])):
                if piece[i][j]:
                    if (x + j < 0 or x + j >= GRID_WIDTH or 
                        y + i >= GRID_HEIGHT or 
                        (y + i >= 0 and self.grid[y + i][x + j] != BLACK)):
                        return False
        return True

    def lock_piece(self):
        for i in range(len(self.current_piece.shape)):
            for j in range(len(self.current_piece.shape[0])):
                if self.current_piece.shape[i][j]:
                    if self.current_piece.y + i < 0:
                        self.game_over = True
                        return
                    self.grid[self.current_piece.y + i][self.current_piece.x + j] = self.current_piece.color
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = Tetromino()
        
        # Check if new piece can be placed (game over condition)
        if not self.valid_move(self.current_piece.shape, self.current_piece.x, self.current_piece.y):
            self.game_over = True

    def clear_lines(self):
        lines_cleared = 0
        y = GRID_HEIGHT - 1
        while y >= 0:
            if all(cell != BLACK for cell in self.grid[y]):
                lines_cleared += 1
                for yy in range(y, 0, -1):
                    self.grid[yy] = self.grid[yy-1][:]
                self.grid[0] = [BLACK] * GRID_WIDTH
            else:
                y -= 1
        
        if lines_cleared > 0:
            self.lines_cleared += lines_cleared
            self.score += (100 * lines_cleared) * lines_cleared  # More points for multiple lines

    def draw(self):
        screen.fill(BLACK)
        
        # Draw grid
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pygame.draw.rect(screen, self.grid[y][x],
                               (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        # Draw current piece
        if self.current_piece:
            for i in range(len(self.current_piece.shape)):
                for j in range(len(self.current_piece.shape[0])):
                    if self.current_piece.shape[i][j]:
                        pygame.draw.rect(screen, self.current_piece.color,
                                       ((self.current_piece.x + j) * BLOCK_SIZE,
                                        (self.current_piece.y + i) * BLOCK_SIZE,
                                        BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        # Draw next piece preview section
        preview_x = GRID_WIDTH * BLOCK_SIZE + 20
        preview_y = 80
        
        # Draw "NEXT" label
        font = pygame.font.Font(None, 28)
        next_text = font.render('NEXT', True, WHITE)
        screen.blit(next_text, (preview_x, preview_y - 30))
        
        # Draw preview box with background
        box_width = 5 * BLOCK_SIZE
        box_height = 4 * BLOCK_SIZE
        pygame.draw.rect(screen, (40, 40, 40), (preview_x, preview_y, box_width, box_height))
        pygame.draw.rect(screen, WHITE, (preview_x, preview_y, box_width, box_height), 2)
        
        # Center the next piece in the preview box
        piece_width = len(self.next_piece.shape[0]) * BLOCK_SIZE
        piece_height = len(self.next_piece.shape) * BLOCK_SIZE
        center_x = preview_x + (box_width - piece_width) // 2
        center_y = preview_y + (box_height - piece_height) // 2
        
        for i in range(len(self.next_piece.shape)):
            for j in range(len(self.next_piece.shape[0])):
                if self.next_piece.shape[i][j]:
                    pygame.draw.rect(screen, self.next_piece.color,
                                   (center_x + j * BLOCK_SIZE,
                                    center_y + i * BLOCK_SIZE,
                                    BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        # Draw score
        score_text = font.render(f'SCORE', True, WHITE)
        screen.blit(score_text, (preview_x, preview_y + 160))
        score_value = font.render(f'{self.score}', True, WHITE)
        screen.blit(score_value, (preview_x, preview_y + 185))
        
        # Draw controls
        controls_font = pygame.font.Font(None, 20)
        controls_y = preview_y + 230
        controls = [
            'CONTROLS:',
            '← → Move',
            '↓ Drop',
            '↑ Rotate'
        ]
        for i, control in enumerate(controls):
            color = WHITE if i == 0 else (200, 200, 200)
            control_text = controls_font.render(control, True, color)
            screen.blit(control_text, (preview_x, controls_y + i * 18))
        
        # Draw additional scoring info
        score_info_y = controls_y + 100
        score_info = [
            'STATS:',
            f'Lines: {self.lines_cleared}',
            f'Level: {self.lines_cleared // 10 + 1}'
        ]
        for i, info in enumerate(score_info):
            color = WHITE if i == 0 else (200, 200, 200)
            info_text = controls_font.render(info, True, color)
            screen.blit(info_text, (preview_x, score_info_y + i * 18))
        
        # Draw game control buttons
        buttons_y = score_info_y + 80
        button_font = pygame.font.Font(None, 18)
        buttons = [
            'GAME:',
            f'P - {"Resume" if self.paused else "Pause"}',
            'R - Reset',
            f'S - Sound {"ON" if self.sound_on else "OFF"}'
        ]
        for i, button in enumerate(buttons):
            color = WHITE if i == 0 else (180, 180, 180)
            button_text = button_font.render(button, True, color)
            screen.blit(button_text, (preview_x, buttons_y + i * 16))

        pygame.display.flip()

    def run(self):
        while not self.game_over:
            self.fall_time += self.clock.get_rawtime()
            self.clock.tick()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                    elif event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_s:
                        self.sound_on = not self.sound_on
                        self.toggle_music()
                    elif not self.paused:
                        if event.key == pygame.K_LEFT:
                            if self.valid_move(self.current_piece.shape, 
                                             self.current_piece.x - 1, 
                                             self.current_piece.y):
                                self.current_piece.x -= 1
                        elif event.key == pygame.K_RIGHT:
                            if self.valid_move(self.current_piece.shape, 
                                             self.current_piece.x + 1, 
                                             self.current_piece.y):
                                self.current_piece.x += 1
                        elif event.key == pygame.K_DOWN:
                            if self.valid_move(self.current_piece.shape, 
                                             self.current_piece.x, 
                                             self.current_piece.y + 1):
                                self.current_piece.y += 1
                        elif event.key == pygame.K_UP:
                            rotated = self.current_piece.rotate()
                            if self.valid_move(rotated, 
                                             self.current_piece.x, 
                                             self.current_piece.y):
                                self.current_piece.shape = rotated

            # Handle automatic falling (only when not paused)
            if not self.paused and self.fall_time >= self.fall_speed:
                if self.valid_move(self.current_piece.shape, 
                                 self.current_piece.x, 
                                 self.current_piece.y + 1):
                    self.current_piece.y += 1
                else:
                    self.lock_piece()
                self.fall_time = 0

            self.draw()

        # Game over screen with options
        while self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        return self.run()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        return
            
            screen.fill(BLACK)
            font = pygame.font.Font(None, 48)
            game_over_text = font.render('GAME OVER!', True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 60))
            
            menu_font = pygame.font.Font(None, 24)
            restart_text = menu_font.render('Press R to Restart', True, WHITE)
            quit_text = menu_font.render('Press Q to Quit', True, WHITE)
            screen.blit(restart_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 20))
            screen.blit(quit_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 50))
            
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
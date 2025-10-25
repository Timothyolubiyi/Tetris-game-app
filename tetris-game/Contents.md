# Tetris Game Development Process

## Table of Contents
1. [Project Setup](#project-setup)
2. [Game Components](#game-components)
3. [Implementation Steps](#implementation-steps)
4. [Code Breakdown](#code-breakdown)
5. [Testing and Debugging](#testing-and-debugging)

## Project Setup

### 1. Environment Setup
```bash
# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate

# Install required package
pip install pygame
```

### 2. Project Structure
```
tetris-game/
├── tetris.py        # Main game file
├── README.md        # Game documentation
└── Contents.md      # Development documentation
```

## Game Components

### 1. Constants and Configurations
```python
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
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 8)
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT
```

### 2. Tetromino Shapes Definition
```python
SHAPES = [
    [[1, 1, 1, 1]],          # I-piece
    [[1, 1], [1, 1]],        # O-piece
    [[1, 1, 1], [0, 1, 0]],  # T-piece
    [[1, 1, 1], [1, 0, 0]],  # L-piece
    [[1, 1, 1], [0, 0, 1]],  # J-piece
    [[1, 1, 0], [0, 1, 1]],  # S-piece
    [[0, 1, 1], [1, 1, 0]]   # Z-piece
]

SHAPE_COLORS = [CYAN, YELLOW, MAGENTA, ORANGE, BLUE, GREEN, RED]
```

## Implementation Steps

### 1. Tetromino Class Implementation
The `Tetromino` class handles individual tetris pieces:

```python
class Tetromino:
    def __init__(self):
        self.rotation = 0
        self.shape_index = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[self.shape_index]
        self.color = SHAPE_COLORS[self.shape_index]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        rows = len(self.shape)
        cols = len(self.shape[0])
        rotated = [[self.shape[rows-1-j][i] for j in range(rows)] 
                   for i in range(cols)]
        return rotated
```

### 2. Game Class Implementation
The main game logic is handled by the `Game` class:

```python
class Game:
    def __init__(self):
        self.reset_game()
        self.clock = pygame.time.Clock()
    
    def reset_game(self):
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] 
                     for _ in range(GRID_HEIGHT)]
        self.current_piece = Tetromino()
        self.game_over = False
        self.paused = False
        self.sound_on = True
        self.score = 0
        self.lines_cleared = 0
        self.fall_time = 0
        self.fall_speed = 500
        self.next_piece = Tetromino()
        self.start_music()
```

### 3. Core Game Functions

#### Movement and Collision Detection
```python
def valid_move(self, piece, x, y):
    for i in range(len(piece)):
        for j in range(len(piece[0])):
            if piece[i][j]:
                if (x + j < 0 or x + j >= GRID_WIDTH or 
                    y + i >= GRID_HEIGHT or 
                    (y + i >= 0 and self.grid[y + i][x + j] != BLACK)):
                    return False
    return True
```

#### Piece Locking
```python
def lock_piece(self):
    for i in range(len(self.current_piece.shape)):
        for j in range(len(self.current_piece.shape[0])):
            if self.current_piece.shape[i][j]:
                if self.current_piece.y + i < 0:
                    self.game_over = True
                    return
                self.grid[self.current_piece.y + i][self.current_piece.x + j] = \
                    self.current_piece.color
    self.clear_lines()
    self.current_piece = self.next_piece
    self.next_piece = Tetromino()
```

#### Line Clearing
```python
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
        self.score += (100 * lines_cleared) * lines_cleared
```

### 4. Graphics and UI

#### Drawing the Game State
```python
def draw(self):
    screen.fill(BLACK)
    
    # Draw grid
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(screen, self.grid[y][x],
                           (x * BLOCK_SIZE, y * BLOCK_SIZE, 
                            BLOCK_SIZE - 1, BLOCK_SIZE - 1))

    # Draw current piece
    if self.current_piece:
        for i in range(len(self.current_piece.shape)):
            for j in range(len(self.current_piece.shape[0])):
                if self.current_piece.shape[i][j]:
                    pygame.draw.rect(screen, self.current_piece.color,
                                   ((self.current_piece.x + j) * BLOCK_SIZE,
                                    (self.current_piece.y + i) * BLOCK_SIZE,
                                    BLOCK_SIZE - 1, BLOCK_SIZE - 1))
```

### 5. Game Loop Implementation
```python
def run(self):
    while not self.game_over:
        self.fall_time += self.clock.get_rawtime()
        self.clock.tick()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.KEYDOWN:
                self.handle_input(event.key)

        # Update game state
        if not self.paused:
            self.update_game_state()

        # Draw everything
        self.draw()
        pygame.display.flip()
```

## Testing and Debugging

### Key Areas to Test
1. Piece Movement
   - Left/Right movement
   - Rotation
   - Downward movement
   - Collision detection

2. Game Mechanics
   - Line clearing
   - Score calculation
   - Level progression
   - Game over conditions

3. UI Elements
   - Score display
   - Next piece preview
   - Game over screen
   - Pause menu

### Common Issues and Solutions
1. Rotation near walls
   - Implement wall kick system
   - Check boundary conditions

2. Piece spawning
   - Center alignment
   - Overflow checking

3. Performance
   - Optimize drawing routines
   - Reduce unnecessary calculations

## Additional Features Implementation

### 1. Sound System
```python
def start_music(self):
    try:
        sample_rate = 22050
        duration = 0.5
        frequency = 440
        frames = int(duration * sample_rate)
        arr = []
        for i in range(frames):
            wave = math.sin(2 * math.pi * frequency * i / sample_rate)
            arr.append([int(wave * 32767 * 0.3), 
                       int(wave * 32767 * 0.3)])
        self.music_sound = pygame.sndarray.make_sound(arr)
        if self.sound_on:
            self.music_sound.play(loops=-1)
    except:
        self.music_sound = None
```

### 2. Game Statistics
```python
def update_statistics(self):
    self.level = self.lines_cleared // 10 + 1
    self.fall_speed = max(50, 500 - (self.level - 1) * 20)
```

## Running the Game

To start the game:
```python
if __name__ == "__main__":
    game = Game()
    game.run()
```

<img width="799" height="952" alt="Image" src="https://github.com/user-attachments/assets/a8ae453e-f34d-49b8-b7b7-fad2c45824c3" />

This documentation covers the complete development process of the Tetris game, from setup to implementation. Each component is explained with relevant code snippets and implementation details.

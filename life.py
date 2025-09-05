# life.py
import argparse
import pygame
import numpy as np
import sys
from scipy import signal

# Initialize argparse
parser = argparse.ArgumentParser(description="Conway's Game of Life")
parser.add_argument('--width', type=int, default=800, help='Width of the window (in pixels)')
parser.add_argument('--height', type=int, default=600, help='Height of the window (in pixels)')
parser.add_argument('--fps', type=int, default=10, help='Frames per second')
args = parser.parse_args()

# Constants derived from args
WIDTH, HEIGHT = args.width, args.height
CELL_SIZE = 8  # Size of one cell in pixels
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
FPS = args.fps

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)

def create_board(rows, cols, random=False):
    """Creates a new board. If random=True, initializes with random alive cells."""
    if random:
        return np.random.choice([0, 1], size=(rows, cols), p=[0.8, 0.2])
    else:
        return np.zeros((rows, cols), dtype=int)

def update_board(board):
    """
    Applies the rules of Conway's Game of Life to create a new generation.
    Does NOT mutate the original board.
    """
    # Copy the board
    new_board = board.copy()
    # Count neighbors for every cell using convolution
    kernel = np.array([[1, 1, 1],
                       [1, 0, 1],
                       [1, 1, 1]])
    neighbor_count = signal.convolve2d(board, kernel, mode='same', boundary='wrap')

    # Apply the rules
    # Rule 1 & 3: Die if underpopulated or overpopulated
    new_board[(board == 1) & ((neighbor_count < 2) | (neighbor_count > 3))] = 0
    # Rule 4: A dead cell becomes alive if it has exactly 3 neighbors
    new_board[(board == 0) & (neighbor_count == 3)] = 1
    # Rule 2: Live on is already handled by the copy. Cells that don't meet the conditions above stay the same.

    return new_board

def draw_grid(surface, board):
    """Draws the grid lines and the live cells."""
    surface.fill(BLACK)
    # Draw live cells
    for row in range(board.shape[0]):
        for col in range(board.shape[1]):
            if board[row, col] == 1:
                pygame.draw.rect(surface, GREEN, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    # Draw grid lines
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(surface, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, GRAY, (0, y), (WIDTH, y))

def draw_ui(surface, generation, live_count, paused):
    """Draws the UI overlay with stats and controls."""
    font = pygame.font.SysFont('Arial', 16)
    # Create UI background
    ui_rect = pygame.Rect(0, 0, WIDTH, 20)
    pygame.draw.rect(surface, (50, 50, 50), ui_rect)
    # Generation text
    gen_text = font.render(f'Gen: {generation}', True, WHITE)
    live_text = font.render(f'Live: {live_count}', True, WHITE)
    status = "PAUSED" if paused else "RUNNING"
    status_text = font.render(f'Status: {status}', True, WHITE)
    # Blit texts to the screen
    surface.blit(gen_text, (5, 2))
    surface.blit(live_text, (100, 2))
    surface.blit(status_text, (200, 2))
    # Draw controls hint at the top right
    controls_text = font.render('Space: Play/Pause  N:Step  R:Random  C:Clear  S:Save  L:Load', True, WHITE)
    surface.blit(controls_text, (WIDTH - controls_text.get_width() - 5, 2))

def save_pattern(board):
    """Saves the current pattern to a file 'pattern.cells'."""
    try:
        with open('pattern.cells', 'w') as f:
            # Write a header
            f.write("# Saved pattern\n")
            # Find all live cells and write their coordinates
            live_cells = np.argwhere(board == 1)
            for cell in live_cells:
                # Format: col,row (x,y) as per the example
                f.write(f"{cell[1]},{cell[0]}\n")
        print("Pattern saved to 'pattern.cells'")
    except IOError:
        print("Error: Could not save file.")

def load_pattern():
    """Loads a pattern from 'pattern.cells'."""
    new_board = create_board(GRID_HEIGHT, GRID_WIDTH) # Start with an empty board
    try:
        with open('pattern.cells', 'r') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if line.startswith('#') or not line:
                    continue
                # Parse coordinates
                try:
                    col, row = map(int, line.split(','))
                    # Place the cell if it's within bounds
                    if 0 <= row < GRID_HEIGHT and 0 <= col < GRID_WIDTH:
                        new_board[row, col] = 1
                except ValueError:
                    print(f"Skipping invalid line: {line}")
        print("Pattern loaded from 'pattern.cells'")
    except FileNotFoundError:
        print("Error: File 'pattern.cells' not found.")
    return new_board

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Conway's Game of Life")
    clock = pygame.time.Clock()

    # Initialize the board
    board = create_board(GRID_HEIGHT, GRID_WIDTH)
    generation = 0
    paused = True
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Handle key presses
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_n and paused:
                    # Single step
                    board = update_board(board)
                    generation += 1
                elif event.key == pygame.K_r:
                    # Random fill
                    board = create_board(GRID_HEIGHT, GRID_WIDTH, random=True)
                    generation = 0
                elif event.key == pygame.K_c:
                    # Clear board
                    board = create_board(GRID_HEIGHT, GRID_WIDTH)
                    generation = 0
                elif event.key == pygame.K_s:
                    # Save pattern
                    save_pattern(board)
                elif event.key == pygame.K_l:
                    # Load pattern
                    board = load_pattern()
                    generation = 0
            # Optional: Add mouse click to toggle cells
            elif event.type == pygame.MOUSEBUTTONDOWN and paused:
                x, y = pygame.mouse.get_pos()
                col, row = x // CELL_SIZE, y // CELL_SIZE
                # Toggle the cell state
                if 0 <= row < GRID_HEIGHT and 0 <= col < GRID_WIDTH:
                    board[row, col] = 1 - board[row, col]

        # Update the game state if not paused
        if not paused:
            board = update_board(board)
            generation += 1

        # Draw everything
        draw_grid(screen, board)
        live_count = np.sum(board) # Calculate live cells for UI
        draw_ui(screen, generation, live_count, paused)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

# Conway's Game of Life

A Python implementation of Conway's Game of Life with an interactive Pygame visualization.

## Features
- Interactive grid: Draw cells with the mouse.
- Controls: Play/Pause (SPACE), Step (N), Clear (C), Random (R), Save (S), Load (L).
- Pattern persistence: Save and load patterns to/from `.cells` files.
- Wrap-around edges.

## How to Run
1. Install dependencies: `pip install pygame numpy scipy`
2. Run the program: `python life.py --width 800 --height 600 --fps 10`
# PATHFINDING VISUALIZATION SYSTEM

## Overview

This project is a comprehensive, production-quality AI Pathfinder Visualization System built with Pygame. It visualizes multiple uninformed and informed search algorithms on a 2D grid, animating their step-by-step progress with real-time metrics, and supports dynamic re-planning when obstacles appear during agent movement.

## Key Features Implemented

### 1. Environment & Grid Logic
- **Dynamic Grid Sizing**: Create grids of any size (default 20x20) by modifying `GRID_ROWS` and `GRID_COLS` in `main.py`
- **Fixed Start & Goal Nodes**: Start at (0,0) and Goal at (rows-1, cols-1) - remain constant across map changes
- **Interactive Editor**: Click on grid cells to place/remove obstacle walls in real-time
- **Random Map Generation**: Press `G` to generate a random obstacle map with 30% density (customizable)

### 2. Pathfinding Algorithms & Heuristics
**Algorithms Available:**
- **A* Search** - Press `1` 
- **Greedy Best-First Search (GBFS)** - Press `2`

**Heuristics Available (for A* and GBFS):**
- **Manhattan Distance**: h(n) = |x₁ - x₂| + |y₁ - y₂|
- **Euclidean Distance**: h(n) = √((x₁ - x₂)² + (y₁ - y₂)²)

**Algorithm Formulas:**
- **A***: f(n) = g(n) + h(n) where g(n) = cost from start, h(n) = heuristic estimate (optimal pathfinding)
- **GBFS**: f(n) = h(n) (heuristic only, ignores actual cost; faster but may not be optimal)

### 3. Visualization & GUI Elements
- **Color-Coded Nodes:**
  - 🟢 **Green**: Start node
  - 🔴 **Red**: Goal node
  - 🟡 **Yellow**: Frontier (next nodes to explore)
  - 🔵 **Blue**: Visited/Explored nodes
  - 🟢 **Bright Green**: Final optimal path
  - ⬛ **Black**: Obstacle walls
  - ⚪ **White**: Empty cells

- **Metrics Dashboard:** Real-time display showing:
  - Total Nodes Visited
  - Final Path Cost (sum of edge weights)
  - Execution Time (in milliseconds)

### 4. Dynamic Mode & Re-planning (Crucial Feature)
- **Toggle Dynamic Mode**: Press `D` to enable/disable dynamic mode
- **Obstacle Spawning**: When enabled and agent moves, new obstacles spawn randomly (2% chance per step)
- **Collision Detection**: System automatically detects if spawned obstacles block the current path
- **Re-planning Mechanism**: If a newly spawned obstacle obstructs the remaining path:
  - Agent stops immediately
  - System calculates a new path from current position to goal
  - Agent continues with the new path
- **Efficiency**: Re-planning only triggered if new obstacle actually blocks the current path

## Installation

1. Ensure Python 3.7+ is installed
2. Install Pygame:
   ```
   pip install pygame
   ```

## How to Run

1. Navigate to the project directory:
   ```
   cd "d:\AI Assignments\A2Q6"
   ```
2. Run the application:
   ```
   python main.py
   ```

## Controls

### Algorithm Selection
- `1` - A* Search with Heuristic
- `2` - Greedy Best-First Search with Heuristic

### Heuristic Control
- `H` - Toggle heuristic (Manhattan ↔ Euclidean) for A* or GBFS

### Grid & Map Control
- `Left Click` - Place/remove obstacle walls
- `R` - Reset grid (clear all obstacles)
- `G` - Generate random map with 30% obstacles

### Execution & Mode Control
- `SPACE` - Run selected algorithm
- `D` - Toggle Dynamic Mode ON/OFF
- `Q` - Quit application

## Configuration

### Customize Grid Size
Edit `main.py`:
```python
GRID_ROWS = 20  # Change to desired number of rows
GRID_COLS = 20  # Change to desired number of columns
```

### Customize Dynamic Mode Obstacle Spawn Rate
Edit `grid.py` in the `Grid` class:
```python
self.obstacle_spawn_probability = 0.15  # Change to 0.05 for 5% chance, 0.20 for 20% chance, etc.
```

### Customize Random Map Density
Edit `main.py` where `G` is pressed:
```python
generate_random_obstacles(grid, density=0.3)  # Change 0.3 to desired density (0.0-1.0)
```

## Project Structure

```
├── main.py                 # Main application and event loop
├── grid.py                 # Grid class with wall management and dynamic spawning
├── gui.py                  # Pygame GUI and visualization
├── node.py                 # Node class for search algorithms
├── utils.py                # Utility functions (heuristics, moves, colors)
├── algorithms/
│   ├── astar.py           # A* Algorithm
│   └── gbfs.py            # Greedy Best-First Search
├── test_implementation.py  # Comprehensive test suite
└── README.md              # This file
```

## Algorithm Comparison

| Algorithm | Optimal | Complete | Time Complexity | Space Complexity |
|-----------|---------|----------|-----------------|------------------|
| **A*** | Yes | Yes | O(b^d) | O(b^d) |
| **GBFS** | No | No | O(b^m) | O(b^m) |

### A* vs GBFS
- **A***: Uses f(n) = g(n) + h(n). Guarantees optimal path. Expands nodes based on actual cost + heuristic estimate.
- **GBFS**: Uses f(n) = h(n). Does NOT guarantee optimal path. Expands nodes based only on heuristic estimate, making it faster but potentially suboptimal.
- **When to use A***: When you need the shortest path
- **When to use GBFS**: When speed is more important than optimality



## Performance Notes

- **A* vs GBFS**: A* is optimal (finds shortest path), GBFS is faster but may not find shortest path
- **Manhattan vs Euclidean**: Euclidean provides tighter bounds but more computation
- **Dynamic Mode**: Performance depends on obstacle spawn probability; set conservatively for real-time performance


## Movement Rules

Movement is allowed in the following strict order:

1. Up → (-1, 0)
2. Right → (0, 1)
3. Down → (1, 0)
4. Left → (0, -1)
5. Bottom-Right → (1, 1)
6. Top-Left → (-1, -1)

No other diagonals or movement orders are permitted.

## Notes

- All algorithms animate their progress step-by-step.
---

# utils.py
import math
import random

MOVES = [
    (-1, 0),   # Up
    (0, 1),    # Right
    (1, 0),    # Down
    (0, -1),   # Left
    (1, 1),    # Bottom-Right
    (-1, -1)   # Top-Left
]

COLOR_MAP = {
    "start": (0, 200, 0),
    "target": (200, 0, 0),
    "wall": (0, 0, 0),
    "empty": (255, 255, 255),
    "frontier": (255, 255, 0),
    "explored": (0, 0, 200),
    "path": (0, 255, 0)
}

def move_cost(from_pos, to_pos):
    dr = abs(from_pos[0] - to_pos[0])
    dc = abs(from_pos[1] - to_pos[1])
    if dr == 1 and dc == 1:
        return math.sqrt(2)
    return 1

def manhattan_distance(pos1, pos2):
    """Manhattan distance heuristic"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def euclidean_distance(pos1, pos2):
    """Euclidean distance heuristic"""
    dr = abs(pos1[0] - pos2[0])
    dc = abs(pos1[1] - pos2[1])
    return math.sqrt(dr * dr + dc * dc)

def generate_random_obstacles(grid, density=0.3):
    """Generate random obstacles on the grid with specified density (0.0 to 1.0)"""
    for r in range(grid.rows):
        for c in range(grid.cols):
            if (r, c) != grid.start and (r, c) != grid.target:
                if random.random() < density:
                    grid.set_wall(r, c)

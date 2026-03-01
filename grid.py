# grid.py
from utils import MOVES
import random

class Grid:
    def __init__(self, rows=20, cols=20):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.start = (0, 0)
        self.target = (rows - 1, cols - 1)
        self.dynamic_mode = False
        self.obstacle_spawn_probability = 0.15  # 15% chance per step

    def reset(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def set_wall(self, row, col):
        if (row, col) != self.start and (row, col) != self.target:
            self.grid[row][col] = 1

    def remove_wall(self, row, col):
        self.grid[row][col] = 0

    def is_wall(self, row, col):
        return self.grid[row][col] == 1

    def in_bounds(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def neighbors(self, row, col):
        for dr, dc in MOVES:
            nr, nc = row + dr, col + dc
            if self.in_bounds(nr, nc) and not self.is_wall(nr, nc):
                yield (nr, nc)
    
    def spawn_random_obstacle(self):
        """Spawn a random obstacle on the grid during dynamic mode"""
        if random.random() < self.obstacle_spawn_probability:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if (r, c) != self.start and (r, c) != self.target:
                return self.set_wall(r, c), (r, c)
        return None, None
    
    def path_obstructed(self, path):
        """Check if any obstacles in path are walls, return obstructed position or None"""
        for r, c in path:
            if self.is_wall(r, c):
                return (r, c)
        return None


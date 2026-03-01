# gui.py
import pygame
from utils import COLOR_MAP

CELL_SIZE = 28
MARGIN = 2
FONT_SIZE = 12

class GUI:
    def __init__(self, grid):
        global CELL_SIZE
        pygame.init()
        self.grid = grid
        self.rows = grid.rows
        self.cols = grid.cols
        self.width = self.cols * (CELL_SIZE + MARGIN) + MARGIN
        self.height = self.rows * (CELL_SIZE + MARGIN) + 130  # Extra space for UI
        max_width = 1366
        max_height = 786
        if self.width > max_width or self.height > max_height:
            # Shrink cell size if needed
            CELL_SIZE = min((max_width - (self.cols + 1) * MARGIN) // self.cols, (max_height - 130 - (self.rows + 1) * MARGIN) // self.rows)
            self.width = self.cols * (CELL_SIZE + MARGIN) + MARGIN
            self.height = self.rows * (CELL_SIZE + MARGIN) + 130
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("PATHFINDING VISUALIZATION - A*, GBFS, and Dynamic Mode")
        self.font = pygame.font.SysFont("consolas", FONT_SIZE)
        self.font_small = pygame.font.SysFont("consolas", 10)
        self.metrics = {"expanded": 0, "path_cost": 0, "time": 0.0}
        self.info = ""

    def draw_grid(self, frontier=set(), explored=set(), path=set()):
        self.screen.fill((220, 220, 220))
        for r in range(self.rows):
            for c in range(self.cols):
                rect = pygame.Rect(
                    c * (CELL_SIZE + MARGIN) + MARGIN,
                    r * (CELL_SIZE + MARGIN) + MARGIN,
                    CELL_SIZE, CELL_SIZE
                )
                color = COLOR_MAP["empty"]
                if (r, c) == self.grid.start:
                    color = COLOR_MAP["start"]
                elif (r, c) == self.grid.target:
                    color = COLOR_MAP["target"]
                elif self.grid.is_wall(r, c):
                    color = COLOR_MAP["wall"]
                elif (r, c) in path:
                    color = COLOR_MAP["path"]
                elif (r, c) in frontier:
                    color = COLOR_MAP["frontier"]
                elif (r, c) in explored:
                    color = COLOR_MAP["explored"]
                pygame.draw.rect(self.screen, color, rect)
        # Draw grid lines
        for r in range(self.rows + 1):
            pygame.draw.line(self.screen, (180, 180, 180), (MARGIN, r * (CELL_SIZE + MARGIN) + MARGIN),
                             (self.width - MARGIN, r * (CELL_SIZE + MARGIN) + MARGIN))
        for c in range(self.cols + 1):
            pygame.draw.line(self.screen, (180, 180, 180), (c * (CELL_SIZE + MARGIN) + MARGIN, MARGIN),
                             (c * (CELL_SIZE + MARGIN) + MARGIN, self.rows * (CELL_SIZE + MARGIN) + MARGIN))
        self.draw_metrics()
        pygame.display.update()

    def draw_metrics(self):
        y = self.rows * (CELL_SIZE + MARGIN) + 10
        expanded = self.font.render(f"Nodes Visited: {self.metrics['expanded']}", True, (0, 0, 0))
        path_cost = self.font.render(f"Path Cost: {self.metrics['path_cost']:.2f}", True, (0, 0, 0))
        time = self.font.render(f"Time: {self.metrics['time']*1000:.1f}ms", True, (0, 0, 0))
        self.screen.blit(expanded, (10, y))
        self.screen.blit(path_cost, (220, y))
        self.screen.blit(time, (420, y))
        
        # Info line
        if self.info:
            info = self.font.render(self.info, True, (80, 0, 80))
            self.screen.blit(info, (10, y + 30))
        
        # Help/Control line
        help_text = self.font_small.render(
            "1:A* 2:GBFS | H:Heuristic | R:Reset | G:GenMap | D:Dynamic | SPACE:Run | Q:Quit",
            True, (50, 50, 50)
        )
        self.screen.blit(help_text, (10, y + 55))

    def set_metrics(self, expanded, path_cost, exec_time):
        self.metrics["expanded"] = expanded
        self.metrics["path_cost"] = path_cost
        self.metrics["time"] = exec_time

    def set_info(self, text):
        self.info = text

    def animate_path(self, path, frontier, explored):
        """Animate the final path and support dynamic mode re-planning"""
        for i, pos in enumerate(path):
            path_set = set(path[:i+1])
            self.draw_grid(frontier, explored, path_set)
            pygame.time.delay(40)
            pygame.display.update()
            
            # Allow interruption
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
            pygame.time.delay(20)
        return True


# main.py
import pygame
import sys
import time

from grid import Grid
from gui import GUI
from node import Node

from algorithms.astar import astar
from algorithms.gbfs import gbfs

from utils import manhattan_distance, euclidean_distance, generate_random_obstacles, move_cost

# Grid sizing configuration
GRID_ROWS = 20
GRID_COLS = 20

ALGO_KEYS = {
    pygame.K_1: ("A*", astar, True),
    pygame.K_2: ("GBFS", gbfs, True),
}

HEURISTICS = {
    pygame.K_m: ("Manhattan", manhattan_distance),
    pygame.K_e: ("Euclidean", euclidean_distance),
}

def calculate_path_cost(path, grid):
    """Calculate total cost of path"""
    if not path or len(path) <= 1:
        return 0.0
    cost = 0.0
    for i in range(len(path) - 1):
        cost += move_cost(path[i], path[i + 1])
    return cost

def detect_path_collision(path, grid):
    """Detect if any obstacle blocks the remaining path"""
    for pos in path:
        if grid.is_wall(pos[0], pos[1]):
            return pos
    return None

def run_pathfinding(grid, gui, algo_func, algo_name, heuristic, depth_limit):
    """Run pathfinding algorithm and return path, metrics"""
    start = Node(*grid.start)
    target = Node(*grid.target)
    
    heur_name = 'Manhattan' if heuristic == manhattan_distance else 'Euclidean'
    gui.set_info(f"Running {algo_name} ({heur_name})...")
    gui.draw_grid()
    pygame.display.update()
    time.sleep(0.2)
    
    t0 = time.time()
    
    # Call algorithm with heuristic
    path, expanded, explored, frontier = algo_func(grid, start, target, gui, heuristic)
    
    t1 = time.time()
    path_cost = calculate_path_cost(path, grid) if path else 0.0
    
    gui.set_metrics(expanded, path_cost, t1 - t0)
    gui.draw_grid(frontier, explored, set())
    pygame.display.update()
    
    return path, expanded, explored, frontier, t1 - t0

def main():
    grid = Grid(GRID_ROWS, GRID_COLS)
    gui = GUI(grid)
    running = True
    
    algo_name = "A*"
    algo_func = astar
    algo_uses_heuristic = True
    heuristic = manhattan_distance
    depth_limit = 10
    dynamic_mode = False
    
    path = None
    explored = set()
    frontier = set()

    while running:
        heur_name = 'M' if heuristic == manhattan_distance else 'E'
        dynamic_text = "[DYNAMIC ON]" if dynamic_mode else "[Dynamic OFF]"
        gui.set_info(f"{algo_name} ({heur_name}) {dynamic_text} | Click:Wall | SPACE:Run | G:GenMap | H:Heuristic | D:Toggle Dynamic")
        gui.draw_grid(frontier, explored, set(path) if path else set())
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key in ALGO_KEYS:
                    algo_name, algo_func, algo_uses_heuristic = ALGO_KEYS[event.key]
                    path = None
                    explored = set()
                    frontier = set()
                elif event.key == pygame.K_h:
                    # Toggle heuristic
                    heuristic = euclidean_distance if heuristic == manhattan_distance else manhattan_distance
                elif event.key == pygame.K_r:
                    grid.reset()
                    path = None
                    explored = set()
                    frontier = set()
                elif event.key == pygame.K_g:
                    grid.reset()
                    generate_random_obstacles(grid, density=0.3)
                    path = None
                    explored = set()
                    frontier = set()
                    gui.set_info("Map generated with 30% obstacles")
                elif event.key == pygame.K_d:
                    dynamic_mode = not dynamic_mode
                    gui.set_info(f"Dynamic Mode {'ENABLED' if dynamic_mode else 'DISABLED'}")
                elif event.key == pygame.K_q:
                    running = False
                    break
                elif event.key == pygame.K_UP:
                    depth_limit += 1
                elif event.key == pygame.K_DOWN:
                    depth_limit = max(1, depth_limit - 1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                from gui import CELL_SIZE, MARGIN
                col = (x - MARGIN) // (CELL_SIZE + MARGIN)
                row = (y - MARGIN) // (CELL_SIZE + MARGIN)
                if 0 <= row < grid.rows and 0 <= col < grid.cols:
                    if grid.is_wall(row, col):
                        grid.remove_wall(row, col)
                    elif (row, col) != grid.start and (row, col) != grid.target:
                        grid.set_wall(row, col)
                    path = None
                    explored = set()
                    frontier = set()

        # Run algorithm on SPACE
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            path, expanded, explored, frontier, exec_time = run_pathfinding(
                grid, gui, algo_func, algo_name, heuristic, depth_limit
            )
            pygame.display.update()
            
            if path:
                # Animate path
                if dynamic_mode:
                    # Dynamic mode: agent moves and obstacles can spawn
                    animate_path_dynamic(path, grid, gui, frontier, explored, algo_func, algo_name, heuristic)
                else:
                    # Normal mode: just animate the path
                    gui.animate_path(path, frontier, explored)
                gui.set_info(f"{algo_name} completed! Press SPACE to run again.")
            else:
                gui.set_info("No path found.")
                gui.draw_grid(frontier, explored, set())
                pygame.display.update()
            time.sleep(0.5)
        
        pygame.time.delay(60)
    
    pygame.quit()
    sys.exit()

def animate_path_dynamic(path, grid, gui, frontier, explored, algo_func, algo_name, heuristic):
    """Animate path with dynamic obstacle spawning and re-planning"""
    from node import Node
    
    agent_pos_idx = 0
    
    while agent_pos_idx < len(path):
        agent_pos = path[agent_pos_idx]
        remaining_path = path[agent_pos_idx:]
        
        # Draw current state
        path_set = set(path[:agent_pos_idx+1])
        gui.draw_grid(frontier, explored, path_set)
        pygame.display.update()
        pygame.time.delay(40)
        
        # Check for quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        # Spawn random obstacles
        new_wall, new_wall_pos = grid.spawn_random_obstacle()
        
        # Check if new obstacle blocks the remaining path
        if new_wall_pos and new_wall_pos in remaining_path:
            # Obstacle blocks path - need to re-plan
            gui.set_info(f"Obstacle detected at {new_wall_pos}! Re-planning...")
            gui.draw_grid(frontier, explored, path_set)
            pygame.display.update()
            pygame.time.delay(200)
            
            # Re-run pathfinding from current position
            start = Node(*agent_pos)
            target = Node(*grid.target)
            
            t0 = time.time()
            new_path, expanded, explored, frontier = algo_func(grid, start, target, gui, heuristic)
            t1 = time.time()
            
            if new_path:
                # Update path from current position
                path = path[:agent_pos_idx] + new_path[1:]  # Skip first pos (current position)
                path_cost = calculate_path_cost(path, grid)
                gui.set_metrics(expanded, path_cost, t1 - t0)
                gui.set_info(f"New path found! Continuing...")
                gui.draw_grid(frontier, explored, set(path[:agent_pos_idx+1]))
                pygame.display.update()
                pygame.time.delay(500)
            else:
                # No new path found
                gui.set_info("No path found from current position!")
                gui.draw_grid(frontier, explored, set(path[:agent_pos_idx+1]))
                pygame.display.update()
                pygame.time.delay(500)
                return
        
        agent_pos_idx += 1
        pygame.time.delay(20)


if __name__ == "__main__":
    main()


def calculate_path_cost(path, grid):
    """Calculate total cost of path"""
    if not path or len(path) <= 1:
        return 0.0
    cost = 0.0
    for i in range(len(path) - 1):
        cost += move_cost(path[i], path[i + 1])
    return cost

def detect_path_collision(path, grid):
    """Detect if any obstacle blocks the remaining path"""
    for pos in path:
        if grid.is_wall(pos[0], pos[1]):
            return pos
    return None

def run_pathfinding(grid, gui, algo_func, algo_name, heuristic, depth_limit):
    """Run pathfinding algorithm and return path, metrics"""
    start = Node(*grid.start)
    target = Node(*grid.target)
    
    heur_name = 'Manhattan' if heuristic == manhattan_distance else 'Euclidean'
    gui.set_info(f"Running {algo_name} ({heur_name})...")
    gui.draw_grid()
    pygame.display.update()
    time.sleep(0.2)
    
    t0 = time.time()
    
    # Call algorithm with appropriate parameters
    if algo_name == "DLS":
        path, expanded, explored, frontier = algo_func(grid, start, target, gui, depth_limit)
    elif algo_name == "IDDFS":
        path, expanded, explored, frontier = algo_func(grid, start, target, gui, max_depth=depth_limit)
    elif algo_name in ["A*", "GBFS"]:
        path, expanded, explored, frontier = algo_func(grid, start, target, gui, heuristic)
    else:
        path, expanded, explored, frontier = algo_func(grid, start, target, gui)
    
    t1 = time.time()
    path_cost = calculate_path_cost(path, grid) if path else 0.0
    
    gui.set_metrics(expanded, path_cost, t1 - t0)
    gui.draw_grid(frontier, explored, set())
    pygame.display.update()
    
    return path, expanded, explored, frontier, t1 - t0


if __name__ == "__main__":
    main()


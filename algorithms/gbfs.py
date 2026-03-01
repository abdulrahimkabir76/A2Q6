import heapq
from node import Node
from utils import MOVES

def gbfs(grid, start, target, gui=None, heuristic=None):
    """
    Greedy Best-First Search using f(n) = h(n)
    h(n) = heuristic estimate to goal only
    heuristic: function that takes (current_pos, goal_pos) and returns estimate
    """
    if heuristic is None:
        from utils import manhattan_distance
        heuristic = manhattan_distance
    
    # Priority queue: (h_score, counter, node)
    counter = 0
    open_set = []
    start_h = heuristic((start.row, start.col), (target.row, target.col))
    heapq.heappush(open_set, (start_h, counter, start))
    counter += 1
    
    visited = set()
    visited.add((start.row, start.col))
    explored = set()
    frontier = {(start.row, start.col)}
    expanded = 0
    
    while open_set:
        h, _, current = heapq.heappop(open_set)
        pos = (current.row, current.col)
        
        if pos in explored:
            continue
        
        frontier.discard(pos)
        explored.add(pos)
        expanded += 1
        
        if gui:
            gui.draw_grid(frontier, explored, set())
            import pygame
            pygame.time.delay(40)
            pygame.display.update()
        
        if pos == (target.row, target.col):
            path = []
            while current:
                path.append((current.row, current.col))
                current = current.parent
            return path[::-1], expanded, explored, frontier
        
        for dr, dc in MOVES:
            nr, nc = current.row + dr, current.col + dc
            if grid.in_bounds(nr, nc) and not grid.is_wall(nr, nc):
                neighbor_pos = (nr, nc)
                
                if neighbor_pos not in visited:
                    visited.add(neighbor_pos)
                    h = heuristic(neighbor_pos, (target.row, target.col))
                    neighbor = Node(nr, nc, current)
                    heapq.heappush(open_set, (h, counter, neighbor))
                    counter += 1
                    frontier.add(neighbor_pos)
    
    return None, expanded, explored, frontier

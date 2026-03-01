import heapq
from node import Node
from utils import MOVES

def astar(grid, start, target, gui=None, heuristic=None):
    """
    A* algorithm using f(n) = g(n) + h(n)
    g(n) = cost from start
    h(n) = heuristic estimate to goal
    heuristic: function that takes (current_pos, goal_pos) and returns estimate
    """
    if heuristic is None:
        from utils import manhattan_distance
        heuristic = manhattan_distance
    
    # Priority queue: (f_score, counter, node)
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
    g_score = {(start.row, start.col): 0}
    
    while open_set:
        f, _, current = heapq.heappop(open_set)
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
                
                # Calculate cost
                from utils import move_cost
                move_c = move_cost(pos, neighbor_pos)
                tentative_g = g_score[pos] + move_c
                
                if neighbor_pos in g_score and tentative_g >= g_score[neighbor_pos]:
                    continue
                
                if neighbor_pos not in visited:
                    visited.add(neighbor_pos)
                    g_score[neighbor_pos] = tentative_g
                    h = heuristic(neighbor_pos, (target.row, target.col))
                    f = tentative_g + h
                    neighbor = Node(nr, nc, current, tentative_g)
                    heapq.heappush(open_set, (f, counter, neighbor))
                    counter += 1
                    frontier.add(neighbor_pos)
                elif tentative_g < g_score[neighbor_pos]:
                    g_score[neighbor_pos] = tentative_g
                    h = heuristic(neighbor_pos, (target.row, target.col))
                    f = tentative_g + h
                    neighbor = Node(nr, nc, current, tentative_g)
                    heapq.heappush(open_set, (f, counter, neighbor))
                    counter += 1
    
    return None, expanded, explored, frontier

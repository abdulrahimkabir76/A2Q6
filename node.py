# node.py
import math

class Node:
    def __init__(self, row, col, parent=None, cost=0, depth=0):
        self.row = row
        self.col = col
        self.parent = parent
        self.cost = cost
        self.depth = depth

    def __eq__(self, other):
        return isinstance(other, Node) and self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.row, self.col))

    def position(self):
        return (self.row, self.col)

    def __lt__(self, other):
        # For heapq (UCS)
        return self.cost < other.cost

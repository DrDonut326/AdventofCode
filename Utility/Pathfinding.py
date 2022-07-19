from collections import deque

from Functions import Pos
from Grids import DictGrid, ArrayGrid


class Node:
    """Used for graph traversal.  Data is what was in the passed-in graph at that point."""
    def __init__(self, pos: Pos, data, cost):
        self.pos = pos
        self.data = data
        self.cost = cost
        self.previous = []

    def __repr__(self):
        return f"Pos: {self.pos}, Data: {self.data}, Cost: {self.cost}"

    def __gt__(self, other):
        return self.cost > other.cost

    def __lt__(self, other):
        return self.cost < other.cost

    def __ge__(self, other):
        return self.cost >= other.cost

    def __eq__(self, other):
        return self.cost == other.cost

    def __ne__(self, other):
        return self.cost != other.cost


def get_test_input():
    grid = DictGrid(None, {'#', 'S', 'F', 'G', 'E'}, bounded=True)
    start = None
    finish = None
    with open('test_input.txt') as f:
        for y, line in enumerate(f):
            line = line.rstrip()
            for x, element in enumerate(line):
                pos = Pos(x, y)
                grid.grid[pos] = element
                if element == 'S':
                    start = pos
                if element == 'F':
                    finish = pos
    return grid, start, finish


def bfs(grid: ArrayGrid, x: int, y: int):
    """Creates a bfs cost grid using a simple 2D array."""
    q = deque()
    q.append((x, y))
    distance = dict()
    distance[(x, y)] = 0

    while q:
        # Tuples of position of (x, y)
        x, y = q.popleft()
        for next_pos in grid.get_neighbors_4way(x, y):
            nx, ny = next_pos
            # Check if in visited already
            if next_pos not in distance:
                # Check if that element in walls
                if grid.grid[ny][nx] not in grid.walls:
                    q.append(next_pos)
                    distance[next_pos] = 1 + distance[(x, y)]

    return distance



def bfs_dictgrid(grid: DictGrid, start: tuple):
    """Creates a cost grid that radiates out from the starting position.  Searches all possible cells."""
    q = deque()
    q.append(start)
    distance = dict()
    distance[start] = 0

    while q:
        current_pos = q.popleft()
        for next_pos in grid.get_neighbors_4way(current_pos[0], current_pos[1], exist_prune=True):
            # Check if in visited already
            if next_pos not in distance:
                # Check if that element in walls
                if grid.get_value_from_pos_object(next_pos) not in grid.walls:
                    q.append(next_pos)
                    distance[next_pos] = 1 + distance[current_pos]

    return distance


def display_cost_grid(grid, cost_grid):
    print('-' * 25)
    min_x, max_x, min_y, max_y = grid.get_graph_min_max()
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            pos = (x, y)
            # If this position in the grid
            if pos in grid.grid:
                # If this position in the cost grid
                if pos in cost_grid:
                    # Print unless the cost is zero
                    if cost_grid[pos] != 0:
                        print(cost_grid[pos], end='')
                    else:
                        print(grid.grid[pos], end='')

                else:
                    print(grid.grid[pos], end='')
            else:
                print(' ', end='')
        print()
    print('-' * 25)


def main():
    grid, start, finish = get_test_input()
    cost_grid = bfs_dictgrid(grid, start, finish)
    grid.display_grid_with_highlighted_positions_all_same([start, finish], (200, 235, 50))




if __name__ == '__main__':
    main()

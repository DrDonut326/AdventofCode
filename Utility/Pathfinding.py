from Functions import Pos
from Grids import DictGrid
from queue import Queue


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


def dijkstra(grid: DictGrid, start: Pos):
    """Creates a cost grid that radiates out from start"""
    q = Queue()
    q.put(start)
    distance = dict()
    distance[start] = 0

    while not q.empty():
        current_pos: Pos
        current_pos = q.get()
        for next_pos in current_pos.get_neighbors_4way():
            # Check if in visited already
            if next_pos not in distance:
                # Check if that element in walls
                if grid.get_value_from_pos_object(next_pos) not in grid.walls:
                    q.put(next_pos)
                    distance[next_pos] = 1 + distance[current_pos]

    return distance


def display_cost_grid(grid, cost_grid):
    print('-' * 25)
    min_x, max_x, min_y, max_y = grid.get_graph_min_max()
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            pos = Pos(x, y)
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
    cost_grid = dijkstra(grid, start, finish)
    grid.display_grid_with_highlighted_positions_all_same([start, finish], (200, 235, 50))




if __name__ == '__main__':
    main()

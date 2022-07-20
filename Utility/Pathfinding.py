import heapq
from collections import deque
from random import randint
from Functions import Pos
from Grids import DictGrid, ArrayGrid


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, pos, priority):
        heapq.heappush(self.elements, (priority, pos))

    def get(self):
        return heapq.heappop(self.elements)[1]


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


def dijkstra_dictgrid(grid: DictGrid, start: tuple, finish: tuple, neighbor_func):
    """Searches a dict grid for the shortest path between start and finish.
    User must pass in a function that tells Dijkstra how to find neighbors and their costs."""
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == finish:
            break

        # Get the pos and cost of that neighbors of this position
        for neighbor, neighbor_cost in neighbor_func(grid, current):
            # Get the cost of going from current to neighbor
            new_cost = cost_so_far[current] + neighbor_cost
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost
                frontier.put(neighbor, priority)
                came_from[neighbor] = current

    return came_from, cost_so_far


def rebuild_path(came_from, start, finish):
    current = finish
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path


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


def get_random_grid(size):
    # Create a size x size grid of random numbers
    grid = []
    for a in range(size):
        row = []
        for b in range(size):
            row.append(randint(0, 9))
        grid.append(row)
    return grid


def get_random_dict_grid(size):
    grid = DictGrid(int)
    array = get_random_grid(size)
    for y, row in enumerate(array):
        for x, element in enumerate(row):
            pos = (x, y)
            grid.add_data_to_grid_at_pos(pos, element)
    return grid


def neighbor_function_use_grid_data(grid: DictGrid, pos):
    """Returns the neighbors of this position and also the cost from pos to neighbor."""
    neighbors = grid.get_neighbors_4way(pos[0], pos[1], exist_prune=True)

    ans = []
    for n in neighbors:
        cost = grid.get_value_from_pos_object(n)
        ans.append((n, cost))
    return ans

def main():
    size = 2
    grid = get_random_dict_grid(size)
    grid.display_grid_ascii()
    start = (0, 0)
    finish = (size - 1, size - 1)

    came_from, cost_so_far = dijkstra_dictgrid(grid, start, finish, neighbor_function_use_grid_data)

    path = rebuild_path(came_from, start, finish)

    grid.display_grid_with_highlighted_positions_all_same(path, (0, 255, 0))
    print(cost_so_far[finish])


if __name__ == '__main__':
    main()

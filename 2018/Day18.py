from Classes.Grids import ArrayGrid
from copy import deepcopy


def get_input():
    g = []
    with open("input.txt") as f:
        for line in f:
            line = line.rstrip()
            row = []
            for element in line:
                row.append(element)
            g.append(row)
    ans = ArrayGrid(g)
    return ans


def is_in_bounds(z, grid):
    pass


def get_pruned_neighbors(grid: ArrayGrid, x, y):
    neighbors_8 = grid.get_neighbors_8way(x, y)
    return [z for z in neighbors_8 if grid.is_in_bounds(z)]


def will_a_tree_grow_from_an_open_square(grid, neighbors):
    tree_count = 0
    for neighbor in neighbors:
        x, y = neighbor
        if grid.grid[y][x] == '|':
            tree_count += 1
            if tree_count >= 3:
                return True
    return False


def will_a_lumberyard_grow_from_a_tree_square(grid, neighbors):
    lumber_count = 0
    for neighbor in neighbors:
        x, y = neighbor
        if grid.grid[y][x] == '#':
            lumber_count += 1
            if lumber_count >= 3:
                return True
    return False


def will_a_lumberyard_turn_into_an_open_square(grid, neighbors):
    tree_count = 0
    lumber_count = 0
    for neighbor in neighbors:
        x, y = neighbor
        if grid.grid[y][x] == '|':
            tree_count += 1
        elif grid.grid[y][x] == '#':
            lumber_count += 1
    if tree_count >= 1 and lumber_count >= 1:
        return False
    return True


def update_grid(grid: ArrayGrid):
    # Copy the grid
    grid_copy = deepcopy(grid.grid)

    # Iterate through the CURRENT grid and make changes to the COPY
    for y, row in enumerate(grid.grid):
        for x, element in enumerate(row):
            neighbors = get_pruned_neighbors(grid, x, y)


            # If current area is a tree
            if element == '.':
                if will_a_tree_grow_from_an_open_square(grid, neighbors):
                    grid_copy[y][x] = '|'

            elif element == '|':
                if will_a_lumberyard_grow_from_a_tree_square(grid, neighbors):
                    grid_copy[y][x] = '#'

            elif element == '#':
                if will_a_lumberyard_turn_into_an_open_square(grid, neighbors):
                    grid_copy[y][x] = '.'

    # Update the current grid
    grid.grid = grid_copy


def get_resource_value(grid):
    trees = 0
    yards = 0
    for row in grid.grid:
        for element in row:
            if element == '|':
                trees += 1
            if element == '#':
                yards += 1
    return trees * yards


def get_grid_hash(grid):
    # Hash each row, then hash the sum
    hash_sum = 0
    for row in grid.grid:
        hash_sum += hash(tuple(row))
    return hash(hash_sum)


def part_1():
    grid = get_input()
    for _ in range(10):
        update_grid(grid)
    print(get_resource_value(grid))  # Part 1 answer


def get_period():
    grid = get_input()
    h = get_grid_hash(grid)

    # Store hashes here
    hashes = set()
    hashes.add(h)

    # Keep track of time steps
    time_counter = 0

    first_stop_time = None   # Time when we first has a match in hashes
    double_stop = None       # The hash that was repeated (start of the period)

    while True:
        time_counter += 1
        update_grid(grid)
        # Get hash
        h = get_grid_hash(grid)

        # If there hash is already there, then we found the period
        if h in hashes:
            if double_stop is None:
                double_stop = h
                first_stop_time = time_counter
            elif h == double_stop:
                return first_stop_time, time_counter-first_stop_time
        else:
            hashes.add(h)


def part_2(first_stop, period):
    grid = get_input()

    total_iterations = 1000000000 - first_stop

    remaining_iterations = total_iterations % period

    for _ in range(first_stop):
        update_grid(grid)

    for _ in range(remaining_iterations):
        update_grid(grid)

    print(get_resource_value(grid))


def main():
    part_1()
    first_stop, period = get_period()
    part_2(first_stop, period)


rgb = {'.': (255, 255, 255), '|': (0, 255, 0), '#': (82, 49, 3)}
main()

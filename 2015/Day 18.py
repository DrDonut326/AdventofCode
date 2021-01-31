from Grids import DictGrid
from Utility import get_input
from copy import deepcopy


def set_corners(grid):
    s = grid.size - 1
    grid.add_data_to_grid_at_x_y_z('#', 0, 0)
    grid.add_data_to_grid_at_x_y_z('#', 0, s)
    grid.add_data_to_grid_at_x_y_z('#', s, 0)
    grid.add_data_to_grid_at_x_y_z('#', s, s)


def init_grid(grid, part=1):
    starting_position = get_input('line')
    # y
    for y, line in enumerate(starting_position):
        # x
        for x, letter in enumerate(line):
            grid.add_data_to_grid_at_x_y_z(letter, x, y)
    # Part 2 Set corners
    if part == 2:
        set_corners(grid)


def count_on_neighbors(key, grid):
    ans = 0
    neighbors = grid.get_neighbors_8way(grid.parse_pos_string(key))
    for n in neighbors:
        k = n.get_name()
        if grid.grid[k] == '#':
            ans += 1
    return ans


def count_on(grid):
    count = 0
    for v in grid.grid.values():
        if v == '#':
            count += 1
    return count



def update(grid, part=1):
    t_grid = deepcopy(grid)
    for key in grid.grid.keys():
        status = grid.grid[key]
        neighbors_on = count_on_neighbors(key, grid)
        if status == '#':
            if neighbors_on != 2 and neighbors_on != 3:
                t_grid.grid[key] = '.'
        elif status == '.':
            if neighbors_on == 3:
                t_grid.grid[key] = '#'
    grid.grid = t_grid.grid
    # Part 2 Set corners
    if part == 2:
        set_corners(grid)




def main():
    size = 100
    grid = DictGrid(str, size)
    init_grid(grid)
    for _ in range(100):
        update(grid)
    # grid.display_grid_ascii()
    print(f"Part 1 answer: {count_on(grid)}")

    # Part 2

    grid = DictGrid(str, size)
    init_grid(grid, 2)

    for _ in range(100):
        update(grid, 2)
    # grid.display_grid_ascii()
    print(f"Part 2 answer: {count_on(grid)}")




main()



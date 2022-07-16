# Rework of Day 11 with COMPUTER SCIENCE MAGIC
from Functions import Pos


def get_fuel_power(pos):
    x, y = pos.x, pos.y
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial
    power_level *= rack_id
    if power_level <= 99:
        power_level = 0
    else:
        if power_level > 0:
            power_level = int(str(power_level)[-3])
        else:
            power_level = int('-' + str(power_level)[-3])

    power_level -= 5
    assert type(power_level) == int
    return power_level


def make_grid():
    grid = []
    for y in range(1, 301):
        row = []
        for x in range(1, 301):
            pos = Pos(x, y)
            row.append(get_fuel_power(pos))
        grid.append(row)
    return grid


def get_summed_area_point(x, y, grid):
    if x == 0 and y == 0:
        return grid[0][0]
    if x == 0 and y == 1:
        return grid[0][0] + grid[1][0]
    if x == 1 and y == 0:
        return grid[0][0] + grid[0][1]

    return grid[y][x] + get_summed_area_point(x, y - 1, grid) + get_summed_area_point(x - 1, y, grid) - get_summed_area_point(x - 1, y - 1, grid)


def make_sums_grid():
    grid = make_grid()
    magic = []
    # At each spot, return the sum of everything up and left including the current spot
    for y, row in enumerate(grid):
        ans_row = []
        for x, element in enumerate(row):
            ans_row.append(get_summed_area_point(x, y, grid))
        magic.append(ans_row)
    return magic


def get_square_at_pos(x, y, size, sums_grid):
    print(x, y, size)
    # Find the area from the bottom right point
    ans = sums_grid[y + size][x + size]

    # Subtract the bottom left and top right areas
    ans -= sums_grid[y][x + size]
    ans -= sums_grid[y + size][x + size]

    # Add the top left
    ans += sums_grid[y][x]

    return ans



def main():
    sums_grid = make_sums_grid()
    print(sums_grid)
    quit()
    print(get_square_at_pos(33, 45, 3, sums_grid))


serial = 18
main()
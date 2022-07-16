from Functions import get_input, manhat_pos
from collections import defaultdict
from Pos import Pos
from Grids import DictGrid


def make_pos_list(nums):
    ans = []
    for num in nums:
        pos = Pos(num[0], num[1], name=next(id_gen), state='alive')
        ans.append(pos)
    return ans


def get_closest_manhat(pos, pos_list):
    best = None
    best_list = []
    for p in pos_list:
        result = manhat_pos(pos, p)
        if best is None:
            best = result
            best_list.append(p)
        elif result == best:
            best_list.append(p)
        elif result < best:
            best = result
            best_list.clear()
            best_list.append(p)

    if len(best_list) > 1:
        return '?'
    if len(best_list) == 1:
        return best_list[0]

    raise Exception('No closest position??')


def get_infinite_locations(pos_list, grid):
    """Returns a set of infinite locations."""
    # Find the rectangle made by the most extreme locations on each side.
    # Get closest positions for each
    # If a letter is directly on it, or it has it's own closest position, it is inifinte

    min_y = min([x.y for x in pos_list])
    max_y = max([x.y for x in pos_list])

    min_x = min([x.x for x in pos_list])
    max_x = max([x.x for x in pos_list])

    ans = set()

    # Check most north and south
    for x in range(min_x, max_x + 1):
        for y in [min_y, max_y]:
            pos = Pos(x, y)
            if pos not in grid.grid:
                result = get_closest_manhat(pos, pos_list)
                if type(result) == Pos:
                    grid.grid[pos] = get_closest_manhat(pos, pos_list).name
                    ans.add(result)
                else:
                    grid.grid[pos] = result

    # East and west
    for y in range(min_y, max_y + 1):
        for x in [min_x, max_x]:
            pos = Pos(x, y)
            if pos not in grid.grid:
                result = get_closest_manhat(pos, pos_list)
                if type(result) == Pos:
                    grid.grid[pos] = get_closest_manhat(pos, pos_list).name
                    ans.add(result)
                else:
                    grid.grid[pos] = result

    return ans, (min_x, max_x, min_y, max_y)


def get_id():
    num = 0
    while True:
        yield num
        num += 1


def fill_in_rest_of_grid(grid, pos_list, minmax):
    min_x, max_x, min_y, max_y = minmax
    for y in range(min_y + 1, max_y):
        for x in range(min_x + 1, max_x):
            pos = Pos(x, y)
            if pos not in grid.grid:
                result = get_closest_manhat(pos, pos_list)
                if type(result) == Pos:
                    grid.grid[pos] = get_closest_manhat(pos, pos_list).name
                else:
                    grid.grid[pos] = result


def make_grid(pos_list):
    grid = DictGrid(str, bounded=False)
    for pos in pos_list:
        grid.grid[pos] = pos.name
    return grid


def count_areas(grid, infinte):
    bad = [b.name for b in infinte]
    bad.append('?')

    areas = defaultdict(int)

    for key in grid.grid:
        x = grid.grid[key]
        if x not in bad:
            areas[x] += 1

    return areas


def get_sum_of_manhat(pos, pos_list):
    count = 0
    for p in pos_list:
        count += manhat_pos(pos, p)
    return count


def how_many_within(pos_list, minmax):
    ans = 0
    min_x, max_x, min_y, max_y = minmax
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            pos = Pos(x, y)
            s = get_sum_of_manhat(pos, pos_list)
            if s < 10000:
                ans += 1
    return ans


def main():
    nums = get_input('line', do_split=True, split_key=', ', int_convert=True)
    
    # List of locations that this position has domain over
    pos_list = make_pos_list(nums)

    # Make grid
    grid = make_grid(pos_list)

    # Get infinites
    infinite, minmax = get_infinite_locations(pos_list, grid)

    # Fill in the remaining inner grid
    fill_in_rest_of_grid(grid, pos_list, minmax)

    areas = count_areas(grid, infinite)

    largest_size = max(areas.items(), key=lambda x: x[1])[1]

    print(largest_size)  # Part 1 answer

    within = how_many_within(pos_list, minmax)

    print(within)


id_gen = get_id()
main()

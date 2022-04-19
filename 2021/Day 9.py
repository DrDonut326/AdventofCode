from Grids import DictGrid
from Pos import Pos


def get_input():
    ans = []
    with open("input.txt") as f:
        for line in f:
            line = line.rstrip()
            line = list(line)
            ans.append([int(x) for x in line])
    return ans


def add_ocean_data(data, map):
    for y, row in enumerate(data):
        for x, num in enumerate(row):
            map.add_data_to_grid_at_x_y_z(num, x, y)


def is_low_point(p, neighbors, map):
    p_value = map.get_value_from_pos_object(p)
    for n in neighbors:
        n_value = map.get_value_from_pos_object(n)
        if n_value <= p_value:
            return False
    return True


def find_low_points(data, map):
    ans = []
    for y, row in enumerate(data):
        for x, num in enumerate(row):
            # Create a position object
            p = Pos(x, y)

            # Get the neighbors
            neighbors = map.get_neighbors_4way(p, exist=True)

            # See if the current position is lower than all of its neighbors
            if is_low_point(p, neighbors, map):
                # If so, add this pos to the low points counter
                ans.append(p)
    return ans


def get_risk_level(pos, map):
    return map.get_value_from_pos_object(pos) + 1


def sum_risk_levels(low_points, map):
    ans = 0
    for low in low_points:
        ans += get_risk_level(low, map)
    return ans


def find_valley_size(map, low):
    visited = map.flood(low, 9)
    return len(visited)


def find_valleys(map, low_points):
    basin_sizes = []
    # Iterate through low points
    for low in low_points:
        # Record basin sizes
        basin_sizes.append(find_valley_size(map, low))
    return basin_sizes

def main():
    ocean_data = get_input()
    ocean_map = DictGrid(datatype=int)
    add_ocean_data(ocean_data, ocean_map)
    low_points = find_low_points(ocean_data, ocean_map)
    all_sizes = find_valleys(ocean_map, low_points)
    all_sizes.sort(reverse=True)
    print(all_sizes[0] * all_sizes[1] * all_sizes[2])




main()

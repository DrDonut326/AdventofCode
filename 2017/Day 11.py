from Functions import get_input
from HexGrid import HexGrid


def main():
    grid = HexGrid()
    current_pos = grid.add_hex_from_qrs(0, 0, 0)
    steps = get_input('line', do_split=True, split_key=(','))[0]
    for step in steps:
        current_pos = current_pos.get_neighbor_from_string(step)
        grid.add_hex(current_pos)

    print(current_pos.get_max())   # Part 1 ans

    max_distance = 0

    for key in grid.grid:
        pos = grid.grid[key]
        dist = pos.get_max()
        if dist > max_distance:
            max_distance = dist

    print(max_distance)   # Part 2 answer

main()

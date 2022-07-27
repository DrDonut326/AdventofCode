from Classes.Grids import DictGrid


def up(pos):
    return pos[0], pos[1] - 1


def down(pos):
    return pos[0], pos[1] + 1


def left(pos):
    return pos[0] - 1, pos[1]


def right(pos):
    return pos[0] + 1, pos[1]


def get_wires():
    wires = []
    with open('input.txt') as f:
        for line in f:
            line = line.rstrip()
            wires.append([x for x in line.split(',')])
    return wires


def add_wires_to_grid(wires, grid: DictGrid):
    wire_1_step_dict = dict()
    wire_2_step_dict = dict()
    for i, wire in enumerate(wires):
        pos = (0, 0)
        steps = 0
        for code in wire:
            direction = code[0]

            n = int(code[1:])
            for _ in range(n):
                steps += 1
                match direction:
                    case 'U':
                        pos = up(pos)
                    case 'D':
                        pos = down(pos)
                    case 'L':
                        pos = left(pos)
                    case 'R':
                        pos = right(pos)
                grid.add_data_to_grid_at_pos(pos, i)
                if i == 0:
                    if pos not in wire_1_step_dict:
                        wire_1_step_dict[pos] = steps
                if i == 1:
                    if pos not in wire_2_step_dict:
                        wire_2_step_dict[pos] = steps
    return wire_1_step_dict, wire_2_step_dict


def get_intersections(grid: DictGrid):
    return [x for x in grid.grid.items() if 1 in x[1] and 0 in x[1]]


def get_closest_intersection(grid):
    intersections = get_intersections(grid)
    best = None
    best_pos = None
    for inter in intersections:
        pos = inter[0]
        dist = abs(pos[0]) + abs(pos[1])
        if best is None or dist < best:
            best = dist
            best_pos = pos
    return best_pos


def part_1(grid):
    pos = get_closest_intersection(grid)
    print(abs(pos[0]) + abs(pos[1]))


def part_2(grid, wire_1_steps, wire_2_steps):
    intersections = get_intersections(grid)
    best = None
    for inter in intersections:
        pos = inter[0]
        first_steps = wire_1_steps[pos]
        second_steps = wire_2_steps[pos]
        combined = first_steps + second_steps
        if best is None or combined < best:
            best = combined
    print(best)


def main():
    grid = DictGrid(list)
    wires = get_wires()
    wire_1_steps, wire_2_steps = add_wires_to_grid(wires, grid)
    part_1(grid)
    part_2(grid, wire_1_steps, wire_2_steps)


main()

from GetInput import get_input
from collections import defaultdict
from Pos import Pos


def parse_command(command):
    code = ''
    if command.startswith('turn on'):
        code = 'turn on'
        command = command.replace('turn on ', '')
    elif command.startswith('turn off'):
        code = 'turn off'
        command = command.replace('turn off ', '')
    elif command.startswith('toggle'):
        code = 'toggle'
        command = command.replace('toggle ', '')
    else:
        raise AssertionError("Command started with something weird.")

    left, right = command.split(' through ')
    x1, y1 = left.split(',')
    x2, y2 = right.split(',')

    return code, int(x1), int(y1), int(x2), int(y2)


def update_grid(code, pos, grid):
    name = pos.get_name()
    if code == 'turn on':
        grid[name] += 1
        return
    if code == 'turn off':
        grid[name] = 0
        if grid[name] < 0:
            grid[name] = 0
        return
    if code == 'toggle':
        if grid[name] == 0:
            grid[name] = 1
        else:
            grid[name] = 0
        return
    raise AssertionError("Shouldn't get here.")


def update_grid_2(code, pos, grid):
    name = pos.get_name()
    if code == 'turn on':
        grid[name] += 1
        return
    if code == 'turn off':
        grid[name] -= 1
        if grid[name] < 0:
            grid[name] = 0
        return
    if code == 'toggle':
        grid[name] += 2
        return
    raise AssertionError("Shouldn't get here.")



def execute_command(command, grid):
    code, x1, y1, x2, y2 = parse_command(command)

    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            pos = Pos(x, y)
            update_grid(code, pos, grid)


def execute_command_2(command, grid):
    code, x1, y1, x2, y2 = parse_command(command)

    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            pos = Pos(x, y)
            update_grid_2(code, pos, grid)



def main(part):
    commands = get_input('line')
    grid = defaultdict(int)
    if part == 1:
        for command in commands:
            execute_command(command, grid)
        print(len([x for x in grid.values() if x >= 1]))
    else:
        # Part 2
        for command in commands:
            execute_command_2(command, grid)
        print(sum(grid.values()))


main(2)

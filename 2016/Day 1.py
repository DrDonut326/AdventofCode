from Functions import get_input


def part1():
    x = 0
    y = 0
    direction = 'N'
    turn_dict = {'N': {'L': 'W', 'R': 'E'},
                 'S': {'L': 'E', 'R': 'W'},
                 'E': {'L': 'N', 'R': 'S'},
                 'W': {'L': 'S', 'R': 'N'}
                 }
    instructions = get_input('line', do_split=True, split_key=', ')[0]
    for instruction in instructions:
        turn = instruction[0]
        value = int(instruction[1:])
        direction = turn_dict[direction][turn]
        if direction == 'N':
            y -= value
        elif direction == 'S':
            y += value
        elif direction == 'E':
            x += value
        elif direction == 'W':
            x -= value
    return abs(x) + abs(y)


def build_string(x, y):
    return f"X:{x}Y:{y}"

def walk(direction, x, y, value, visited):
    """Walks forward value times
    Adding eaching place to visited"""
    for _ in range(value):

        if direction == 'N':
            y -= 1
        elif direction == 'S':
            y += 1
        elif direction == 'E':
            x += 1
        elif direction == 'W':
            x -= 1

        if (x, y) in visited:
            return x, y, True
        else:
            visited.add((x, y))

    return x, y, False


def part2():
    x = 0
    y = 0
    visited = set()
    direction = 'N'
    turn_dict = {'N': {'L': 'W', 'R': 'E'},
                 'S': {'L': 'E', 'R': 'W'},
                 'E': {'L': 'N', 'R': 'S'},
                 'W': {'L': 'S', 'R': 'N'}
                 }
    instructions = get_input('line', do_split=True, split_key=', ')[0]
    visited.add((x, y))
    for instruction in instructions:
        turn = instruction[0]
        value = int(instruction[1:])
        direction = turn_dict[direction][turn]
        x, y, answer = walk(direction, x, y, value, visited)
        if answer:
            return abs(x) + abs(y)

    raise EnvironmentError("No solution found??")






def main():
    print(f"Part 1 answer = {part1()}")
    print(f"Part 2 answer = {part2()}")

main()

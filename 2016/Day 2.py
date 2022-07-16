from Functions import get_input


def make_keypad():
    ans = {
        (-1, 1): 1, (0, -1): 2, (1, -1): 3,
        (-1, 0): 4, (0, 0): 5, (1, 0): 6,
        (-1, 1): 7, (0, 1): 8, (1, 1): 9
    }
    return ans


def part1(keypad, codes):
    move_dict = {'L': (-1, 0), 'R': (1, 0), 'U': (0, -1), 'D': (0, 1)}
    door_code = []
    for code in codes:
        x, y = 0, 0
        for letter in code:
            dx, dy = move_dict[letter]
            tx, ty = dx + x, dy + y
            if (tx, ty) in keypad:
                x = tx
                y = ty
        door_code.append(keypad[(x, y)])
    ans = ''.join([str(x) for x in door_code])
    return ans

def make_crosspad():
    ans = {
        (0, 0): 5, (1, 0): 6, (2, 0): 7, (3, 0): 8, (4, 0): 9,
        (1, 1): 'A', (2, 1): 'B', (3, 1): 'C',
        (2, 2): 'D',
        (1, -1): 2, (2, -1): 3, (3, -1): 4,
        (2, -2): 1
    }
    return ans


def main():
    keypad = make_keypad()
    codes = get_input('line')
    print(f"Part 1 answer = {part1(keypad, codes)}")
    keypad = make_crosspad()
    print(f"Part 2 answer = {part1(keypad, codes)}")


main()

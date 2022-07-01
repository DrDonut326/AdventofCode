from collections import deque
from itertools import permutations



def swap_position(s: list, x: int, y: int):
    s[x], s[y] = s[y], s[x]
    return s


def swap_letter(s: list, x: str, y: str):
    xi = s.index(x)
    yi = s.index(y)
    s[xi], s[yi] = s[yi], s[xi]
    return s


def rotate(s, x):
    # Positive number = rotate right
    d = deque(s)
    d.rotate(x)
    return list(d)


def rotate_positionally(s, x):
    si = s.index(x)
    s = rotate(s, 1)
    s = rotate(s, si)
    if si >= 4:
        s = rotate(s, 1)
    return s


def reverse_span(s, x, y):
    span = s[x: y+1]
    span.reverse()
    s[x:y+1] = span
    return s


def move(s: list, x, y):
    m = s[x]
    del s[x]
    s.insert(y, m)
    return s


def get_codes():
    ans = []
    with open("input.txt") as f:
        for line in f:
            line = line.rstrip()
            if line.startswith('swap position'):
                # Swap position
                line = line.replace('swap position ', '')
                x, y = line.split(' with position ')
                ans.append(('swap pos', int(x), int(y)))

            elif line.startswith('swap letter'):
                line = line.replace('swap letter ', '')
                x, y = line.split(' with letter ')
                ans.append(('swap letter', x, y))

            elif line.startswith('rotate left') or line.startswith('rotate right'):
                line = line.replace('rotate ', '')
                line = line.replace(' steps', '')
                line = line.replace(' step', '')
                direction, x = line.split(' ')
                x = int(x)
                if direction == 'left':
                    x *= -1
                ans.append(('rotate', x))

            elif line.startswith('rotate based'):
                letter = line[-1]
                ans.append(('rotate pos', letter))

            elif line.startswith('reverse'):
                line = line.replace('reverse positions ', '')
                x, y = [int(z) for z in line.split(' through ')]
                ans.append(('reverse', x, y))

            elif line.startswith('move'):
                line = line.replace('move position ', '')
                x, y = [int(z) for z in line.split(' to position ')]
                ans.append(('move', x, y))

            else:
                print(line)
                raise EnvironmentError(f"Parsing error with line: {line}")

    return ans


def handle_code(s, c):
    name = c[0]
    if name == 'swap pos':
        return swap_position(s, c[1], c[2])

    if name == 'swap letter':
        return swap_letter(s, c[1], c[2])

    if name == 'rotate':
        return rotate(s, c[1])

    if name == 'rotate pos':
        return rotate_positionally(s, c[1])

    if name == 'reverse':
        return reverse_span(s, c[1], c[2])

    if name == 'move':
        return move(s, c[1], c[2])

    raise EnvironmentError("Bad code name couldn't parse.")


def scramble(s, codes):
    for code in codes:
        s = handle_code(s, code)
    result = ''.join(s)
    return result

def main():
    start_string = list('abcdefgh')
    codes = get_codes()
    part_1 = scramble(start_string, codes)


    goal_pass = 'fbgdceah'
    combs = permutations('abcdefgh', 8)
    # Go through permutations and find one that results in
    for comb in combs:
        result = scramble(list(comb), codes)
        if result == goal_pass:
            print(f"The password is: {comb}")



main()

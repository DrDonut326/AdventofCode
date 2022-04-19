from collections import deque
import re


def swap_position(arr, x, y):
    test = test_swap(arr, x, y)
    """Swap index x with index y"""
    t = arr[x]
    arr[x] = arr[y]
    arr[y] = t
    assert ''.join(list(arr)) == test


def test_swap(s, x, y):
    before = ''.join(list(s))
    s = list(s)
    a = s[x]
    b = s[y]
    s[x] = b
    s[y] = a
    s = ''.join(list(s))
    return s


def swap_elements(arr, x, y):
    """Swaps all elements x with y"""
    for i, z in enumerate(arr):
        if z == x:
            arr[i] = y
        elif z == y:
            arr[i] = x


def rotate_left(arr, n):
    """Rotates left n steps"""
    arr.rotate(-n)


def rotate_right(arr, n):
    arr.rotate(n)


def test_rotate_from_index(arr, x):
    s = ''.join(list(arr))
    i = s.index(x) + 1
    if i >= 5:
        i += 1
    for _ in range(i):
        s = s[-1] + s[0:-1]
    return s


def rotate_from_index(arr, x):
    test = test_rotate_from_index(arr, x)
    i = arr.index(x)
    rotate_right(arr, 1)
    rotate_right(arr, i)
    if i >= 4:
        rotate_right(arr, 1)
    assert ''.join(list(arr)) == test


def test_reverse_span(arr, x, y):
    s = ''.join(list(arr))
    sub = s[x:y+1]



def reverse_span(arr, x, y):
    """Reverses the slice starting x through y"""
    #test = test_reverse_span(arr, x, y)
    span = reversed(list(arr)[x:y + 1])
    i = x
    for letter in span:
        arr[i] = letter
        i += 1


def move_position(arr, x, y):
    movee = arr[x]
    del arr[x]
    arr.insert(y, movee)


def get_codes():
    """Returns a list of tuples, with code at the front and data behind"""
    ans = []
    raw_lines = []
    with open("input.txt") as f:
        for line in f:
            raw_lines.append(line.rstrip())
            line = line.rstrip()
            if line.startswith("swap position"):
                # swap position 4 with position 0
                c = ['swap position']
                line = line.replace("swap position ", "")
                line = line.replace(" with position ", ' ')
                x, y = line.split(' ')
                c.append(int(x))
                c.append(int(y))
                ans.append(tuple(c))

            elif line.startswith('swap letter'):
                # swap letter d with letter b
                c = ['swap letter']
                line = line.replace("swap letter ", "")
                line = line.replace(" with letter ", ' ')
                x, y = line.split(' ')
                c.append(x)
                c.append(y)
                ans.append(tuple(c))

            elif line.startswith('rotate left'):
                c = ['rotate left']
                line = line.replace('rotate left ', '')
                a, t = line.split(' ')
                c.append(int(a))
                ans.append(tuple(c))

            elif line.startswith('rotate right'):
                c = ['rotate left']
                line = line.replace('rotate right ', '')
                a, t = line.split(' ')
                c.append(int(a))
                ans.append(tuple(c))

            elif line.startswith('rotate based'):
                c = ['rotate based']
                line = line.replace('rotate based on position of letter ', '')
                c.append(line)
                ans.append(tuple(c))

            elif line.startswith('reverse positions'):
                c = ['reverse positions']
                line = line.replace('reverse positions ', '')
                x, y = line.split(' through ')
                c.append(int(x))
                c.append(int(y))
                ans.append(tuple(c))

            elif line.startswith('move position'):
                c = ['move position']
                line = line.replace('move position ', '')
                x, y = line.split(' to position ')
                c.append(int(x))
                c.append(int(y))
                ans.append(tuple(c))

            else:
                print(line)
                raise EnvironmentError("Invalid code detected in parsing")

    return ans, raw_lines


def part1(arr, codes):
    code_history = []
    for c in codes:
        if c[0] == 'swap position':
            swap_position(arr, c[1], c[2])
        elif c[0] == 'swap letter':
            swap_elements(arr, c[1], c[2])
        elif c[0] == 'rotate left':
            rotate_left(arr, c[1])
        elif c[0] == 'rotate right':
            rotate_right(arr, c[1])
        elif c[0] == 'rotate based':
            rotate_from_index(arr, c[1])
        elif c[0] == 'reverse positions':
            reverse_span(arr, c[1], c[2])
        elif c[0] == 'move position':
            move_position(arr, c[1], c[2])
        else:
            print(c)
            raise EnvironmentError("Unknown code in the code list")
        code_history.append(list(arr).copy())
    return code_history


def test_part1(codes):
    password = ["a","b","c","d","e","f","g","h"]
    code_history = []
    for input_line in codes:
        password_copy = password.copy()
        password_copy = deque(password_copy)
        if "swap position" in input_line:
            first_position = int(re.search("(\d).+(\d)", input_line).group(1))
            second_position = int(re.search("(\d).+(\d)", input_line).group(2))
            first_letter = password[first_position]
            second_letter = password[second_position]
            password[first_position] = second_letter
            password[second_position] = first_letter
            swap_position(password_copy, first_position, second_position)
            assert password == list(password_copy)

        elif "swap letter" in input_line:
            first_letter = re.search("(\D)\swith\sletter\s(\D)", input_line).group(1)
            second_letter = re.search("(\D)\swith\sletter\s(\D)", input_line).group(2)
            first_position = password.index(first_letter)
            second_position = password.index(second_letter)
            password[first_position] = second_letter
            password[second_position] = first_letter
            swap_elements(password_copy, first_letter, second_letter)
            assert password == list(password_copy)

        elif "rotate based" in input_line:
            letter = re.search("letter\s(\D)", input_line).group(1)
            letter_position = password.index(letter)
            number_of_rotations = letter_position + 1
            if letter_position >= 4:
                number_of_rotations += 1
            if number_of_rotations >= 8:
                number_of_rotations -= 8
            password = password[-number_of_rotations:] + password[:-number_of_rotations]
            rotate_from_index(password_copy, letter)
            assert password == list(password_copy)

        elif "rotate" in input_line:
            number_of_rotations = int(re.search("(\d)", input_line).group(1))
            if "left" in input_line:
                password = password[-(8-number_of_rotations):] + password[:-(8-number_of_rotations)]
                rotate_left(password_copy, number_of_rotations)
            elif "right" in input_line:
                password = password[-number_of_rotations:] + password[:-number_of_rotations]
                rotate_right(password_copy, number_of_rotations)
            assert password == list(password_copy)


        elif "reverse" in input_line:
            first_position = int(re.search("(\d).+(\d)", input_line).group(1))
            second_position = int(re.search("(\d).+(\d)", input_line).group(2))
            init_fp = first_position
            init_sp = second_position
            while first_position < second_position:
                first_letter = password[first_position]
                second_letter = password[second_position]
                password[first_position] = second_letter
                password[second_position] = first_letter
                first_position += 1
                second_position -= 1
            reverse_span(password_copy, init_fp, init_sp)
            print(password)
            print(list(password_copy))
            print()
            assert password == list(password_copy)

        elif "move" in input_line:
            first_position = int(re.search("(\d).+(\d)", input_line).group(1))
            second_position = int(re.search("(\d).+(\d)", input_line).group(2))
            letter = password.pop(first_position)
            password.insert(second_position, letter)
            move_position(password_copy, first_position, second_position)
            assert password == list(password_copy)

        code_history.append(password.copy())
    print(password)
    return code_history


def main():
    puzzle_input = 'abcdefgh'
    letter_list = deque(list(puzzle_input))
    codes, raw_lines = get_codes()
    correct_history = test_part1(raw_lines)



    history = part1(letter_list, codes)
    print(correct_history)
    print(history)
    print(f"Part 1 answer = {''.join(list(letter_list))}")
    # gfedhacb  not right
    # fdhbcgea was right




if __name__ == '__main__':
    main()

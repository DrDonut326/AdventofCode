from Day10 import part_2
from Grids import DictGrid
from Pos import Pos


def convert_hex_to_4_bit_binary(x):
    """Converts one character."""

    # Get the integer
    int_x = int(x, 16)

    # Switch to binary
    bin_x = bin(int_x)

    # Remove front fluff
    true_bin_x = bin_x[2:]

    # Add extra bits as ness
    real_true_bin_x = true_bin_x.zfill(4)

    return real_true_bin_x


def convert_hex_string_bin_string(x):
    ans = []
    for letter in x:
        ans.append(convert_hex_to_4_bit_binary(letter))
    return ''.join(ans)


def display_test_grid(row):
    ans = ''
    for letter in row[0:8]:
        if letter == '0':
            ans += '.'
        elif letter == '1':
            ans += '#'
        else:
            raise EnvironmentError('Something other than 0 or 1 used.')
    print(ans)


def part_1(disk):
    count = 0
    for row in disk:
        for x in row:
            if x == '1':
                count += 1
    print(count)


def main():
    # Put in puzzle input
    puzzle_input = 'hxtvlmkl'

    # Build grid
    disk = []
    for n in range(128):
        row = []
        combined_input = f"{puzzle_input}-{n}"
        hex_string = part_2(combined_input)
        t = convert_hex_string_bin_string(hex_string)
        for letter in t:
            row.append(letter)
        disk.append(row)

    part_1(disk)  # Part 1 answer


    # ------- Part 2
    # Convert to a grid class
    grid = DictGrid(str, bounded=True, x_size=128, y_size=128)
    grid.add_2D_array_to_grid(disk)

    regions = grid.get_regions('0')

    print(len(regions))  # Part 2 answer

main()

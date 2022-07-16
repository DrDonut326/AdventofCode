from functools import lru_cache

from Functions import Pos


@lru_cache()
def get_fuel_power(pos):
    x, y = pos.x, pos.y
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial
    power_level *= rack_id
    if power_level <= 99:
        power_level = 0
    else:
        if power_level > 0:
            power_level = int(str(power_level)[-3])
        else:
            power_level = int('-' + str(power_level)[-3])

    power_level -= 5
    assert type(power_level) == int
    return power_level


def get_square_fuel(pos, size):
    total = 0
    sx, sy = pos.x, pos.y
    for x in range(sx, sx + size):
        for y in range(sy, sy + size):
            pos = Pos(x, y)
            total += get_fuel_power(pos)
    return total


def get_column_fuel(pos, size):
    total = 0
    sx, sy = pos.x, pos.y
    for y in range(sy, sy + size):
        pos = Pos(sx, y)
        total += get_fuel_power(pos)
    return total


def get_row_fuel(pos, size):
    total = 0
    sx, sy = pos.x, pos.y
    for x in range(sx, sx + size):
        pos = Pos(x, sy)
        total += get_fuel_power(pos)
    return total


def find_largest_n_sized_square(size):
    # Find the first square
    x = 1
    y = 1

    # Setup bests
    best_fuel_square = None
    best_fuel_pos = None

    # Get max size
    max_size = 301 - size

    while y <= max_size:
        # Slide all the way across to the right
        # Subtracting the left side and adding the next right side only

        # Beginning of a row, set the current square size
        # Set current pos
        pos = Pos(x, y)

        # Set square size
        square_fuel = get_square_fuel(pos, size)

        # Check in case this is the best option
        # Check for besties
        if best_fuel_square is None or square_fuel > best_fuel_square:
            best_fuel_square = square_fuel
            best_fuel_pos = pos

        # Slide across the right
        while x < max_size:
            # Subtract the left side
            pos = Pos(x, y)
            square_fuel -= get_column_fuel(pos, size)

            # Increment x
            x += 1

            # Add the right side
            pos = Pos(x+(size - 1), y)
            square_fuel += get_column_fuel(pos, size)

            # Check for besties
            if square_fuel > best_fuel_square:
                best_fuel_square = square_fuel
                best_fuel_pos = Pos(pos.x - (size-1), pos.y)

        x = 1
        y += 1

    return best_fuel_square, best_fuel_pos


def main():
    square, pos = find_largest_n_sized_square(3)
    print(f"{pos.x},{pos.y}") # Part 1 answer

    # Part 2----------------
    best_square = None
    best_pos = None
    best_size = None
    for x in range(1, 21):
        print(f"Checking size: {x}")
        square, pos = find_largest_n_sized_square(x)
        if best_square is None or square > best_square:
            best_square = square
            best_pos = pos
            best_size = x

    print(f"{best_pos.x},{best_pos.y},{best_size}")  # Part 2 answer


serial = 1133
main()

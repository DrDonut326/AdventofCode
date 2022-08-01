from fractions import Fraction
from collections import defaultdict
from math import atan2, degrees

from Functions import manhat


def get_asteroids():
    """Returns the set of all asteroids by x y  position"""
    asteroids = set()
    with open("input.txt") as f:
        for y, line in enumerate(f):
            line = line.rstrip()
            for x, element in enumerate(line):
                if element == '#' or element == 'X':
                    asteroids.add((x, y))
    return asteroids


def get_slope(a, b):
    """Returns the slope between these two points."""
    rise = a[1] - b[1]
    run = a[0] - b[0]

    # Check for flat lines
    if run == 0:
        if rise > 0:
            return 1, 0
        else:
            return -1, 0

    if rise == 0:
        if run > 0:
            return 0, 1
        else:
            return 0, -1

    slope = Fraction(rise, run)

    n = abs(slope.numerator)
    d = abs(slope.denominator)

    if rise < 0:
        n *= -1

    if run < 0:
        d *= -1

    return n, d


def get_angle(point_1, point_2):
    angle = atan2(point_1[1] - point_2[1], point_1[0] - point_2[0])

    angle = degrees(angle)

    return angle


def how_many_asteroids_can_this_asteroid_see(aster_pos, asteroids):
    return len(create_slope_dict(aster_pos, asteroids))


def create_slope_dict(aster_pos, asteroids):
    slope_dict = defaultdict(list)

    for asteroid in asteroids:
        if asteroid != aster_pos:
            # Get slope between these two
            slope = get_slope(asteroid, aster_pos)
            slope_dict[slope].append(asteroid)

    return slope_dict


def part_1(asteroids):
    # Create a dict to store answers
    asteroids_see_count = dict()

    # Iterate and count
    for asteroid in asteroids:
        count = how_many_asteroids_can_this_asteroid_see(asteroid, asteroids)
        asteroids_see_count[asteroid] = count

    best_asteroid = max(asteroids_see_count.items(), key=lambda x: x[1])

    pos, count = best_asteroid
    #print(count)
    return pos





def part_2(best_pos, asteroids):
    home_base = best_pos
    slope_dict = create_slope_dict(home_base, asteroids)


    print(slope_dict[(-1, 0)])
    quit()

    boom_count = dict()
    boom_counter = 0

    target_slope = (0, -1)
    current_angle = 90.0
    if target_slope not in slope_dict:
        target_slope, current_angle = get_next_slope_and_angle(target_slope, current_angle)

    # If there is no asteroid at this target, then adjust to the next one

    # While there are asteroids remaining
    while slope_dict:
        # Increment the counter
        boom_counter += 1

        # Destroy the closest asteroid at this slope

        # Rotate to the next closest one clockwise



def main():
    asteroids = get_asteroids()
    best_pos = part_1(asteroids)
    # print(best_pos) # Part 1 answer
    part_2(best_pos, asteroids)


main()

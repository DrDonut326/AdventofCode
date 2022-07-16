# Every house gets present = 10 times each factor of that number
from collections import defaultdict

from Functions import factors


def part_1(target):
    house_number = 0
    while True:
        presents = 0
        house_number += 1
        facs = factors(house_number)
        for x in facs:
            presents += 10 * x
        if presents >= target:
            print(f"Part 1 answer: {house_number}")
            return


def part_2(target):
    house_number = 0
    visits = defaultdict(int)
    while True:
        presents = 0
        house_number += 1
        facs = factors(house_number)
        for x in facs:
            if visits[x] < 50:
                presents += 11 * x
                visits[x] += 1
        if presents >= target:
            print(f"Part 2 answer: {house_number}")
            return


def main():
    puzzle_target = 34000000
    part_1(puzzle_target)
    part_2(puzzle_target)


main()

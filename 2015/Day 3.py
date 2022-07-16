from collections import defaultdict
from Pos import Pos
from Functions import get_input
from queue import Queue as q


def move_santa(command, santa):
    directions = {'^' : (0, -1),
                  'v' : (0, +1),
                  '<' : (-1, 0),
                  '>' : (1, 0)}

    # Update Santa's position
    dx, dy = directions[command]
    santa.x += dx
    santa.y += dy


def deliver_present(santa, houses):
    houses[santa.get_name()] += 1


def print_total_present(houses):
    ans = 0
    for x in houses.values():
        ans += x
    print(ans)


def main(part):
    santa = Pos(0, 0)
    commands = get_input('char')
    houses = defaultdict(int)

    robo_santa = Pos(0, 0)
    command_queue = q()
    for command in commands:
        command_queue.put(command)

    if part == 1:
        # Part 1
        deliver_present(santa, houses)
        for command in commands:
            move_santa(command, santa)
            deliver_present(santa, houses)
        print(len(houses.keys()))

    else:
        # Part 2
        deliver_present(santa, houses)
        deliver_present(robo_santa, houses)
        turn = 'real'
        while not command_queue.empty():
            if turn == 'real':
                move_santa(command_queue.get(), santa)
                deliver_present(santa, houses)
                turn = 'fake'
            else:
                move_santa(command_queue.get(), robo_santa)
                deliver_present(robo_santa, houses)
                turn = 'real'
        print(len(houses.keys()))

main(2)

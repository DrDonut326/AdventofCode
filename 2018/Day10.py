from Pos import Pos
from Grids import DictGrid
from collections import defaultdict


def get_input():
    lights = []
    with open("input.txt") as f:
        for line in f:
            line = line.rstrip()
            line = line.replace('position=<', ' ')
            line = line.replace('>', '')
            line = line.replace('velocity=<', ' ')
            line = line.replace(', ', ' ')
            x, y, dx, dy = [int(z) for z in line.split()]
            pos = Pos(x, y, dx=dx, dy=dy)
            lights.append(pos)
    return lights


def make_grid(lights):
    grid = DictGrid(None)
    for light in lights:
        grid.add_data_to_grid_at_pos(light, light)
    grid.set_size()
    return grid


def show_lights(lights):
    grid = make_grid(lights)
    grid.display_grid_ascii(data_override='*')


def get_total_distance(lights):
    total = 0
    for light in lights:
        total += abs(light.x)
        total += abs(light.y)
    return total


def get_same_y_count(lights):
    sames = defaultdict(int)
    for light in lights:
        sames[light.y] += 1
    # Get max same score
    total = max(sames.values())
    return total


def update_lights(lights):
    for light in lights:
        light.x += light.dx
        light.y += light.dy





def main():
    lights = get_input()
    same = 0
    seconds = 1
    while same < 22:
        seconds += 1
        update_lights(lights)
        same = get_same_y_count(lights)

    print(seconds)


main()

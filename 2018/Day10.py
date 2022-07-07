from Pos import Pos
from Grids import DictGrid


def get_input(speed_multiplier):
    lights = []
    with open("input.txt") as f:
        for line in f:
            line = line.rstrip()
            line = line.replace('position=<', ' ')
            line = line.replace('>', '')
            line = line.replace('velocity=<', ' ')
            line = line.replace(', ', ' ')
            x, y, dx, dy = [int(z) for z in line.split()]
            dx *= speed_multiplier
            dy *= speed_multiplier
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



def update_lights(lights: list):
    light: Pos
    for light in lights:
        print(light)

        quit()

def main():
    lights = get_input(1)
    update_lights(lights)
    show_lights(lights)


main()

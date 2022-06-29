from Grids import DictGrid
from Pos import Pos


class Sporeifica:
    """A next level nano-virus with no known cure.
    Only able to be contained using grid computing clusters."""
    def __init__(self, grid: DictGrid, pos: Pos, direction=(0, -1)):
        self.grid = grid
        self.pos = pos
        self.direction = direction
        self.infections_caused = 0

    def turn_right(self):
        # Up
        if self.direction == (0, -1):
            self.direction = (1, 0)

        # Right
        elif self.direction == (1, 0):
            self.direction = (0, 1)

        # Down
        elif self.direction == (0, 1):
            self.direction= (-1, 0)

        #left
        elif self.direction == (-1, 0):
            self.direction = (0, -1)

        else:
            raise EnvironmentError("Virus direction unknown or bad value.")

    def turn_left(self):
        # Up
        if self.direction == (0, -1):
            self.direction = (-1, 0)

        # Right
        elif self.direction == (-1, 0):
            self.direction = (0, 1)

        # Down
        elif self.direction == (0, 1):
            self.direction = (1, 0)

        # left
        elif self.direction == (1, 0):
            self.direction = (0, -1)

    def is_current_node_infected(self):
        node_status = self.grid.get_value_from_pos_object(self.pos)
        return node_status == '#'

    def move_forward(self):
        x, y = (self.pos.x, self.pos.y)
        dx, dy = self.direction
        x += dx
        y += dy
        self.pos = Pos(x, y)

    def burst(self):
        # Turn right or left
        if self.is_current_node_infected():
            self.turn_right()
        else:
            self.turn_left()

        # Clean or infect
        if self.is_current_node_infected():
            self.grid.add_data_to_grid_at_pos('.', self.pos)
        else:
            self.grid.add_data_to_grid_at_pos('#', self.pos)
            self.infections_caused += 1

        # Move forward one space
        self.move_forward()


class Evolved(Sporeifica):

    def is_current_node_infected(self):
        node_status = self.grid.get_value_from_pos_object(self.pos)
        return node_status == '#'

    def is_current_node_clean(self):
        node_status = self.grid.get_value_from_pos_object(self.pos)
        return node_status == '.' or node_status == ''

    def is_current_node_weak(self):
        node_status = self.grid.get_value_from_pos_object(self.pos)
        return node_status == 'W'

    def is_current_node_flagged(self):
        node_status = self.grid.get_value_from_pos_object(self.pos)
        return node_status == 'F'

    def burst(self):
        # Turn right or left
        if self.is_current_node_clean():
            self.turn_left()

        elif self.is_current_node_weak():
            pass

        elif self.is_current_node_infected():
            self.turn_right()

        elif self.is_current_node_flagged():
            self.turn_right()
            self.turn_right()

        else:
            raise EnvironmentError("Virus not sure what to do.")

        # Clean or infect
        if self.is_current_node_clean():
            self.grid.add_data_to_grid_at_pos('W', self.pos)

        elif self.is_current_node_weak():
            self.grid.add_data_to_grid_at_pos('#', self.pos)
            self.infections_caused += 1

        elif self.is_current_node_infected():
            self.grid.add_data_to_grid_at_pos('F', self.pos)

        elif self.is_current_node_flagged():
            self.grid.add_data_to_grid_at_pos('.', self.pos)

        else:
            raise EnvironmentError('Strange object on board, virus does not know what to do.')

        # Move forward one space
        self.move_forward()


def display_2d_array(arr):
    for row in arr:
        print(row)
    print()


def get_map():
    grid_map = []
    with open("input.txt") as f:
        for line in f:
            line = line.rstrip()
            grid_map.append(list(line))
    return grid_map


def locate_center_of_grid(grid_map):
    # Make sure the grid is odd shaped
    assert len(grid_map) % 2 != 0
    assert len(grid_map[0]) % 2 != 0

    y = len(grid_map) // 2
    x = len(grid_map[0]) // 2

    return Pos(x, y)


def get_grid(grid_map):
    grid = DictGrid(str, bounded=False)
    grid.add_2D_array_to_grid(grid_map)
    return grid

def main():
    grid_map = get_map()
    grid = get_grid(grid_map)
    start_pos = locate_center_of_grid(grid_map)

    sporeifica = Sporeifica(grid, start_pos)

    for _ in range(10000):
        sporeifica.burst()

    print(sporeifica.infections_caused) # Part 1 answer

    grid_map = get_map()
    grid = get_grid(grid_map)
    start_pos = locate_center_of_grid(grid_map)

    evolved_virus = Evolved(grid, start_pos)

    for _ in range(10000000):
        evolved_virus.burst()

    print(evolved_virus.infections_caused)  # Part 2 answer

main()

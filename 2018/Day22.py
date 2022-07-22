from functools import lru_cache
from Utility.Pathfinding import dijkstra_dictgrid
from Classes.Grids import DictGrid

class Cave:
    risk_dict = {'rocky': 0, 'wet': 1, 'narrow': 2}
    risk_symbols = {'rocky': '.', 'wet': '=', 'narrow': '|'}

    def __init__(self, pos, target_pos, depth):
        self.pos = pos
        self.target_pos = target_pos
        self.depth = depth

    @lru_cache(maxsize=None)
    def get_geologic_index(self, pos):
        x, y = pos

        if pos == (0, 0):
            return 0

        if pos == self.target_pos:
            return 0

        if y == 0:
            return x * 16807

        if x == 0:
            return y * 48271

        return self.get_erosion_level((x-1, y)) * self.get_erosion_level((x, y-1))

    @lru_cache(maxsize=None)
    def get_erosion_level(self, pos):
        return (self.get_geologic_index(pos) + self.depth) % 20183

    @lru_cache(maxsize=None)
    def get_risk_type(self, pos):
        fine_erosion = self.get_erosion_level(pos) % 3
        if fine_erosion == 0:
            return 'rocky'
        elif fine_erosion == 1:
            return 'wet'
        elif fine_erosion == 2:
            return 'narrow'
        else:
            raise EnvironmentError('bad erosion type')

    def get_total_risk(self):
        total_risk = 0
        for y in range(0, self.target_pos[1] + 1):
            for x in range(0, self.target_pos[0] + 1):
                pos = (x, y)
                total_risk += self.risk_dict[self.get_risk_type(pos)]
        return total_risk

    def get_allowable_equipment(self, cave_type):
        if cave_type == 'rocky':
            return [1, 2]
        if cave_type == 'wet':
            return [0, 2]
        if cave_type == 'narrow':
            return [0, 1]


def find_neighbors_cave(grid: DictGrid, pos: tuple):
    # Get neighbros
    neighbors = grid.get_neighbors_4way(pos[0], pos[1])

    # Prune < 0
    neighbors = [n for n in neighbors if n[0] >= 0 and n[1] >=0]

    # Locate the type of this current position???
    # todo: is this a tuple with cost or what?
    print(neighbors)


def part_1(target, depth):
    cave = Cave((0, 0), target, depth)
    print(cave.get_total_risk())
    return cave


def add_locations_to_grid(grid: DictGrid, cave: Cave, pos: tuple):
    """Given a location in the cave, adds appropriate z level dimensions to it."""
    # 0 = neither equipment
    # 1 = torch
    # 2 = climbing gear

    # Get the type of this location
    cave_type = cave.get_risk_type(pos)

    # Get allowable equipment numbers
    equip_nums = cave.get_allowable_equipment(cave_type)

    # Add each equipment number as a z value to the tuple
    for equip in equip_nums:
        cave_pos = (pos[0], pos[1], equip)

        # Add it to the grid as a location
        grid.add_data_to_grid_at_pos(cave_pos, cave.risk_symbols[cave_type])

def main():
    depth = 10647
    target_pos = (7, 770)
    cave = part_1(target_pos, depth)  # Part 1 answer

    grid = DictGrid(str)
    grid

main()

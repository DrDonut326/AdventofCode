from functools import lru_cache
from Utility.Pathfinding import dijkstra_dictgrid, rebuild_path
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
    def get_terrain_type(self, pos):
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
                total_risk += self.risk_dict[self.get_terrain_type(pos)]
        return total_risk

    def get_allowable_equipment(self, cave_type):
        if cave_type == 'rocky':
            return [1, 2]
        if cave_type == 'wet':
            return [0, 2]
        if cave_type == 'narrow':
            return [0, 1]


def find_neighbors_cave(grid: DictGrid, pos: tuple):
    """Function that will be passed to the Dijkstra function to find neighbors.
    Each neighbor will return a tuple of (pos, cost)"""
    global cave
    ans = []

    # First add equipment change

    # Get the current positions terrain type
    current_terrain = cave.get_terrain_type((pos[0], pos[1]))

    # Find what equipment is allowed there
    current_allow_equip = cave.get_allowable_equipment(current_terrain)

    # Add the one you don't have equipped
    for equip in current_allow_equip:
        if equip != pos[2]:

            # Add this equipment to the answer
            new_pos = (pos[0], pos[1], equip)
            cost = 7
            ans.append((new_pos, cost))

    # Now get neighbors of the current position
    # that the current equipment are allowed in

    # Get 2d neighbors of this position
    neighbors = grid.get_neighbors_4way(pos[0], pos[1])

    # Prune < 0
    neighbors = [n for n in neighbors if n[0] >= 0 and n[1] >= 0]

    for neighbor in neighbors:
        # Get terrain type
        terrain_type = cave.get_terrain_type((neighbor[0], neighbor[1]))

        # Get the allowable equipment
        allow_equip = cave.get_allowable_equipment(terrain_type)

        # Get the current equipped numbed
        currently_equipped = pos[2]

        # If the currently equipped item is allowed in the next zone, add it to neighbors
        if currently_equipped in allow_equip:

            # Make new position
            new_pos = (neighbor[0], neighbor[1], currently_equipped)
            cost = 1
            priority = (new_pos, cost)
            ans.append(priority)

    return ans


def part_1(target, depth):
    cave = Cave((0, 0), target, depth)
    print(cave.get_total_risk())
    return cave


def main():
    grid = DictGrid(str)
    came_from, cost_so_far = dijkstra_dictgrid(grid, (0, 0, 1), target_pos, find_neighbors_cave)
    print(cost_so_far[target_pos])

depth = 10647
target_pos = (7, 770, 1)
cave = part_1(target_pos, depth)
main()

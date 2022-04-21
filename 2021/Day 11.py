from Grids import DictGrid
from Utility import get_input
from Pos import Pos


class Octopus:
    def __init__(self, energy):
        self.energy = energy
        self.flashed = False

    def __repr__(self):
        return str(self.energy)

    def energy_up(self):
        """Increases the energy level by 1.
        Returns True if it just flashed."""
        self.energy += 1
        if not self.flashed and self.energy > 9:
            self.flashed = True
            return True
        return False

    def reset(self):
        """Resets the energy to 0 if it flashed this turn
        Returns True if there was a flash"""
        if self.flashed:
            self.energy = 0
            self.flashed = False
            return True
        return False


def octo_update_from_pos(p, oct_map):
    octopus = oct_map.grid[oct_map.get_string_pos_key(p)]
    # --- Energy up while checking for flash
    if octopus.energy_up():
        # If it flashes, increase neighbor's energy that haven't flashed
        oct_neighbors = oct_map.get_neighbors_8way(p, exist=True)

        # Prune any neighbors that flashed
        pruned_neighbors = []
        for next_p in oct_neighbors:
            next_octopus = oct_map.grid[oct_map.get_string_pos_key(next_p)]
            if not next_octopus.flashed:
                pruned_neighbors.append(next_p)

        # Recurse through he list of pruned neighbors
        for final_p in pruned_neighbors:
            octo_update_from_pos(final_p, oct_map)


def update_octopi(octopi, oct_map):
    all_flashed = True
    # Increase all the energy levels (recursion included)
    for y, row in enumerate(octopi):
        for x, element in enumerate(row):
            # Increase energy of octopus
            p = Pos(x, y)
            octo_update_from_pos(p, oct_map)

    # Reset energy levels of flashers
    for y, row in enumerate(octopi):
        for x, element in enumerate(row):
            p = Pos(x, y)
            octopus = oct_map.grid[oct_map.get_string_pos_key(p)]
            if not octopus.reset():
                all_flashed = False

    return all_flashed




def make_oct_map(octopi):
    oct_map = DictGrid(datatype=None)
    for y, row in enumerate(octopi):
        for x, element in enumerate(row):
            o = Octopus(element)
            oct_map.add_data_to_grid_at_x_y_z(o, x, y)
    return oct_map




def main():
    octopi = get_input('line', int_split=True)
    oct_map = make_oct_map(octopi)
    oct_map.display_grid_ascii()

    time_count = 0

    all_same = False
    # Update
    while not all_same:
        time_count += 1
        all_same = update_octopi(octopi, oct_map)

    oct_map.display_grid_ascii()
    print(time_count)





main()

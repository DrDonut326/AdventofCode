from collections import defaultdict
from Pos import Pos
from queue import Queue
from math import inf

# TODO: Remove get neighbors and let pos objects handle that

class DictGrid:
    """
    A grid where locations are only generated as they are explored
    North or Up is Negative on the y-axis
    Left or West is Negative on the x-axis
    """
    def __init__(self, datatype, walls=None, bounded=True, max_x=None, max_y=None):
        self.bounded = bounded
        self.datatype = datatype
        self.walls = walls
        self.grid = defaultdict(datatype)
        self.max_x = max_x
        self.max_y = max_y
        # (dx, dy) pairs for navigating

    def add_data_to_grid_at_x_y_z(self, data, x, y, z=0):
        pos = Pos(x, y, z)
        self.add_data_to_grid_at_pos(pos, data)

    def add_data_to_grid_at_pos(self, pos, data):
        """Handles how data gets added depending on the data type."""
        assert type(pos) == Pos
        if self.datatype == list:
            self.grid[pos].append(data)

        elif self.datatype == set:
            self.grid[pos].add(data)

        elif self.datatype == int:
            self.grid[pos] += data

        elif self.datatype == str:
            self.grid[pos] = data

        elif self.datatype is None:
            self.grid[pos] = data

        else:
            raise NotImplemented(f"Datatype of {self.datatype} not implemented yet.")

    def get_graph_min_max(self):
        min_x = None
        min_y = None
        max_x = None
        max_y = None
        for key in self.grid.keys():
            x, y = key.x, key.y
            if min_x is None or x < min_x:
                min_x = x
            if max_x is None or x > max_x:
                max_x = x
            if min_y is None or y < min_y:
                min_y = y
            if max_y is None or y > max_y:
                max_y = y
        return min_x, max_x, min_y, max_y

    def display_grid_ascii(self, data_override=None):
        print('-' * 25)
        min_x, max_x, min_y, max_y = self.get_graph_min_max()
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                t = Pos(x, y)
                if t in self.grid:
                    if data_override is None:
                        print(self.grid[t], end='')
                    else:
                        print(data_override, end='')
                else:
                    print(' ', end='')
            print()
        print('-' * 25)

    def get_value_from_pos_object(self, pos):
        return self.grid[pos]

    def flood_neighbors(self, pos, visited, master_visited=None):
        """Returns a neighbors list pruned by visited and wall"""
        neighbors = pos.get_neighbors_4way(pos, exist=True) #TODO: add wall_exception
        if master_visited is None:
            master_visited = set()
        ans = []
        for p in neighbors:
            # Prune for visited + master visited
            if p not in visited and p not in master_visited:
                ans.append(p)
        return ans

    def flood(self, start_pos, wall=None, master_visited=None):
        """Floods outwards from the starting position
        Does not pass through tiles equaling 'wall'
        Returns a list of positions."""

        # If this position is itself a wall, return an empty set
        if self.get_value_from_pos_object(start_pos) == wall:
            return []

        visited = set()
        if master_visited is None:
            master_visited = set()
        q = Queue()

        visited.add(start_pos)
        master_visited.add(start_pos)
        q.put(start_pos)

        while not q.empty():
            s = q.get()
            s_neighbors = self.flood_neighbors(s, wall, visited)
            for neighbor in s_neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    master_visited.add(neighbor)
                    q.put(neighbor)

        return visited

    def get_regions(self, wall):
        """Returns a list of all regions and their positions"""
        master_visited = set()
        regions = []
        # Iterate through all positions on the grid
        # Ignoring those already found in master_visited
        for y in range(self.y_size):
            for x in range(self.x_size):

                # Create a pos object
                pos = Pos(x, y)

                # Skip if you're starting on a wall
                if self.get_value_from_pos_object(pos) != wall:

                    # See if the pos object is already visited
                    if pos not in master_visited:
                        flood = self.flood(pos, wall, master_visited)
                        assert len(flood) > 0
                        regions.append(flood)

        return regions

    def add_2D_array_to_grid(self, arr):
        """Converts the array to x, y position and adds it to this graph"""
        for y, row in enumerate(arr):
            for x, element in enumerate(row):
                p = Pos(x, y)
                self.add_data_to_grid_at_pos(p, element)

    def make_pos_from_x_y(self, x, y):
        ans = Pos(x, y)
        return ans

    def get_costs(self, start):
        # Dictionary of positions: cost
        ans = defaultdict(int)

        # Iterate and create
        for pos in self.grid:
            ans[pos] = inf

        # Set the starting position to value 0
        ans[start] = 0

        return ans

    def colored(self, r, g, b, text):
        return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

    def get_pos_object_from_value(self, v):
        for item in self.grid.items():
            if item[1] == v:
                return item[0]
        raise Exception("Was not found.")

    def display_grid_with_highlighted_values(self, rgb_dict):
        """Highlights all values in dict according to the given dictionary [value]: color_tuple"""
        print('-' * 25)
        min_x, max_x, min_y, max_y = self.get_graph_min_max()
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                pos = Pos(x, y)
                if pos in self.grid:
                    element = str(self.grid[pos])
                    if element in rgb_dict:
                        r, g, b = rgb_dict[element]
                        print(self.colored(r, g, b, element), end='')
                    else:
                        print(element, end='')
                else:
                    print('.', end='')
            print()
        print('-' * 25)

    def display_grid_with_highlighted_positions_by_dictionary(self, rgb_dict):
        """Highlights all values in dict according to the given dictionary [pos]: color_tuple"""
        print('-' * 25)
        min_x, max_x, min_y, max_y = self.get_graph_min_max()
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                pos = Pos(x, y)
                if pos in self.grid:
                    element = str(self.grid[pos])
                    if pos in rgb_dict:
                        r, g, b = rgb_dict[pos]
                        print(self.colored(r, g, b, element), end='')
                    else:
                        print(element, end='')
                else:
                    print('.', end='')
            print()
        print('-' * 25)

    def display_grid_with_highlighted_positions_all_same(self, positions, rgb_choice):
        """Highlights all positions given with the same color."""
        print('-' * 25)
        min_x, max_x, min_y, max_y = self.get_graph_min_max()
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                pos = Pos(x, y)
                if pos in self.grid:
                    element = str(self.grid[pos])
                    if pos in positions:
                        r, g, b = rgb_choice
                        print(self.colored(r, g, b, element), end='')
                    else:
                        print(element, end='')
                else:
                    print('.', end='')
            print()
        print('-' * 25)

    def set_size(self):
        sizes = self.get_graph_min_max()
        self.x_size = sizes[1] + 1
        self.y_size = sizes[3] + 1




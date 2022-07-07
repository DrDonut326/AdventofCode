from collections import defaultdict
from Pos import Pos
from queue import Queue
from math import inf


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
        self.four_way_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.eight_way_directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

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

    def prune_neighbors(self, pos_list, exist, visited: set):
        ans = pos_list
        # If the grid has a max size, make sure it is under that
        if self.bounded:
            # Check for x
            if self.max_x is not None:
                ans = [x for x in ans if 0 <= x.x < self.max_x]

            # Check for y
            if self.max_y is not None:
                ans = [x for x in ans if 0 <= x.y < self.max_y]

        # Prune for pre-existing positions
        if exist:
            ans = [x for x in ans if x in self.grid]

        # Prune for walls
        if self.walls is not None:
            assert type(self.walls) == set
            ans = [x for x in ans if self.get_value_from_pos_object(x) not in self.walls]

        # Prune for visited
        if visited is not None:
            assert type(visited) == set
            ans = [x for x in ans if x not in visited]

        return ans

    def get_neighbors_4way(self, pos, exist=False, visited: set = None):
        """Returns an array of neighbors using only North, South, East, West (No diagonals).
        If the array is bounded, only in-bounds neighbors
        If exist is True, only pre-existing neighbors
        Wall will prune for any symbols passed in as a wall.
        Visited will prune for any positions passed in."""

        # Get all possible new directions
        pos_list = []
        for d in self.four_way_directions:
            nx = pos.x + d[0]
            ny = pos.y + d[1]
            pos_list.append(Pos(nx, ny))

        pruned = self.prune_neighbors(pos_list, exist, visited)
        return pruned

    def get_neighbors_8way(self, pos, exist=False, visited: set = None):
        """Returns an array of neighbors using only using 8 directions (with diagonals).
        If the array is bounded, only in-bounds neighbors
        If exist is True, only pre-existing neighbors
        Wall will prune for any symbols passed in as a wall.
        Visited will prune for any positions passed in."""

        pos_list = []
        for d in self.eight_way_directions:
            nx = pos.x + d[0]
            ny = pos.y + d[1]
            pos_list.append(Pos(nx, ny))

        pruned = self.prune_neighbors(pos_list, exist, visited)
        return pruned

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
                    print('.', end='')
            print()
        print('-' * 25)

    def get_value_from_pos_object(self, pos):
        return self.grid[pos]

    def flood_neighbors(self, pos, visited, master_visited=None):
        """Returns a neighbors list pruned by visited and wall"""
        neighbors = self.get_neighbors_4way(pos, exist=True)
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

    def get_smallest_cost(self, costs, visited):
        """Returns the position of the lowest cost
        that has not yet been visited"""
        items = costs.items()
        ans = ''
        best = inf

        # Iterate through items, noting down the smallest
        for pos, cost in items:
            if pos not in visited and cost < best:
                ans = pos
                best = cost

        return ans

    def get_adjacency_graph(self):
        """Returns a graph that shows what positions are connected to each other"""
        ans = defaultdict(list)
        for pos in self.grid:
            if self.grid[pos] not in self.walls:
                # Get list of neighbor pos objects
                neighbors = self.get_neighbors_4way(pos, exist=True)

                # Add each neighbor to the adjacency graph
                for neighbor in neighbors:
                    ans[pos].append(neighbor)

        return ans

    def update_costs(self, pos, costs, adjacent, all_cost):
        """Updates each neighbor of pos if the current cost is less than previous"""
        # TODO: By default this assume grid square values are showing their cost
        if all_cost is not None:
            assert type(all_cost) == int

        current_pos_cost = costs[pos]

        neighbors = adjacent[pos]

        for neighbor in neighbors:
            # Get the cost of travel to that node
            if all_cost is None:
                travel_cost = current_pos_cost + self.grid[neighbor]
            else:
                travel_cost = current_pos_cost + all_cost

            # Get the current cost
            current_cost = costs[neighbor]

            # Compare with the current node
            if travel_cost < current_cost:
                # Update the costs
                costs[neighbor] = travel_cost

    def dijkstra(self, start: Pos, finish: Pos, all_cost=None):
        # print(f"Finding shortest path between {start} and {finish}")
        # Create cost dictionary
        costs = self.get_costs(start)

        # Create adjacency graph
        adjacent = self.get_adjacency_graph()

        # Create a visited set
        visited = set()

        while len(visited) < len(costs):
            # Get the smallest cost
            smallest_cost_pos = self.get_smallest_cost(costs, visited)

            # Add to visited
            visited.add(smallest_cost_pos)

            # Update costs
            self.update_costs(smallest_cost_pos, costs, adjacent, all_cost)

            # Check for finish
            if costs[finish] < inf:
                return costs[finish]

    def colored(self, r, g, b, text):
        return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

    def get_pos_object_from_value(self, v):
        for item in self.grid.items():
            if item[1] == v:
                return item[0]
        raise Exception("Was not found.")

    def display_grid_with_highlighted_positions(self, pos_list, rgb=(255, 100, 50)):
        print('-' * 25)
        min_x, max_x, min_y, max_y = self.get_graph_min_max()
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                t = Pos(x, y)
                if t in self.grid:
                    p = str(self.grid[t])
                    if t in pos_list:
                        r, g, b = rgb
                        print(self.colored(r, g, b, p), end='')
                    else:
                        print(p, end='')
                else:
                    print('.', end='')
            print()
        print('-' * 25)

    def set_size(self):
        sizes = self.get_graph_min_max()
        self.x_size = sizes[1] + 1
        self.y_size = sizes[3] + 1

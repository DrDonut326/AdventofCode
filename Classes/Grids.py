from collections import defaultdict
from Pos import Pos
from queue import Queue
from math import inf


class DictGrid:
    """
    A grid where locations are only generated as they are explored
    North or Up is Negative on the y-axis
    Left or West is Negative on the x-axis
    Grid dictionary is using with pos objects converted to string data for keys
    Works with Pos objects.  Use pos.get_name() for the string rep
    """
    def __init__(self, datatype=list, bounded=True, x_size=None, y_size=None):
        self.bounded = bounded
        self.x_size = x_size
        self.y_size = y_size
        self.datatype = datatype
        self.grid = defaultdict(datatype)
        # (dx, dy) pairs for navigating
        self.four_way_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.eight_way_directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

    def add_data_to_grid_at_x_y_z(self, data, x, y, z=0):
        pos = Pos(x, y, z)
        self.add_data_to_grid_at_pos(data, pos)

    def get_string_pos_key(self, pos):
        return pos.get_name()

    def add_data_to_grid_at_pos(self, data, pos):
        if self.datatype == list:
            self.grid[pos.get_name()].append(data)
        elif self.datatype == set:
            self.grid[pos.get_name()].add(data)
        elif self.datatype == int:
            self.grid[pos.get_name()] += data
        elif self.datatype == str:
            self.grid[pos.get_name()] = data
        elif self.datatype is None:
            self.grid[pos.get_name()] = data
        else:
            raise NotImplemented(f"Datatype of {self.datatype} not implemented yet.")

    def get_neighbors_4way(self, pos, exist=False):
        """Returns an array of neighbors.
        If the array is bounded, only in-bounds neighbors
        If exist is True, only pre-existing neighbors"""
        ans = []
        # Get all possible new directions
        for d in self.four_way_directions:
            nx = pos.x + d[0]
            ny = pos.y + d[1]
            ans.append(Pos(nx, ny))

        # If the grid has a max size, make sure it is under that
        if self.bounded:
            cleaned_ans = []
            for p in ans:
                if 0 <= p.x < self.x_size and 0 <= p.y < self.y_size:
                    cleaned_ans.append(p)
            ans = cleaned_ans

        # Clean answers: Step 2. If the position is not already existing in the array, dump it
        if exist:
            cleaned_ans = []
            for pos in ans:
                if pos.get_name() in self.grid:
                    cleaned_ans.append(pos)
            ans = cleaned_ans
        return ans

    def get_neighbors_8way(self, pos, exist=False):
        """Returns an array of neighbors.
        If the array is bounded, only in-bounds neighbors
        If exist is True, only pre-existing neighbors"""
        ans = []
        for d in self.eight_way_directions:
            nx = pos.x + d[0]
            ny = pos.y + d[1]
            ans.append(Pos(nx, ny))

        # Clean answers: Step 1.  If the grid is bounded, trip OOB
        if self.bounded:
            cleaned_ans = []
            for p in ans:
                if 0 <= p.x < self.size.x and 0 <= p.y < self.size.y:
                    cleaned_ans.append(p)
            ans = cleaned_ans

        # Clean answers: Step 2. If the position is not already existing in the array, dump it
        if exist:
            cleaned_ans = []
            for pos in ans:
                if pos.get_name() in self.grid:
                    cleaned_ans.append(pos)
            ans = cleaned_ans
        return ans

    def parse_pos_string(self, s):
        x, right = s.split('X | ')
        x = int(x)
        y = right[0:-1]
        y = int(y)
        return x, y

    def get_pos_from_string_key(self, key):
        x, y = self.parse_pos_string(key)
        pos = Pos(x, y)
        return pos

    def get_graph_min_max(self):
        min_x = None
        min_y = None
        max_x = None
        max_y = None
        for key in self.grid.keys():
            x, y = self.parse_pos_string(key)
            if min_x is None or x < min_x:
                min_x = x
            if max_x is None or x > max_x:
                max_x = x
            if min_y is None or y < min_y:
                min_y = y
            if max_y is None or y > max_y:
                max_y = y
        return min_x, max_x, min_y, max_y

    def display_grid_ascii(self):
        print('-' * 25)
        min_x, max_x, min_y, max_y = self.get_graph_min_max()
        for y in range(min_y, max_y + 1):
            row = []
            for x in range(min_x, max_x + 1):
                t = Pos(x, y)
                if t.get_name() in self.grid:
                    row.append(self.grid[t.get_name()])
                else:
                    row.append('.')
            print(row)
        print('-' * 25)

    def get_value_from_pos_object(self, pos):
        name = self.get_string_pos_key(pos)
        return self.grid[name]

    def flood_neighbors(self, pos, wall, visited, master_visited=None):
        """Returns a neighbors list pruned by visited and wall"""
        neighbors = self.get_neighbors_4way(pos, exist=True)
        if master_visited is None:
            master_visited = set()
        ans = []
        for p in neighbors:
            # Prune for visited + master visited
            if p not in visited and p not in master_visited:
                # Prune for wall (if applicable)
                if wall is not None:
                    if self.get_value_from_pos_object(p) != wall:
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
                self.add_data_to_grid_at_pos(element, p)

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
        ans[start.get_name()] = 0

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
            pos_ob = self.get_pos_from_string_key(pos)
            # Get list of neighbor pos objects
            neighbors = self.get_neighbors_4way(pos_ob, True)

            # Add each neighbor to the adjacency graph
            for neighbor in neighbors:
                ans[pos].append(neighbor.get_name())

        return ans

    def update_costs(self, pos, costs, adjacent):
        """Updates each neighbor of pos if the current cost is less than previous"""
        current_pos_cost = costs[pos]

        neighbors = adjacent[pos]

        for neighbor in neighbors:
            # Get the cost of travel to that node
            travel_cost = current_pos_cost + self.grid[neighbor]

            # Get the current cost
            current_cost = costs[neighbor]

            # Compare with the current node
            if travel_cost < current_cost:
                # Update the costs
                costs[neighbor] = travel_cost

    def dijkstra(self, start: Pos, finish: Pos):
        print("Finding shortest path...")
        # Create cost dictionary
        costs = self.get_costs(start)

        # Create adjecenty graph
        adjacent = self.get_adjacency_graph()

        # Create a visited set
        visited = set()

        while len(visited) < len(costs):
            # Get the smallest cost
            smallest_cost_pos = self.get_smallest_cost(costs, visited)

            # Add to visited
            visited.add(smallest_cost_pos)

            # Update costs
            self.update_costs(smallest_cost_pos, costs, adjacent)

            # Check for finish
            if costs[finish.get_name()] < inf:
                return costs[finish.get_name()]







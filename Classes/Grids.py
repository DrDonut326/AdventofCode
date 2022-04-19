from collections import defaultdict
from Pos import Pos
from queue import Queue

class DictGrid:
    """
    A grid where locations are only generated as they are explored
    North or Up is Negative on the y-axis
    Left or West is Negative on the x-axis
    Grid dictionary is using with pos objects converted to string data for keys
    Works with Pos objects.  Use pos.get_name() for the string rep
    """
    def __init__(self, datatype=list, size=None):
        if size is not None:
            self.bounded = True
            self.size = size
        else:
            self.bounded = False
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
        else:
            raise NotImplemented(f"Datatype of {self.datatype} not implemented yet.")

    def get_neighbors_4way(self, pos, exist=False):
        """Returns an array of neighbors.
        If the array is bounded, only in-bounds neighbors
        If exist is True, only pre-existing neighbors"""
        ans = []
        for d in self.four_way_directions:
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

    def get_neighbors_8way(self, pos, exist=False):
        """Returns an array of neighbors.
        If the array is bounded, only in-bounds neighbors
        If exist is True, only pre-existing neighbors"""
        ans = []
        for d in self.eight_way_directions:
            nx = pos[0] + d[0]
            ny = pos[1] + d[1]
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

    def flood_neighbors(self, pos, wall, visited):
        """Returns a neighbors list pruned by visited and wall"""
        neighbors = self.get_neighbors_4way(pos, exist=True)
        ans = []
        for p in neighbors:
            # Prune for visited
            if p not in visited:
                # Prune for wall (if applicable)
                if wall is not None:
                    if self.get_value_from_pos_object(p) != wall:
                        ans.append(p)
        return ans

    def flood(self, start_pos, wall=None):
        """Floods outwards from the starting position
        Does not pass through tiles equaling 'wall'
        Returns a list of positions."""
        visited = []
        q = Queue()

        visited.append(start_pos)
        q.put(start_pos)

        while not q.empty():
            s = q.get()
            s_neighbors = self.flood_neighbors(s, wall, visited)
            for neighbor in s_neighbors:
                if neighbor not in visited:
                    visited.append(neighbor)
                    q.put(neighbor)

        return visited
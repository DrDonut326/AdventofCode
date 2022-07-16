class Pos:
    """A 2d or 3d data class for use with grids"""
    four_way_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    eight_way_directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

    def __init__(self, x, y, z=0, **kwargs):
        self.x = x
        self.y = y
        self.z = z
        self.__dict__.update(kwargs)


    def __repr__(self):
        return f"({self.x},{self.y})"

    def hash_key(self):
        return (self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.hash_key())

    def get_name(self):
        """Return a string version of current position"""
        return self.__repr__()

    def get_neighbors_4way(self):
        """Returns neighboring positions for adjacent directions only."""
        # Get all possible new directions
        pos_list = []
        for d in self.four_way_directions:
            nx = self.x + d[0]
            ny = self.y + d[1]
            pos_list.append(Pos(nx, ny))

        return pos_list

    def get_neighbors_8way(self):
        """Returns neighboring positions for adjacent and diagonal neighbors."""
        # Get all possible new directions
        pos_list = []
        for d in self.eight_way_directions:
            nx = self.x + d[0]
            ny = self.y + d[1]
            pos_list.append(Pos(nx, ny))
        return pos_list


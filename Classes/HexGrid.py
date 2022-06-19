# TODO: Add a data=None to the hex?


# Used this website
# https://www.redblobgames.com/grids/hexagons/

class HexPos:
    """Stores hex position in the form of q, r, s.
    Can get neighboring position with a compass method."""
    def __init__(self, q, r, s):
        self.q = q
        self.r = r
        self.s = s

        # Confirm that they sum to zero
        assert sum([q, r, s]) == 0

    def __repr__(self):
        return self.get_key()

    def get_max(self):
        return max([self.q, self.r, self.s])

    def get_key(self):
        """Returns a key used for hashing."""
        return f"{self.q}|{self.r}|{self.s}"

    def get_neighbor_from_string(self, requested_string):
        directions = {
            'n': self.north,
            'ne': self.northeast,
            'se': self.southeast,
            's': self.south,
            'sw': self.southwest,
            'nw': self.northwest
        }
        return directions[requested_string]()

    # Return New positions based on compass directions
    def north(self):
        return HexPos(self.q, self.r - 1, self.s + 1)

    def northeast(self):
        return HexPos(self.q + 1, self.r -1, self.s)

    def southeast(self):
        return HexPos(self.q + 1, self.r, self.s - 1)

    def south(self):
        return HexPos(self.q, self.r + 1, self.s - 1)

    def southwest(self):
        return HexPos(self.q - 1, self.r + 1, self.s)

    def northwest(self):
        return HexPos(self.q - 1, self.r, self.s + 1)


class HexGrid:
    """Simple Grid that doesn't store any data in nodes."""
    def __init__(self):
        self.grid = dict()

    def add_hex_from_qrs(self, q, r, s):
        """Adds the position to the grid and returns it"""
        pos = HexPos(q, r, s)
        self.add_hex(pos)
        return pos

    def add_hex(self, pos):
        self.grid[pos.get_key()] = pos






# TODO: Build a hex grid class

# TODO: Store positions as q, r, s

# TODO: q + r + s must always equal 0
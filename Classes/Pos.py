class Pos:
    """A 2d or 3d data class for use with grids"""
    def __init__(self, x, y, z=0, **kwargs):
        self.x = x
        self.y = y
        self.z = z
        self.__dict__.update(kwargs)

    def __repr__(self):
        return f"X:{self.x} Y:{self.y}"

    def hash_key(self):
        return f"H:{self.x}/{self.y}"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.hash_key())

    def get_name(self):
        """Return a string version of current position"""
        return self.__repr__()

class Pos:
    """A 2d or 3d data class for use with grids"""
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"{self.x} // {self.y}"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(self.__repr__())

    def get_name(self):
        """Return a string version of current position"""
        return f"{self.x}X | {self.y}Y"

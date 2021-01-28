class Pos:
    """A 2d or 3d data class for use with grids"""
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

    def get_name(self):
        """Return a string version of current position"""
        return f"{self.x}X | {self.y}Y"

from collections import defaultdict


class Spiral:
    def __init__(self, x, y, value):
        self.pos = Pos(x, y)
        self.value = value

    def get_key(self):
        return f"({self.pos.x},{self.pos.y})"


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x},{self.y})"

    def get_key(self):
        return f"({self.x},{self.y})"


def spiral_gen():
    """Yields the position and value of the next spiral."""
    x = 0
    y = 0
    steps = 1
    count = 1

    # First call, give the origin
    yield Spiral(x, y, count)

    while True:
        # Right
        for _ in range(steps):
            x += 1
            count += 1
            yield Spiral(x, y, count)

        # Up
        for _ in range(steps):
            y -= 1
            count += 1
            yield Spiral(x, y, count)

        # Add 1 to steps
        steps += 1

        # Left
        for _ in range(steps):
            x -= 1
            count += 1
            yield Spiral(x, y, count)

        # Down
        for _ in range(steps):
            y += 1
            count += 1
            yield Spiral(x, y, count)

        # Add 1 to steps
        steps += 1


def get_manhat_dist(pos_a, pos_b):
    return abs(pos_a.x - pos_b.x) + abs(pos_a.y - pos_b.y)


def get_neighbors_8way(pos):
    ans = []
    d = [-1, 0 , 1]

    for dx in d:
        for dy in d:
            new_x = pos.x + dx
            new_y = pos.y + dy
            if new_x != pos.x or new_y != pos.y:
                ans.append(Pos(new_x, new_y))

    return ans

def override_value(spiral, visited):
    """Overwrites the value of the spiral based on the sum of neighbors at that position"""
    pos = spiral.pos

    # Get all neighbors of pos
    neighbors = get_neighbors_8way(pos)

    # Sum up all the existing nodes in visited
    count = 0
    for n in neighbors:
        if n.get_key() in visited:
            count += visited[n.get_key()]

    # Set new value
    spiral.value = count


def main():
    spiral = spiral_gen()

    origin = next(spiral)

    magic = 312051

    # Find the magic number
    outside = next(spiral)
    while outside.value != magic:
        outside = next(spiral)

    print(get_manhat_dist(origin.pos, outside.pos))  # Part 1 answer

    # -------- Part 2 -----------
    spiral = spiral_gen()
    origin = next(spiral)

    # Keep a dict of all positions visited so far
    visited = defaultdict(int)
    visited[origin.get_key()] = origin.value


    # Find the magic number
    outside = next(spiral)
    override_value(outside, visited)
    visited[outside.get_key()] = outside.value

    while outside.value <= magic:
        outside = next(spiral)
        override_value(outside, visited)
        visited[outside.get_key()] = outside.value

    print(outside.value)




main()

from Grids import DictGrid
from Pos import Pos


class Follower:
    def __init__(self, pos, grid: DictGrid, direction=(0, 1)):
        self.pos = pos
        self.direction = direction
        self.letters_found = []
        self.visited = {pos}
        self.grid = grid
        self.steps = 0


    def find_way(self):
        """Keeps following the path until it runs out of places to go"""
        done = False
        while not done:
            # Look down and record what you see
            see = self.look_down()

            # Record letter and keep going
            if see.isalpha():
                self.letters_found.append(see)
                # If there are no more unvisited neighbors, end
                self.keep_going()

            # If you're on a +, change direction then keep going
            elif see == '+':
                self.change_direction()
                self.keep_going()

            # If on a line, keep going in direction
            elif see == '|' or see == '-':
                self.keep_going()

            else:
                done = True

        # Return letters seen
        return ''.join(self.letters_found)


    def get_neighbors(self):
        return [x for x in self.grid.get_neighbors_4way(self.pos, exist=True) if x not in self.visited]

    def look_down(self) -> str:
        see = self.grid.get_value_from_pos_object(self.pos)
        return see

    def change_direction(self):

        # Get neighbors that haven't been visited yet
        neighbors = self.get_neighbors()

        x, y = self.pos.x, self.pos.y

        # There should only be one possible way to go?
        assert len(neighbors) == 1

        neighbor = neighbors[0]
        nx, ny = neighbor.x, neighbor.y

        # Test North
        if ny < y:
            self.direction = (0, -1)

        elif ny > y:
            self.direction = (0, 1)

        elif nx < x:
            self.direction = (-1, 0)

        elif nx > x:
            self.direction = (1, 0)

        else:
            raise EnvironmentError(f"Strange directions with Pos={self.pos} // neighbors={neighbors}")

    def keep_going(self):
        """Continues in the current direction."""
        x, y = self.pos.x, self.pos.y
        dx, dy = self.direction

        x += dx
        y += dy

        self.pos = Pos(x, y)
        # Add to visited
        self.visited.add(self.pos)
        self.steps += 1


def get_input():
    ans = []
    with open("input.txt") as f:
        for line in f:
            line = line.rstrip()
            row = []
            for c in line:
                row.append(c)
            ans.append(row)
    return ans


def make_grid(grid: DictGrid, diagram):
    for y, row in enumerate(diagram):
        for x, element in enumerate(row):
            if element != ' ':
                p = Pos(x, y)
                grid.add_data_to_grid_at_pos(element, p)


def get_grid(diagram):
    grid = DictGrid(str, bounded=False)
    make_grid(grid, diagram)
    return grid


def main():
    diagram = get_input()
    start_pos = Pos(diagram[0].index('|'), 0)
    grid = get_grid(diagram)

    f = Follower(start_pos, grid)
    part_1 = f.find_way()
    print(part_1)
    print(f.steps)


main()

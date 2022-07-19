from Classes.Grids import DictGrid
from Utility.Pathfinding import bfs_dictgrid, display_cost_grid

# (  = Create a new crawler and send it off.  Return finish coords and type
# |  = Send finish coords such that the original makes a NEW clone from that point
# )  = Send finish coords that causes the parent to jump to this point


class Crawler:
    def __init__(self, pos, instructions, i, grid: DictGrid):
        self.pos = pos
        self.instructions = instructions
        self.i = i
        self.grid = grid

    def crawl(self):
        instru_len = len(self.instructions)
        while self.i < instru_len:
            # What instruction do you see
            see = self.instructions[self.i]

            # If the start or the finish, walk past
            if see == '^' or see == '$':
                self.i += 1

            # If a cardinal direction, move there and increment i
            elif see == 'N':
                self.go(self.north())
                self.grid.grid[self.pos] = '-'
                self.go(self.north())
                self.grid.grid[self.pos] = '.'
                self.i += 1

            elif see == 'S':
                self.go(self.south())
                self.grid.grid[self.pos] = '-'
                self.go(self.south())
                self.grid.grid[self.pos] = '.'
                self.i += 1

            elif see == 'E':
                self.go(self.east())
                self.grid.grid[self.pos] = '|'
                self.go(self.east())
                self.grid.grid[self.pos] = '.'
                self.i += 1

            elif see == 'W':
                self.go(self.west())
                self.grid.grid[self.pos] = '|'
                self.go(self.west())
                self.grid.grid[self.pos] = '.'
                self.i += 1

            # Open paren: Create a new crawler and get it's result
            elif see == '(':
                new_c = Crawler(self.pos, self.instructions, self.i + 1, self.grid)
                result, new_i = new_c.crawl()
                while result == 'CLONE':
                    new_c = Crawler(self.pos, self.instructions, new_i, self.grid)
                    result, new_i = new_c.crawl()
                if result == 'JUMP':
                    self.i = new_i


            # Pipe: Return i + 1 and a clone command so the parent makes another clone
            elif see == '|':
                return 'CLONE', self.i + 1

            elif see == ')':
                return 'JUMP', self.i + 1


    def go(self, pos):
        self.pos = pos

    def north(self, pos=None):
        if pos is None:
            pos = self.pos
        return pos[0], pos[1] - 1

    def south(self, pos=None):
        if pos is None:
            pos = self.pos
        return pos[0], pos[1] + 1

    def east(self, pos=None):
        if pos is None:
            pos = self.pos
        return pos[0] + 1, pos[1]

    def west(self, pos=None):
        if pos is None:
            pos = self.pos
        return pos[0] - 1, pos[1]


def get_input():
    ans = None
    with open('input.txt') as f:
        for line in f:
            line = line.rstrip()
            ans = line
    return ans



def main():
    grid = DictGrid(str)
    start_pos = (0, 0)
    grid.add_data_to_grid_at_pos(start_pos, 'X')
    sample = get_input()
    crawler = Crawler(start_pos, sample, 0, grid)
    crawler.crawl()
    b = bfs_dictgrid(grid, start_pos)
    # Get max cost in grid
    part_1 = max(b.values()) // 2
    print(part_1)

    part_2_count = 0
    for key in b:
        if b[key] / 2 >= 1000:
            part_2_count += 1

    print(part_2_count // 2 + 1)

main()

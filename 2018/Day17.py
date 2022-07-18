def make_grid():
    grid = []

    # Store any clay you find for later
    clay = set()

    with open('input.txt') as f:

        min_x = None
        max_x = None
        min_y = 0  #Spring y will also be 0
        max_y = None

        # Build up individual clay locations and store them as (x, y)
        for line in f:
            line = line.rstrip()

            # X First
            if line[0] == 'x':
                left, right = line.split(', ')

                # Check for min / max in the meantime
                x = int(left[2:])
                if min_x is None or x < min_x:
                    min_x = x
                if max_x is None or x > max_x:
                    max_x = x

                start_y, fin_y = [int(z) for z in right[2:].split('..')]
                for y in range(start_y, fin_y + 1):

                    if max_y is None or y > max_y:
                        max_y = y

                    pos = (x, y)
                    clay.add(pos)

            # Y First
            elif line[0] == 'y':
                left, right = line.split(', ')

                y = int(left[2:])

                if max_y is None or y > max_y:
                    max_y = y

                start_x, fin_x = [int(z) for z in right[2:].split('..')]
                for x in range(start_x, fin_x + 1):

                    if min_x is None or x < min_x:
                        min_x = x
                    if max_x is None or x > max_x:
                        max_x = x

                    pos = (x, y)
                    clay.add(pos)

    # Build up a full 2d array
    for y in range(min_y, max_y + 1):
        row = []
        for x in range(min_x, max_x + 1):
            pos = (x, y)
            if pos == (500, 0):
                row.append('+')
            elif pos in clay:
                row.append('#')
            else:
                row.append('.')
        grid.append(row)

    return grid


class Drop:
    solids = ['#', '~']  # Water can 'land' on these and flow
    stop_symbols = {'<', '>', 'v', '%'}  # Can merge with these
    move_symbols = {'.', '<', '>', 'v', '%'} # Can move through these

    def __init__(self, x: int, y: int, grid: list):
        self.x = x
        self.y = y
        self.grid = grid

    def flow(self):
        """Flow until you go OOB or merge with an existing stream"""

        while True:
            # Global timer for debugging
            global iter_count
            iter_count += 1

            # Check if left / right OOB
            if self.x < 0 or self.x >= len(self.grid[self.y]):
                return 'OOB'

            # Check if down OOB
            if self.y >= len(self.grid):
                return 'OOB'

            # Check if OOB is below and mark current as flowing and then move
            if self.y+1 >= len(self.grid):
                self.grid[self.y][self.x] = 'v'
                return 'OOB'

            # If nothing below, fall down
            if self.grid[self.y+1][self.x] == '.':
                # Mark current grid square as flowing down
                self.grid[self.y][self.x] = 'v'
                self.y += 1

            # If current is empty but a flow symbol below
            # Mark current as down and then return (don't retrace)
            elif self.grid[self.y][self.x] in self.move_symbols and self.grid[self.y+1][self.x] in self.stop_symbols:
                self.grid[self.y][self.x] = 'v'
                return 'MERGED'

            # If a solid is below:
            elif self.grid[self.y+1][self.x] in self.solids:
                # Determine the left and right end types
                left, right = self.find_ends()

                # If there are walls on both sides, fill that row
                if left[1] == 'closed' and right[1] == 'closed':
                    self.fill_with_resting_water(left, right)
                    # Move to one above
                    self.y -= 1

                # If open on both sides, flowing water and split
                elif left[1] == 'open' and right[1] == 'open':
                    self.fill_with_flowing_and_split(left, right, (self.x, self.y))
                    # Make a new drop and move it to the right exit
                    d = Drop(right[0][0], right[0][1], self.grid)
                    d.flow()

                    # Move current drop to the left exit
                    self.x = left[0][0]
                    self.y = right[0][1]

                # If open on one side, create flowing water in that direction
                elif left[1] == 'open':
                    self.fill_with_flowing_water(left, right, 'left')
                    # Move to the exit
                    self.x = left[0][0]

                elif right[1] == 'open':
                    self.fill_with_flowing_water(left, right, 'right')
                    # Move to the exit
                    self.x = right[0][0]

    def is_in_bounds(self, pos, direction):
        x, y = pos
        if direction == 'right':
            return x + 1 < len(self.grid[y])

        if direction == 'left':
            return x - 1 >= 0

        if direction == 'down':
            return y + 1 >= len(self.grid)

        if direction == 'up':
            return y - 1 >= 0

    def get_side(self, side):
        if side == 'right':
            dx = 1
        elif side == 'left':
            dx = -1
        else:
            raise EnvironmentError('bad direction given')

        # ----Search
        search_pos = (self.x, self.y)

        # If there is a wall directly to the side, then return this position
        if self.grid[self.y][self.x + dx] == '#':
            right = (search_pos, 'closed')
        else:
            right = self.traverse_right(search_pos, dx)

        return right

    def traverse_right(self, start_pos, dx):
        x, y = start_pos
        while True:
            # Move right1
            x += dx
            pos = (x, y)

            # Look down (open)
            if self.grid[y+1][x] not in self.solids:
                return pos, 'open'

            # If you look OB, return it as the exit with 'open'
            if x+dx < 0 or x+dx >= len(self.grid[y]):
                return (x+dx, y), 'open'

            # Look right
            if self.grid[y][x+dx] == '#':
                return pos, 'closed'

    def find_ends(self):
        right = self.get_side('right')
        left = self.get_side('left')
        return left, right

    def fill_with_resting_water(self, left, right):
        left_pos = left[0]
        right_pos = right[0]
        y = left_pos[1]
        for x in range(left_pos[0], right_pos[0] + 1):
            assert x >= 0 # Should be impossible as clay should be in bounds
            self.grid[y][x] = '~'

    def fill_with_flowing_water(self, left, right, direction):
        left_pos = left[0]
        right_pos = right[0]
        y = left_pos[1]
        for x in range(left_pos[0], right_pos[0] + 1):
            # Ignore if 0 is OOB
            if x < 0 or x >= len(self.grid[y]):
                pass
            else:
                if direction == 'right':
                    self.grid[y][x] = '>'
                elif direction == 'left':
                    self.grid[y][x] = '<'
                else:
                    raise EnvironmentError('Bad direction for flowing water')

    def fill_with_flowing_and_split(self, left, right, middle):
        left_pos = left[0]
        right_pos = right[0]
        y = left_pos[1]

        # Fill left side to center - 1
        for x in range(left_pos[0], middle[0]):  # One left of middle
            if x < 0 or x >= len(self.grid[y]):
                global oob_list
                oob_list.append((x, y))
            else:
                self.grid[y][x] = '<'

        # Fill middle with split sign
        self.grid[y][middle[0]] = '%'

        # Fill right side
        for x in range(middle[0] + 1, right_pos[0] + 1):  # Start 1 right of middle
            if x < 0 or x >= len(self.grid[y]):
                pass
            else:
                self.grid[y][x] = '>'


def display_grid(grid):
    for row in grid:
        for element in row:
            print(element, end='')
        print()


def count_water_path(grid, oob):  # Part 1
    count = 0
    water = {'<', '>', 'v', '%', '~'}
    for row in grid:
        for element in row:
            if element in water:
                count += 1

    # Handle water that went OOB
    left_list = [z for z in oob if z[0] < 0]
    right_list = [z for z in oob if z[0] > 0]

    left_high = None
    right_high = None

    # For each list find the highest place it went OOB
    if left_list:
        left_high = min(left_list, key=lambda x: x[1])[1]
    if right_list:
        right_high = min(right_list, key=lambda x: x[1])[1]

    # Get the difference between the grid high and each high
    if left_high is not None:
        left_difference = (len(grid) - 2) - left_high
        # Add to count
        count += left_difference

    if right_high is not None:
        right_difference = (len(grid) - 2) - right_high
        count += right_difference
    return count


def count_only_resting(grid):  # Part 2
    count = 0
    for row in grid:
        for element in row:
            if element == '~':
                count += 1
    return count


def find_spring_x(grid):
    # Should be in the first row
    for x, element in enumerate(grid[0]):
        if element == '+':
            return x

def main():
    grid = make_grid()
    spring_x = find_spring_x(grid)
    drops = []
    drops.append(Drop(spring_x, 1, grid))


    for d in drops:
        # All drops flow to OOB
        result = d.flow()
        if result == 'OOB':
            oob_list.append((d.x, d.y))


    display_grid(grid)
    print(count_water_path(grid, oob_list))     # Part 1 answer
    print(count_only_resting(grid))             # Part 2 answer


oob_list = []
iter_count = 0
main()

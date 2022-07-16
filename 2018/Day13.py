from Functions import Pos
from os import system


class Minecart:
    def __init__(self, pos, dir_symbol, grid):
        self.pos = pos
        self.dir_symbol = dir_symbol
        self.next_turn = 'left'
        self.turn_gen = turn_gen()
        self.direction = get_symbol_to_direction(self.dir_symbol)
        self.dxyx = get_dir_to_dx_dy(self.direction)
        self.grid_reference = grid

    def __repr__(self):
        return f"{self.pos}, {self.dir_symbol}"

    def update(self):
        # Move forward in your current direction
        new_pos = Pos(self.pos.x + self.dxyx[0], self.pos.y + self.dxyx[1])
        self.pos = new_pos

        # Check the current track
        x, y = self.pos.x, self.pos.y
        track = self.grid_reference[y][x]

        # If on a curved track, change direction
        if track in curved_tracks:
            # -- Update direction symbol // Direction word // dxyx
            self.dir_symbol = get_curved_track_direction(self.dir_symbol, track)
            self.direction = get_symbol_to_direction(self.dir_symbol)
            self.dxyx = get_dir_to_dx_dy(self.direction)

        # If on an intersection, change direction
        elif track == '+':
            self.dir_symbol = get_direction_at_intersection(self.dir_symbol, self.next_turn)
            # Update the next turn
            self.next_turn = next(self.turn_gen)
            # Update related
            self.direction = get_symbol_to_direction(self.dir_symbol)
            self.dxyx = get_dir_to_dx_dy(self.direction)


def turn_gen():
    # Carts themselves start left, so the next direction should be straight
    current = 'straight'
    yield current
    while True:
        if current == 'left':
            current = 'straight'
        elif current == 'straight':
            current = 'right'
        elif current == 'right':
            current = 'left'
        else:
            raise EnvironmentError("Bad direction for minecart turn.")
        yield current


def get_dir_to_dx_dy(direction):
    return direction_to_dx_yx[direction]


def get_symbol_to_direction(symbol):
    return symbol_to_direction[symbol]


def get_symbol_to_track(symbol):
    return symbol_to_track_dict[symbol]


def get_grid_and_carts():
    # Make grid first
    grid = []
    carts = dict()
    y = 0
    with open('input.txt') as f:
        for line in f:
            x = 0
            row = []
            line = line.rstrip()
            #
            for s in line:
                if s in symbol_to_track_dict:
                    # Put track under cart
                    row.append(get_symbol_to_track(s))

                    # Make minecart
                    pos = Pos(x, y)
                    cart = Minecart(pos, s, grid)
                    carts[pos] = cart
                else:
                    row.append(s)

                x += 1
            grid.append(row)
            y += 1
    return grid, carts


def get_curved_track_direction(symbol, track):
    assert track in curved_tracks
    # Going left
    if symbol == '<':
        if track == '/':
            return 'v'
        else:
            return '^'

    if symbol == '^':
        if track == '/':
            return '>'
        else:
            return '<'

    if symbol == '>':
        if track == '\\':
            return 'v'
        else:
            return '^'

    if symbol == 'v':
        if track == '\\':
            return '>'
        else:
            return '<'


def display_tracks_only(grid):
    for row in grid:
        for element in row:
            print(element, end='')
        print()


def display_all(grid: list, carts: dict):
    system('cls')
    for y, row in enumerate(grid):
        for x, element in enumerate(row):
            pos = Pos(x, y)
            if pos in carts:
                cart: Minecart
                cart = carts[pos]
                print(cart.dir_symbol, end='')
            else:
                print(grid[y][x], end='')
        print()


def get_direction_at_intersection(dir_symbol, turn):
    if dir_symbol == '^':
        if turn == 'left':
            return '<'
        if turn == 'straight':
            return '^'
        if turn == 'right':
            return '>'

    if dir_symbol == '<':
        if turn == 'left':
            return 'v'
        if turn == 'straight':
            return '<'
        if turn == 'right':
            return '^'

    if dir_symbol == 'v':
        if turn == 'left':
            return '>'
        if turn == 'straight':
            return 'v'
        if turn == 'right':
            return '<'

    if dir_symbol == '>':
        if turn == 'left':
            return '^'
        if turn == 'straight':
            return '>'
        if turn == 'right':
            return 'v'

    raise EnvironmentError('Bad Symbol for turning.')


def update_carts(carts_dict, part):
    # Get carts and sort them by top down left to right
    carts = [c for c in carts_dict.values()]
    carts.sort(key=lambda x: [x.pos.y, x.pos.x])

    # Update each card
    for cart in carts:
        # Get the previous position
        previous_pos = Pos(cart.pos.x, cart.pos.y)

        # Update the cart
        cart.update()

        # Get the new position
        new_pos = cart.pos

        # If there is another cart with this position, then a collision has happened
        if new_pos in carts_dict:
            # ---- Colliision logic
            # If doing part 1, return this position
            if part == 1:
                return new_pos
            else:
                # Remove both carts (so delete this position from carts dict and previous)
                del carts_dict[new_pos]
                del carts_dict[previous_pos]


        # If not delete the old position in the dictionary and put in the new updated cart
        else:
            if previous_pos in carts_dict:
                del carts_dict[previous_pos]
                carts_dict[new_pos] = cart

    # Check if only one cart remaining
    if len(carts_dict.values()) == 1:
        # Get last card
        last_cart_list = list(carts_dict.values())
        return last_cart_list[0].pos


def part_1():
    grid, carts = get_grid_and_carts()

    while True:
        result = update_carts(carts, 1)
        if result is not None:
            return f"Collision dected at {result}"


def part_2():
    grid, carts = get_grid_and_carts()

    while True:
        result = update_carts(carts, 2)
        if result is not None:
            return f"Last collision at {result}"


def main():
    # **** Be sure to iterate carts in order from the top! *****
    print(part_1())
    print(part_2())



curved_tracks = ['/', '\\']
direction_to_dx_yx = dict(North=(0, -1), South=(0, 1), East=(1, 0), West=(-1, 0))
symbol_to_direction = {'<': 'West', '^': 'North', '>': 'East', 'v': 'South'}
symbol_to_track_dict = {'<': '-', '^': '|', '>': '-', 'v': '|'}


main()

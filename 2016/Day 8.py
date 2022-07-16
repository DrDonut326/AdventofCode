from collections import deque

from Functions import get_input


def make_grid(width, height):
    ans = []
    for y in range(height):
        row = [' '] * width
        ans.append(row)
    return ans


def print_grid(g):
    for row in g:
        print(row)


def rotate_row(grid, row_number, v):
    """Rotates the given row v-times"""
    d = deque(grid[row_number])
    d.rotate(v)
    grid[row_number] = list(d)


def make_column(grid, col_number):
    ans = []
    for col in grid:
        ans.append(col[col_number])
    return ans


def place_column(grid, col, col_number):
    for i, x in enumerate(col):
        grid[i][col_number] = x


def rotate_col(grid, col_number, v):
    """Rotates the given column v-times"""
    col = make_column(grid, col_number)
    d = deque(col)
    d.rotate(v)
    place_column(grid, list(d), col_number)


def make_rect(grid, x_size, y_size):
    for y in range(y_size):
        for x in range(x_size):
            grid[y][x] = '#'


def main():
    grid = make_grid(50, 6)
    codes = get_input('line')
    for code in codes:
        if 'rect' in code:
            left, right = code.split(' ')
            x, y = right.split('x')
            make_rect(grid, int(x), int(y))
        elif 'rotate row' in code:
            code = code[11:]
            left, by, v = code.split(' ')
            trash, y = left.split('=')
            y = int(y)
            v = int(v)
            rotate_row(grid, y, v)
        else:
            code = code[14:]
            left, by, v = code.split(' ')
            trash, x = left.split('=')
            x = int(x)
            v = int(v)
            rotate_col(grid, x, v)
    count = 0
    for row in grid:
        for x in row:
            if x == '#':
                count += 1
    print(f"Part 1 answer = {count}")
    print_grid(grid)


if __name__ == '__main__':
    main()

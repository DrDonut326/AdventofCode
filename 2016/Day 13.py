from collections import defaultdict
from copy import deepcopy
from queue import PriorityQueue


def get_cubicle_state(x, y):
    fav_number = 1350
    """Returns the maze representation at the given coord"""
    r = (x*x) + (3*x) + (2*x*y) + y + (y*y)
    r += fav_number
    r = bin(r)
    count = r.count('1')
    if count % 2 == 0:
        return '.'
    return '#'


def build_grid(grid, grid_size):
    for y in range(grid_size):
        for x in range(grid_size):
            cubicle = get_cubicle_state(x, y)
            grid[(x, y)] = cubicle


def get_neighbors_4way(grid, grid_size, x, y):
    """Returns an array of neighbors.
    If the array is bounded, only in-bounds neighbors
    If exist is True, only pre-existing neighbors"""
    ans = []
    pos = (x, y)
    four_way_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for d in four_way_directions:
        nx = pos[0] + d[0]
        ny = pos[1] + d[1]
        ans.append((nx, ny))

    # Clean answers: Step 1.  If the grid is bounded, trip OOB
    cleaned_ans = []
    for p in ans:
        if 0 <= p[0] < grid_size[0] and 0 <= p[1] < grid_size[1]:
            cleaned_ans.append(p)
    ans = cleaned_ans

    # Clean answers: Step 2. If the position is not already existing in the array, dump it
    cleaned_ans = []
    for pos in ans:
        if pos in grid:
            cleaned_ans.append(pos)
    ans = cleaned_ans
    return ans


def draw_grid(grid, grid_size):
    for y in range(grid_size):
        row = ''
        for x in range(grid_size):
            row += grid[(x, y)]
        print(row)

def is_we_done(pos_a, end_pos):
    if pos_a[0] == end_pos[0] and pos_a[1] == end_pos[1]:
        return True
    return False


def get_valid_moves(grid, all_moves):
    ans = []
    for pos in all_moves:
        if grid[pos] == '.':
            ans.append(pos)
    return ans


def bfs(grid, start_pos, end_pos, grid_size, part):
    visited = set()
    q = PriorityQueue()
    visited.add((start_pos, start_pos))
    q.put((0, [start_pos]))

    while not q.empty():
        steps, path = q.get()
        pos = path[-1]

        # Check if finished
        if is_we_done(pos, end_pos):
            return steps, path

        # get NEIGHBORS
        all_moves = get_neighbors_4way(grid, grid_size, pos[0], pos[1])

        # Prune moves that are not valid states
        valid_moves = get_valid_moves(grid, all_moves)

        for pos in valid_moves:
            if pos not in visited:
                path_copy = deepcopy(path)
                path_copy.append(pos)
                if part == 'part2':
                    if steps + 1 <= 49:
                        q.put((steps + 1, path_copy))
                        visited.add(pos)
                else:
                    q.put((steps + 1, path_copy))
                    visited.add(pos)

    if part == 'part2':
        return visited
    else:
        return (f"No answer found!")


def main():
    grid_size = 40
    grid = defaultdict()
    build_grid(grid, grid_size)
    result = bfs(grid, (1, 1), (31, 39), (grid_size, grid_size), 'part1')
    brain = {}


    while result == 'No answer found!':
        grid_size += 1
        grid = defaultdict()
        build_grid(grid, grid_size)
        result = bfs(grid, (1, 1), (31, 39), (grid_size, grid_size), 'part1')

    steps, path = result

    print(f"Part 1 answer = {steps}")
    grid_size = 60
    grid = defaultdict()
    build_grid(grid, grid_size) #ayylmao
    visited = bfs(grid, (1, 1), (69, 69), (grid_size, grid_size), 'part2')
    print(f"Part 2 answer = {len(visited)}")

if __name__ == '__main__':
    main()
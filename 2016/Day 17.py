from queue import PriorityQueue
from hashlib import md5
from copy import deepcopy


def get_bytes(s):
    """Convert a string into bytes for hash input"""
    return bytes(s, 'utf-8')


def get_hash(steps, pos, path):
    ans = [steps]
    x, y = pos
    ans.append(x)
    ans.append(y)
    p = tuple(path)
    ans.append(p)
    ans = tuple(ans)
    ans = hash(ans)
    return ans


def is_visited_already(visited, steps, pos, path):
    h = get_hash(steps, pos, path)
    return h in visited


def add_to_visited(visited, steps, pos, path):
    h = get_hash(steps, pos, path)
    visited.add(h)


def get_door_hash(salt, path):
    """Generate hashes based on the input salt"""
    s = salt
    for p in path:
        s += p
    m = md5(get_bytes(s)).hexdigest()

    return m[0:4]


def get_door_states(puzzle_input, path):
    ans = []
    door_hash = get_door_hash(puzzle_input, path)
    doors = ['U', 'D', 'L', 'R']
    for h, door in zip(door_hash, doors):
        if h in ['b', 'c', 'd', 'e', 'f']:
            ans.append(door)
    return ans


def get_new_pos(direction, pos):
    four_way_directions = {'L': (-1, 0), 'R': (1, 0), 'U': (0, -1), 'D': (0, 1)}
    x, y = pos
    dx, dy = four_way_directions[direction]
    nx = x + dx
    ny = y + dy
    return nx, ny


def prune_doors(open_doors, pos):
    ans = []
    for d in open_doors:
        nx, ny = get_new_pos(d, pos)
        if 0 <= nx < 4 and 0 <= ny < 4:
            ans.append(d)
    return ans


def get_moves(pos, path, puzzle_input):
    # Get all moves
    open_doors = get_door_states(puzzle_input, path)
    # Prune ones that lead out of the prison
    pruned_moves = prune_doors(open_doors, pos)
    return pruned_moves


def bfs(puzzle_input, part):
    visited = set()
    q = PriorityQueue()
    pos = (0, 0)
    path = []
    steps = 0
    add_to_visited(visited, steps, pos, path)
    q.put((steps, pos, path))
    # Part 2
    longest = 0

    while not q.empty():
        steps, pos, path = q.get()

        # Check if finished
        if part == 'part1':
            if pos[0] == 3 and pos[1] == 3:
                return steps, pos, path
        elif pos[0] == 3 and pos[1] == 3:
            if steps > longest:
                longest = steps

        # Get neighbors
        moves = get_moves(pos, path, puzzle_input)

        if pos[0] != 3 or pos[1] != 3:
            for move in moves:
                nx, ny = get_new_pos(move, pos)
                if not is_visited_already(visited,steps, (nx, ny), path):
                    path_copy = deepcopy(path)
                    path_copy.append(move)
                    new_steps = steps + 1
                    q.put((new_steps, (nx, ny), path_copy))
                    add_to_visited(visited, new_steps, (nx, ny), path_copy)

    return longest, pos, path


def main():
    puzzle_input = 'bwnlcvfs'
    steps, pos, path = bfs(puzzle_input, 'part1')
    print(f"Part 1 answer = {''.join(path)}")
    steps, pos, path = bfs(puzzle_input, 'part2')
    print(f"Part 2 answer = {steps}")


if __name__ == '__main__':
    main()

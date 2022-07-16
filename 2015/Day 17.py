from Functions import get_input
from collections import deque


def build_solutions(ans, path, containers):
    # If the current path matches the solution length, add it to the answer dict
    if sum(path) == 150:
        ans.append(path)
        return
    # Current path is too long, so abandon it
    if sum(path) > 150:
        return
    # Need to explore more, so create offshoot using the remaining containers
    while len(containers) > 0:
        # Pop off the container
        n = containers.popleft()
        # Make a copy of the path
        t = path.copy()
        # Append the container to the path copy
        t.append(n)
        # Copy the containers
        tc = containers.copy()
        # Only care about things in ans, so don't need to worry about returning
        build_solutions(ans, t, tc)
    return ans



def main():
    cont = [int(x) for x in get_input('line')]
    containers = deque()
    for c in cont:
        containers.append(c)
    ans = build_solutions([], [], containers)
    print(f"Part 1 answer = {len(ans)}")

    # Part 2
    smallest = len(min(ans, key=len))
    count = 0
    for a in ans:
        if len(a) == smallest:
            count += 1
    print(f"Part 2 answer = {count}")




main()

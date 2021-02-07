from Utility import get_input
from collections import deque

def get_triangles():
    ans = []
    triangles = get_input('line')
    for line in triangles:
        line = line[1:]
        line = [int(x) for x in line.split()]
        a, b, c = line
        ans.append((a, b, c))
    return ans


def is_triangle_valid(triangle):
    """Returns if a triangle tuple is valid or not"""
    a, b, c = triangle
    return a + b > c and a + c > b and b + c > a


def part1(triangles):
    count = 0
    for triangle in triangles:
        if is_triangle_valid(triangle):
            count += 1
    return count


def part2(triangles):
    count = 0
    queue = deque(triangles)
    assert len(queue) % 3 == 0
    while len(queue) > 0:
        tris = []
        for _ in range(3):
            tris.append(queue.popleft())
        a,b,c = tris
        new_triangles = []
        for i in range(3):
            new_triangles.append((a[i], b[i], c[i]))
        for t in new_triangles:
            if is_triangle_valid(t):
                count += 1
    return count

def main():
    triangles = get_triangles()
    print(f"Part 1 = {part1(triangles)}")
    print(f"Part 2 = {part2(triangles)}")


if __name__ == '__main__':
    main()

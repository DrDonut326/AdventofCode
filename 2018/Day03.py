from Pos import Pos
from itertools import combinations
from collections import defaultdict


class Rect:
    def __init__(self, id_num, pos, width, height):
        self.id_num = id_num
        self.pos = pos
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def __hash__(self):
        return hash(self.pos.x * self.pos.y * self.height * self.height)

    def add_squares_to_dict(self, d):
        for y in range(self.pos.y, self.pos.y + self.height):
            for x in range(self.pos.x, self.pos.x + self.width):
                pos = Pos(x, y)
                d[pos] += 1


def get_input():
    claims = []
    with open("input.txt") as f:
        for line in f:
            line = line.rstrip()

            # Remove #
            line = line[1:]

            # Remove @
            line = line.replace(' @ ', ' ')

            # Remove :
            line = line.replace(':', '')

            id_num, topleft, size = line.split()

            id_num = int(id_num)

            width, height = [int(x) for x in size.split('x')]

            x, y = [int(x) for x in topleft.split(',')]

            pos = Pos(x, y)

            claims.append((id_num, pos, width, height))
    return claims


def get_rects(claims):
    ans = []
    for claim in claims:
        r = Rect(claim[0], claim[1], claim[2], claim[3])
        ans.append(r)
    return ans


def get_overlap_of_2_rects(a: Rect, b: Rect):
    # Take the difference between the most left ride-side, with the most right left-side
    dx = min(a.pos.x + a.width, b.pos.x + b.width) - max(a.pos.x, b.pos.x)

    # Same thing for y
    dy = min(a.pos.y + a.height, b.pos.y + b.height) - max(a.pos.y, b.pos.y)

    # If both are >= 0, there is some overlap
    if dx >= 0 and dy >= 0:
        return dx * dy


def get_overlap_dict(rects):
    overlap = dict()
    for i, a in enumerate(rects):
        amount = dict()
        for j, b in enumerate(rects):
            if i != j:
                result = get_overlap_of_2_rects(a, b)
                if result is not None and result != 0:
                    amount[b.id_num] = result
        overlap[a.id_num] = amount
    return overlap



def main():
    # Get input
    claims = get_input()

    # Convert to rect objects
    rects = get_rects(claims)

    # Make dict for tracking square overlaps
    squares = defaultdict(int)

    # Add squares
    for rect in rects:
        rect.add_squares_to_dict(squares)

    # Overlaps have more than one addition
    print(len([x for x in squares.items() if x[1] > 1]))  # Part 1 answer

    # Get fancy overlap dictionary that didn't quite workout for the fancy part 1 answer
    overlap = get_overlap_dict(rects)

    # The one with no overlaps is the one!
    print([x[0] for x in overlap.items() if len(x[1]) == 0][0])  # Part 2 answer


main()

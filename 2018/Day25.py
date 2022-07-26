def get_input():
    ans = []
    with open('input.txt') as f:
        for line in f:
            line = line.rstrip()
            ans.append(tuple([int(x) for x in line.split(',')]))
    return ans


def man_hat_dist(a, b):
    d = 0
    d += abs(a[0] - b[0])
    d += abs(a[1] - b[1])
    d += abs(a[2] - b[2])
    d += abs(a[3] - b[3])
    return d


def build_constellations(constellations: list[set]):
    # Can any part of a set connect with any other set?
    for i, a in enumerate(constellations):
        for j, b in enumerate(constellations):
            if a != b:
                for a_item in a:
                    for b_item in b:
                        if a_item != b_item:
                            if man_hat_dist(a_item, b_item) <= 3:
                                # Join these two sets
                                constellations[i] = a.union(b)
                                constellations.pop(j)
                                return build_constellations(constellations)
    return constellations


def part_1():
    points = get_input()
    constellations = []
    for point in points:
        constellations.append({point})
    ans = build_constellations(constellations)
    print(len(ans))

def main():
    part_1()



main()

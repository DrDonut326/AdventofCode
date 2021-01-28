def get_present_dimension():
    with open("input.txt") as f:
        ans = []
        for line in f:
            a, b, c = line.rstrip().split('x')
            ans.append((int(a), int(b), int(c)))
    return ans


def calculate_paper_for_surface_area(l, w, h):
    a = l * w
    b = w * h
    c = h * l
    return min(a, b, c) + (2 * a + 2 * b + 2 * c)


def calculate_ribbon(present):
    min1, min2 = sorted(present)[:2]
    a, b, c = present
    return min1 + min1 + min2 + min2 + (a * b * c)


def main(part):
    presents = get_present_dimension()
    if part == 1:
        # Part 1
        ans = 0
        for p in presents:
            a, b, c = p
            ans += calculate_paper_for_surface_area(a, b, c)
        print(ans)

    else:
        # Part 2
        ans = 0
        for p in presents:
            ans += calculate_ribbon(p)
        print(ans)

main(2)





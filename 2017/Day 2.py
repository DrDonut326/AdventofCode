def get_rows():
    ans = []
    with open('input.txt') as f:
        for line in f:
            line = line.rstrip()
            line = line.split()
            ans.append([int(x) for x in line])
    return ans


def minmaxdiff(row):
    return max(row) - min(row)


def get_checksum(rows):
    count = 0
    for row in rows:
        count += minmaxdiff(row)
    return count


def find_2_even_div(row):
    for i, a in enumerate(row):
        # Compare against all others
        for j, b in enumerate(row):
            if i != j:
                # Test
                if a % b == 0:
                    return a, b


def get_div_checksum(rows):
    count = 0
    for row in rows:
        a, b = find_2_even_div(row)
        count += a // b
    return count


def main():
    puzzle = get_rows()
    print(get_checksum(puzzle))  # Part 1
    print(get_div_checksum(puzzle))  # Part 2


main()

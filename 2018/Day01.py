def get_input():
    ans = []
    with open("input.txt") as f:
        for line in f:
            line = line.rstrip()
            if line[0] == '+':
                ans.append(int(line[1:]))
            else:
                ans.append(int(line))
    return ans


def main():
    frequencies = [0]
    changes = get_input()
    for change in changes:
        frequencies.append(frequencies[-1] + change)

    print(frequencies[-1]) # Part 1 answer

    seen = set(frequencies)

    while True:
        for c in changes:
            frequencies.append(frequencies[-1] + c)
            last = frequencies[-1]
            if last not in seen:
                seen.add(last)
            else:
                print(last)  # Part 2 ans
                quit()

main()

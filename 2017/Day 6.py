def get_input():
    ans = []
    with open('input.txt') as f:
        for line in f:
            line = line.rstrip()
            line = line.split()
            for x in line:
                ans.append(int(x))
    return ans


def add_to_seen(membank, seen):
    seen.add(tuple(membank))


def find_largest_bank_index(membank):
    maxy = None
    ans = None
    for i, num in enumerate(membank):
        if maxy is None or num > maxy:
            maxy = num
            ans = i
    return ans


def reallocate(membank, i):
    """Reallocates blocks at spot i"""
    communism = membank[i]
    membank[i] = 0

    while communism > 0:
        i += 1
        if i >= len(membank):
            i = 0
        membank[i] += 1
        communism -= 1


def part_1():
    membank = get_input()
    seen = set()
    add_to_seen(membank, seen)
    count = 0
    while True:
        # Find biggest block
        index = find_largest_bank_index(membank)

        # Reallocate
        reallocate(membank, index)
        count += 1

        # Check if seen before
        if tuple(membank) not in seen:
            add_to_seen(membank, seen)
        else:
            break

    print(count)
    return membank


def part_2(membank):
    seen = set()
    add_to_seen(membank, seen)
    count = 0
    while True:
        # Find biggest block
        index = find_largest_bank_index(membank)

        # Reallocate
        reallocate(membank, index)
        count += 1

        # Check if seen before
        if tuple(membank) not in seen:
            add_to_seen(membank, seen)
        else:
            break

    print(count)


def main():
    membank = part_1()
    part_2(membank)


main()

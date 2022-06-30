def get_blocked_ips():
    ans = []
    with open("input.txt") as f:
        for line in f:
            a, b = line.rstrip().split('-')
            ans.append((int(a), int(b)))
    # Sort
    ans.sort(key=lambda x: x[0])
    return ans


def check_for_overlap(x, block):
    return block[0] <= x <= block[1]


def is_overlapping_with_any(x, blocked):
    for block in blocked:
        if check_for_overlap(x, block):
            return True
    return False


def get_lowest_allowable_number(blocked, x):
    """Gets the next lowest possible range that comes after x"""
    # Start with +1
    lowest = x + 1

    # Check to see if this number overlaps with any block
    while is_overlapping_with_any(lowest, blocked):
        for block in blocked:
            if check_for_overlap(lowest, block):
                # Current inside the block, so raise it above
                lowest = block[1] + 1

    return lowest


def main():
    blocked = get_blocked_ips()

    list_of_lowest = []
    lowest = get_lowest_allowable_number(blocked, -1)  # Part 1 answer
    list_of_lowest.append(lowest)
    while lowest < 4294967295:
        lowest = get_lowest_allowable_number(blocked, lowest)
        list_of_lowest.append(lowest)

    if list_of_lowest[-1] > 4294967295:
        list_of_lowest.pop()
    print(len(list_of_lowest))  # Part 2 answer


main()

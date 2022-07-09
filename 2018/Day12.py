from collections import defaultdict


def get_input():
    pots = defaultdict(lambda: '.')
    rules = dict()
    with open('input.txt') as f:
        state_string = f.readline().rstrip().replace('initial state: ', '')
        for x, letter in enumerate(state_string):
            pots[x] = letter

        f.readline()

        for line in f:
            line = line.rstrip()
            left, right = line.split(' => ')
            rules[left] = right

    return pots, rules


def get_pot_neighbors(pots, n):  # n = key
    return pots[n-2] + pots[n-1] + pots[n] + pots[n+1] + pots[n+2]


def display_pots(pots, iteration=None):
    min_x = min(pots.keys())
    max_x = max(pots.keys())
    x = min_x
    if iteration is not None:
        print(f"Iter: {iteration} :", end='')
    while x <= max_x:
        print(pots[x], end='')
        x += 1
    print()


def get_first_and_last_key_of_plants(pots):
    plants = [x[0] for x in pots.items() if x[1] == '#']
    plants.sort()
    return plants[0], plants[-1]

def update_pots(pots: defaultdict, rules: dict):
    original_pots = pots.copy()
    start, finish = get_first_and_last_key_of_plants(pots)
    start = start - 2
    finish = finish + 2
    while start <= finish:
        neighbor_string = get_pot_neighbors(original_pots, start)
        assert neighbor_string in rules
        pots[start] = rules[neighbor_string]
        start += 1


def part_1(pots):
    count = 0
    for i, pot in pots.items():
        if pot == '#':
            count += i
    return count


def part_2(pots, bigboi):
    count = 0
    for i, pot in pots.items():
        if pot == '#':
            count += i + bigboi
    return count

def main():
    pots, rules = get_input()
    repeats = 100
    iteration = 0
    # keep track of how many times you've reached that number of plants
    results = defaultdict(int)

    for _ in range(repeats):  # Stable by 100
        iteration += 1
        update_pots(pots, rules)

    # Pots stay the same, but keep moving to the right
    # So you just need to add the equivalent missing number of empty pots to each value once it gets stable
    big_dots = 50000000000 - 100
    print(part_2(pots, big_dots))


main()

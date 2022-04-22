from collections import defaultdict


def get_input():
    with open("input.txt") as f:
        polymer = f.readline().rstrip()
        f.readline()
        changes = defaultdict(str)
        for line in f:
            a, b = line.rstrip().split(' -> ')
            changes[a] = b
    return polymer, changes

def poly_insert(polymer, changes):
    """Returns the polymer after 1 round of changes"""
    ans = ''
    for a, b in zip(polymer, polymer[1::]):
        # Add the first pair
        ans += a

        # Check to see if the ab pair is in the changes and insert the result
        ab = a + b
        if ab in changes:
            ans += changes[ab]

        else:
            raise Exception('Not in changes list!')

    # Add the final letter at the end
    ans += polymer[-1]

    return ans

def part_1_main():
    polymer, changes = get_input()
    original_polymer = polymer
    # Insert polymers n times
    n = 20

    polymer_list = [polymer]

    for _ in range(n):
        # Do normal insertions
        new_polymer = poly_insert(polymer, changes)

        changes[polymer] = new_polymer
        polymer_list.append(new_polymer)
        polymer = new_polymer

    # Get most common and least common element
    count_dict = defaultdict(int)
    for letter in polymer:
        count_dict[letter] += 1

    max_num = max(count_dict.items(), key=lambda x: x[1])
    min_num = min(count_dict.items(), key=lambda x: x[1])


def part_2_main():
    """Keep track of pairs, not the whole polymer"""
    polymer, changes = get_input()
    original_polymer = polymer

    # Setup pairs graph
    pairs_graph = defaultdict(int)
    for a, b in zip(original_polymer, original_polymer[1::]):
        pairs_graph[a+b] += 1

    for _ in range(40):
        current_pairs = list(pairs_graph.items())
        for k, n in current_pairs:
            pairs_graph[k] -= n
            a = k[0] + changes[k]
            b = changes[k] + k[1]
            pairs_graph[a] += n
            pairs_graph[b] += n

    # Letter graph
    letter_graph = defaultdict(int)
    for key, n in pairs_graph.items():
        a = key[0]
        b = key[1]

        letter_graph[b] += n

    max_num = max(letter_graph.values())
    min_num = min(letter_graph.values())

    print(max_num-min_num-1)








part_2_main()

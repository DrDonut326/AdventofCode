def get_input():
    with open("input.txt") as f:
        return f.readline().rstrip()



def do_polarities_match(a, b):
    if a.lower() == b.lower():
        return (a.islower() and b.isupper()) or (a.isupper() and b.islower())


def collapse_polymer(polymer):
    ans = [polymer[0]]
    bi = 1
    p_length = len(polymer)
    while bi < p_length:
        # Edge case for if the front of the list gets nuked
        # If the front 2 are matching set the front of answer to bi and increment
        if len(ans) == 0:
            ans.append(polymer[bi])
            bi += 1

        # A is always the last good letter of the polymer
        a = ans[-1]
        # B increments along, skipping ahead of deletions
        b = polymer[bi]

        # If 2 letters match, get rid of the last good letter
        if do_polarities_match(a, b):
            # Matching letters
            ans.pop()
        else:
            # No match
            ans.append(b)
        bi += 1

    return ''.join(ans)



def main():
    polymer = get_input()
    collapsed = collapse_polymer(polymer)

    print(len(collapsed)) # Part 1 ans

    # Get set of all letters in lowercase form
    letters = set(polymer.lower())

    # Iterate through all letter types and remove them and collapse the result

    # Record the best result length\
    shortest_length = None

    for letter in letters:
        prototype_polymer = polymer.replace(letter.upper(), '')
        prototype_polymer = prototype_polymer.replace(letter, '')
        reaction = collapse_polymer(prototype_polymer)
        if shortest_length is None or len(reaction) < shortest_length:
            shortest_length = len(reaction)

    print(shortest_length) # Part 2 answer


main()

from collections import defaultdict
from Functions import get_input


def get_rules():
    forwards = defaultdict(list)
    backwards = defaultdict(list)
    lines = get_input('line', split_key=' => ', do_split=True, early_stop=True)

    for rule in lines:
        left, right = rule
        forwards[left].append(right)
        backwards[right].append(left)
    return forwards, backwards


def mutate_forward(forwards, molecule):
    # Rules can be longer than one length!!!!!!!!!!

    found = set()  # Keep track of internal things found already

    # Iterate through all the rules
    # Substitute for each possible place
    mutations = []
    for f in forwards:
        # Check to see if the letter is in the molecule
        if f in molecule:
            # Iterate through EACH RULE of that letter
            for replacement in forwards[f]:
                for i, letter in enumerate(molecule):
                    # Iterate through the molecule looking for place to insert
                    t = molecule[i: i + len(f)]
                    if t == f:
                        # If you find a match, create a new molecule

                        new_molecule = molecule[0:i] + replacement + molecule[i+len(f):]

                        # Check to see if the new molecule is already found
                        if new_molecule not in found:
                            mutations.append(new_molecule)
                            found.add(new_molecule)
    return mutations


def get_starting_molecule():
    with open("input.txt") as f:
        while True:
            t = f.readline().rstrip()
            if t == '':
                break
        return f.readline().rstrip()


def fully_collapse_molecule(molecule, backwards):
    count = 0
    while True:
        if molecule == 'e':
            return count
        for key, repl in backwards.items():
            repl = repl[0]
            if key in molecule:
                while key in molecule:
                    molecule = molecule.replace(key, repl, 1)
                    count += 1


def main():
    # Dictionaries that govern what can be transformed
    forwards, backwards = get_rules()
    starting_molecule = get_starting_molecule()
    next_mutations = mutate_forward(forwards, starting_molecule)
    print(f"Part 1 Answer: {len(next_mutations)}")

    # Part 2
    starting_molecule = get_starting_molecule()
    count = fully_collapse_molecule(starting_molecule, backwards)
    print(f"Part 2 Answer: {count}")


main()

from collections import deque, defaultdict
from Utility import get_input

# TODO: Figure out the explored set.  What do I need to add?
# Redo.  Try to go from the finished product back down towards 'e'
# Only explore paths


class Graph:
    """Find a path from start_string to end_string
    Keeps track of the path and returns it.
    Either depth first or breadth first search"""
    def __init__(self, start_string, end_string, transform):
        self.explored = set()
        self.queue = deque()
        self.start_string = start_string
        self.end_string = end_string
        self.initialize_queue()
        # Transform: Should be a FUNCTION that returns a list of
        # mutations from the given input string
        self.transform = transform

    def get_list_string(self, x):
        assert type(x) == list
        add_string = ''.join(x)
        assert type(add_string) == str
        return add_string

    def initialize_queue(self):
        """Sets up the starting condition of the search queue"""
        self.queue.append([self.start_string])
        self.explored.add(self.start_string)

    def breadth_first_search(self, search_dict):
        """Returns the shortest path from start to end strings"""
        while len(self.queue) > 0:
            # Item is a list (path)
            item = self.queue.popleft()
            assert type(item) == list
            if item[-1] == self.end_string:
                # Answer is found, return the whole path
                return item

            else:
                next_list = []
                # Need to mutate the string and add them back into the stack
                mutations = self.transform(search_dict, item[-1])
                for mut in mutations:
                    if len(mut) <= len(self.end_string):
                        t = item.copy()
                        t.append(mut)
                        if self.get_list_string(t) not in self.explored:
                            next_list.append(t)
                            print(t)
                            print(self.end_string)
                            quit()
                            assert len(t[-1]) < self.end_string
            if len(self.queue) == 0 and len(next_list) > 0:
                for m in next_list:
                    self.queue.append(m)


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


def mutate_backwards(backwards, molecule):
    # Rules can be longer than one length!!!!!!!!!!

    print(molecule)
    quit()
    found = set()  # Keep track of internal things found already

    # Iterate through all the rules
    # Substitute for each possible place
    mutations = []
    for f in backwards:
        # Check to see if the letter is in the molecule
        if f in molecule:
            # Iterate through EACH RULE of that letter
            for replacement in backwards[f]:
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


def get_starting_molecule():
    with open("input.txt") as f:
        while True:
            t = f.readline().rstrip()
            if t == '':
                break
        return f.readline().rstrip()


def main():
    # Dictionaries that govern what can be transformed
    forwards, backwards = get_rules()   #TODO: Change for real input last line different
    # starting_molecule = get_starting_molecule()
    # next_mutations = mutate_forward(forwards, starting_molecule)
    # print(f"Part 1 Answer: {len(next_mutations)}")

    # Part 2
    starting_molecule = 'e'
    goal_molecule = get_starting_molecule()
    graph = Graph(starting_molecule, goal_molecule, mutate_forward)
    ans = graph.breadth_first_search(forwards)
    print(ans)


main()

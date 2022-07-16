from collections import defaultdict
from copy import deepcopy
from itertools import permutations, combinations
from queue import PriorityQueue
from time import time


# TODO: Look out for names that start with M or G.  Will cause problems with the flipping.  Change the naming convention?
# TODO: Add double moves to the get_all_moves_function


def sort_floors(floors):
    for floor in floors.values():
        floor.sort()


def get_state(floors, elevator_starting_floor):
    """Gets the state of the floors.  Elevator position is always the last position"""
    ans = []
    for floor, items in floors.items():
        for stuff in items:
            ans.append(f"{floor}@{stuff}")
    ans.sort()
    ans.append(elevator_starting_floor)
    return tuple(ans)


def build_all_pairs(floors):
    all_items = []
    for x in floors.values():
        for y in x:
            all_items.append(y)
    ans = defaultdict(list)
    for item in all_items:
        ans[item[0]].append(item)
    return ans


def all_on_fourth_floor(state):
    state = list(state)
    elevator = state.pop()
    state = tuple(state)
    for item in state:
        if any(i in ['1', '2', '3'] for i in item):
            return False
    return True


def get_all_pairs_of_floor(state, floor_num):
    # Get all items on the current floor
    items = []
    for item in state:
        if item.startswith(str(floor_num)):
            items.append(item)
    all_pairs = combinations(items, 2)

    # Prune any pairs where a microchip is moving with a generator that doesn't match it
    final_pairs = []
    for p in all_pairs:
        a, b = p

        # Strip away the floor number
        a = a[2:]
        b = b[2:]

        # If either is a chip, and they dont' match, reject
        if a[-1] == 'M' or b[-1] == 'M':
            if a[0] == b[0]:
                final_pairs.append(p)
        else:
            final_pairs.append(p)

    return final_pairs


def get_all_moves(state, visited):
    all_moves = []

    # Pop elevator off of state
    state = list(state)
    elevator = state.pop()
    state = tuple(state)

    # TODO: Split this section into up and down
    # TODO: If you can move two items upstairs, don't bother bringing one item upstairs. If you can move one item downstairs, don't bother bringing two items downstairs.

    # ---- get double moves ----
    # get a list of all items
    all_pairs = get_all_pairs_of_floor(state, elevator)

    for p in all_pairs:
        # Make up and down copies of each pair
        double_up_copy = list(state)
        double_down_copy = list(state)

        # Make up
        for replace_item in p:
            for i, original_item in enumerate(double_up_copy):
                if original_item == replace_item:
                    f, name = replace_item.split('@')
                    f = int(f)
                    double_up_copy[i] = f"{f + 1}@{name}"

        # Make down
        for replace_item in p:
            for i, original_item in enumerate(double_down_copy):
                if original_item == replace_item:
                    f, name = replace_item.split('@')
                    f = int(f)
                    double_down_copy[i] = f"{f - 1}@{name}"

        # Sort them both
        double_up_copy.sort()
        double_down_copy.sort()

        # Add elevator back in
        double_up_copy.append(elevator + 1)
        double_down_copy.append(elevator - 1)

        # Put in the answer
        all_moves.append(tuple(double_up_copy))
        all_moves.append(tuple(double_down_copy))

    # ------------------get all single moves-----------------------------
    for i, item in enumerate(state):
        # Make copies of the input state
        state_up = list(state)
        state_down = list(state)

        # Get the floor number and object name
        floor, name = item.split('@')
        floor = int(floor)

        # Only proceed if the floor number matches the current elevator
        if floor == elevator:

            # Make up copy
            state_up[i] = f"{floor + 1}@{name}"
            # Make down copy
            state_down[i] = f"{floor - 1}@{name}"

            # Sort them both
            state_up.sort()
            state_down.sort()

            # Add the elevator back in
            state_up.append(elevator + 1)
            state_down.append(elevator - 1)

            # Put in the answer
            all_moves.append(tuple(state_up))
            all_moves.append(tuple(state_down))

    return all_moves


def is_state_in_bounds(state):
    state = list(state)
    elevator = state.pop()
    for item in state:
        floor, name = item.split('@')
        if int(floor) < 1 or int(floor) > 4:
            return False
    return True


def are_there_gens_on_this_floor(floor):
    for item in floor:
        if item.endswith('G'):
            return True
    return False


def is_state_legal(state):
    # A state is illegal if a chip is with a non-matching generator without being with its own
    # So a state is legal if:
    #  -- The floor has no generators
    # or
    #  -- every chip has it's coresponding generator

    # Pop off the elevator
    state = list(state)
    elevator = state.pop()
    state = tuple(state)



    # Build a floor_map
    floors = {'1': [], '2': [], '3': [], '4': []}
    for item in state:
        floor_num, name = item.split('@')
        floors[floor_num].append(name)

    for floor in floors.values():
        # If there are no generators on the floor, no need to check anything else
        # as microchips are cool hanging around each other
        if are_there_gens_on_this_floor(floor):
            # There are generators present so make sure any chips around have a buddy
            # Check if this is a microchip
            for item in floor:
                if item.endswith('M'):
                    # If buddy gen is not present, this state is ILLEGAL
                    buddy_gen = item[0] + 'G'
                    if buddy_gen not in floor:
                        return False
    return True


def get_valid_moves(all_moves):
    valid = []
    for state in all_moves:
        if is_state_in_bounds(state) and is_state_legal(state):
            valid.append(state)
    return valid


def flip_all_a_b_in_state(state, a, b):
    """Returns a new tuple with a, b flipped"""
    # Pop the elevator off
    elevator = state.pop()

    for i, item in enumerate(state):
        floor, name = item.split('@')
        if name.startswith(a):
            new_name = b + name[1:]
            state[i] = f"{floor}@{new_name}"
        if name.startswith(b):
            new_name = a + name[1:]
            state[i] = f"{floor}@{new_name}"

    state.append(elevator)

    return tuple(state)


def add_state_to_visited_and_all_equivalencies(state, visited, pairs):
    # Add this state as is
    visited.add(state)

    # Get all equivalent states
    # -- Iterate through all pairs and replace all A with B
    for pair in pairs:
        a, b = pair
        state_copy = list(state)
        new_tuple_state = flip_all_a_b_in_state(state_copy, a, b)

        # Add the new equivalent tuple to visited
        visited.add(new_tuple_state)



def bfs(initial_state, name_pairs):
    visited = set()
    q = PriorityQueue()
    add_state_to_visited_and_all_equivalencies(initial_state, visited, name_pairs)
    q.put((0, [initial_state]))

    while not q.empty():
        steps, path = q.get()
        state = path[-1]

        # Check if finished
        if all_on_fourth_floor(state):
            return steps, path

        # get NEIGHBORS
        all_moves = get_all_moves(state, visited)

        # Prune moves that are not valid states
        valid_moves = get_valid_moves(all_moves)

        for move in valid_moves:
            if move not in visited:
                add_state_to_visited_and_all_equivalencies(move, visited, name_pairs)
                # Increase the steps by 1
                copy_path = deepcopy(path)
                copy_path.append(move)
                q.put((steps + 1, copy_path))

    print(f"No answer found!")
    quit()


def get_all_name_pairs(floors):
    names = set()
    for floor in floors.values():
        for item in floor:
            names.add(item[0])
    pairs = permutations(names, 2)
    return pairs


def main():
    start = time()
    floors = {1: ['TG', 'TM', 'PG', 'SG', 'EG', 'EM', 'DG', 'DM'], 2: ['PM', 'SM'], 3: ['ZG', 'ZM', 'RG', 'RM'], 4: []}
    elevator_starting_floor = 1
    name_pairs = get_all_name_pairs(floors)
    sort_floors(floors)
    state = get_state(floors, elevator_starting_floor)
    steps, path = bfs(state, name_pairs)
    for p in path:
        print(p)
    print(f"The solution was found in {steps} after {time() - start} seconds.")


if __name__ == '__main__':
    main()


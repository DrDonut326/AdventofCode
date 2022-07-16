from math import sqrt

import numpy as np


def rule_string_to_2d_array(rule):
    ans = []
    row = []
    for symbol in rule:
        if symbol == '/':
            ans.append(row)
            row = []
        else:
            row.append(symbol)
    ans.append(row)
    return ans


def display_2d_array(arr):
    for row in arr:
        print(row)
    print()


def array_2d_to_rule_string(arr):
    ans = []
    for row in arr:
        for element in row:
            ans.append(element)
        ans.append('/')
    # Get rid of final /
    ans = ans[:-1]
    ans = ''.join(ans)
    return ans


def return_rule_permutations(rule):
    """Returns all possible flattened permuations of that rule (flipped / rotated)"""
    # ---- All these permutations should point to the base rule ------
    perms = set()
    rule_arr = rule_string_to_2d_array(rule)

    # Add the base case to perms
    perms.add(array_2d_to_rule_string(rule_arr))

    # Flip vertical
    vert_flip = np.flipud(rule_arr)
    perms.add(array_2d_to_rule_string(vert_flip))

    # Flip horizontal
    hor_flip = np.fliplr(rule_arr)
    perms.add(array_2d_to_rule_string(hor_flip))

    for _ in range(3):
        # Rotate / repeat
        rule_arr = np.rot90(rule_arr)
        perms.add(array_2d_to_rule_string(rule_arr))

        # Flip vertical
        vert_flip = np.flipud(rule_arr)
        perms.add(array_2d_to_rule_string(vert_flip))

        # Flip horizontal
        hor_flip = np.fliplr(rule_arr)
        perms.add(array_2d_to_rule_string(hor_flip))

    return perms


def get_perms_dict(rules):
    """Returns a dictionary of rule variations --> base rule."""
    ans = dict()

    # For each rule, get all perms and point them towards the base rule
    for rule in rules:
        perms = return_rule_permutations(rule)
        # Add the base case of rule --> rule
        ans[rule] = rule
        for perm in perms:
            ans[perm] = rule
    return ans


def get_rules_dict():
    """Returns a dict from the input file
    in the form of rule: output string"""
    ans = dict()
    with open("input.txt") as f:
        for line in f:
            line = line.rstrip()
            rule, output = line.split(' => ')
            ans[rule] = output
    return ans


def subdivide_3_array(arr):
    """Divides an array divisible by 3 into 3x3 chunks"""
    assert len(arr) % 3 == 0

    ans = []

    row_length = len(arr)

    y = 0
    while y < row_length:

        # Iterate along x
        x = 0
        chunk = []
        while x < row_length:
            row_1 = []
            row_1.append(arr[y][x])
            row_1.append(arr[y][x+1])
            row_1.append(arr[y][x+2])

            row_2 = []
            row_2.append(arr[y+1][x])
            row_2.append(arr[y+1][x + 1])
            row_2.append(arr[y+1][x + 2])

            row_3 = []
            row_3.append(arr[y + 2][x])
            row_3.append(arr[y + 2][x + 1])
            row_3.append(arr[y + 2][x + 2])

            chunk.append(row_1)
            chunk.append(row_2)
            chunk.append(row_3)

            ans.append(chunk)
            chunk = []

            x += 3

        y += 3

    return ans


def subdivide_2_array(arr):
    """Divides an array divisible by 2 into 2x2 chunks"""
    assert len(arr) % 2 == 0

    ans = []

    row_length = len(arr)


    y = 0
    while y < row_length:

        # Iterate along x
        x = 0
        chunk = []
        while x < row_length:
            row_1 = []
            row_1.append(arr[y][x])
            row_1.append(arr[y][x+1])


            row_2 = []
            row_2.append(arr[y+1][x])
            row_2.append(arr[y+1][x + 1])

            chunk.append(row_1)
            chunk.append(row_2)

            ans.append(chunk)
            chunk = []

            x += 2

        y += 2

    return ans


def rebuild(outputs):
    """Rebuilds a new 2d array from a list of array strings"""
    row_lengths = int(sqrt(len(outputs)))

    # Get rows of row_lengths arrays and combine them horizontally
    # Then move down until you've gottem all

    rows = []
    x = 0
    while x < len(outputs):
        to_combine = [rule_string_to_2d_array(x) for x in outputs[x:x+row_lengths]]
        rows.append(np.concatenate(to_combine, axis=1))
        x += row_lengths

    ans = np.concatenate(rows)

    return ans


def iterate(arr, perms, rules):
    # Break into chunks  *** will return a list of arrays ***
    if len(arr) % 2 == 0:
        chunks = subdivide_2_array(arr)

    elif len(arr) % 3 == 0:
        chunks = subdivide_3_array(arr)

    else:
        raise EnvironmentError('Bad divisible somehow.')

    # Convert those chunks into rule strings
    rules_list = []
    for chunk in chunks:
        # These could be permutations of a rule, run it through the perm dict
        potential_perm = array_2d_to_rule_string(chunk)
        rule = perms[potential_perm]
        rules_list.append(rule)


    # Match each rule to the output
    outputs = []
    for rule in rules_list:
        outputs.append(rules[rule])


    # Rebuild into one square array
    new_array = rebuild(outputs)
    return new_array


def count_on(arr):
    count = 0
    for row in arr:
        for x in row:
            if x == '#':
                count += 1
    return count


def main():
    rules = get_rules_dict()
    perms = get_perms_dict(rules.keys())

    start_string = '.#./..#/###'
    arr = rule_string_to_2d_array(start_string)

    for _ in range(18):  # 5 for part 1, 18 for part 2
        arr = iterate(arr, perms, rules)


    print(count_on(arr))






main()

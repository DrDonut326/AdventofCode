import numpy as np
from collections import defaultdict


# TODO: Calculate three iterations of each 3x3 block.

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


def get_next_rule(rule, rules, perms):
    perm = perms[rule]
    ans = rules[perm]
    return ans


def break_into_2x2(four):
    """Breaks a 4x4 rule string into 4 2x2 rule strings."""
    ans = []

    rule1 = four[0] + four[1] + '/' + four[5] + four[6]
    rule2 = four[2] + four[3] + '/' + four[7] + four[8]
    rule3 = four[10] + four[11] + '/' + four[15] + four[16]
    rule4 = four[12] + four[13] + '/' + four[17] + four[18]

    ans.append(rule1)
    ans.append(rule2)
    ans.append(rule3)
    ans.append(rule4)

    return ans


def get_fours_dict(rules, perms):
    """Returns a dictionary of what each 4x4 will break into."""

    ans = dict()

    # Get a list of all 4x4 outputs
    four_outputs = [x for x in rules.values() if len(x) == 19]

    # For each divide into four 2x2 arrays
    for four in four_outputs:
        # Get the four sub blocks
        two_by_twos = break_into_2x2(four)

        # Find what each two will turn into
        three_blocks = []
        for two in two_by_twos:
            three_blocks.append(get_next_rule(two, rules, perms))

        # Update the answer
        ans[four] = three_blocks

    return ans


def count_on(art_dict):
    count = 0
    for rule in art_dict:
        count += rule.count('#') * art_dict[rule]
    return count

def main():
    start_rule = '.#./..#/###'
    rules = get_rules_dict()
    perms = get_perms_dict(rules.keys())
    fours = get_fours_dict(rules, perms)


    # Init master dictionary
    art_dict = defaultdict(int)

    # Add the starting pattern
    art_dict[start_rule] += 1

    # Iterate                 - Get rid of each existing rule as you mutate it!
    for _ in range(18):

        # Get a list of rules to update this iteration
        print(f"Rules starting this iteration:")
        rules_to_check = list(art_dict.keys())
        print(rules_to_check)


        for rule in rules_to_check:
            # 3 x 3 block
            if len(rule) == 11:
                # Add 1 answer for each existing rule
                art_dict[get_next_rule(rule, rules, perms)] += (1 * art_dict[rule])

                # Remove the rule we just mutated
                art_dict.pop(rule)

            # 4 x 4 block
            elif len(rule) == 19:
                # Get the 4 outputs of the 4x4 block
                threes = fours[rule]

                # Add each one
                for three in threes:
                    art_dict[three] += (1 * art_dict[rule])

                # Remove the rule we just mutated
                art_dict.pop(rule)

            print(f"Art dict at the end of iteration...")
            print(art_dict)

    # Count total on
    print(count_on(art_dict))

main()

# Try to work backwards

# An output chunk of 3x3 will turn into 1 more 4x4 of a certain type

# An output chunk of 4x4 will turn into 4 more (different) 2x2s
# And each of those will turn into 1 3x3


# Build a dictionary of all rotated / flipped rules
# and map them to their outputs


# Build a dictionary of what each 4x4 output creates when subdivided


# Each iteration, count how many of each are being produced, and multiply the results
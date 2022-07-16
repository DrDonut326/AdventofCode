from collections import defaultdict

from anytree import Node


def get_input():
    ans = []
    with open('input.txt') as f:
        for line in f:
            line = line.rstrip()
            ans.append(line)
    return ans


def get_weights(lines):
    ans = defaultdict(int)
    for line in lines:
        # Get just left side
        if '->' in line:
            left, right = line.split(' -> ')
            line = left

        line = line[:-1]
        name, weight = line.split(' (')
        weight = int(weight)
        ans[name] = weight
    return ans


def get_parents(lines):
    """Returns a dict with [child]: parent"""
    ans = dict()
    for line in lines:
        if '->' in line:
            left, right = line.split(' -> ')

            name, age = left.split(' ')
            children = right.split(', ')

            for child in children:
                ans[child] = name

    return ans


def get_names(lines):
    """Returns a list of all names"""
    ans = []
    for line in lines:
        name, garbage = line.split(' (')
        ans.append(name)
    return ans


def build_nodes(names, parents, weights):
    nodes = dict()
    for name in names:
        new_node = Node(name, weight=weights[name])
        nodes[name] = new_node

    # Set parents
    for name in names:
        if name in parents:
            parent_name = parents[name]
            nodes[name].parent = nodes[parent_name]

    return nodes


def find_root(nodes):
    for name in nodes:
        if nodes[name].is_root:
            return nodes[name]


def get_total_weight(node: Node):
    """Return own weight + weight of all children"""
    total = node.weight
    for child in node.children:
        total += get_total_weight(child)
    return total


def find_different_stack(children):
    """Returns the odd weight stack, as well as the difference to the others"""
    weights = defaultdict(list)
    for child in children:
        total_weight = get_total_weight(child)
        weights[total_weight].append(child)

    # Find the odd one out
    odd_node = None
    for w in weights:
        if len(weights[w]) == 1:
            odd_node = weights[w][0]

    # Find an even one for comparison
    working_node = None
    for w in weights:
        if len(weights[w]) > 1:
            working_node = weights[w][0]

    # Check for all same
    if odd_node is None:
        return None, None

    difference = get_total_weight(odd_node) - get_total_weight(working_node)
    return odd_node, difference


def main():
    lines = get_input()
    weights = get_weights(lines)
    parents = get_parents(lines)
    names = get_names(lines)
    nodes = build_nodes(names, parents, weights)

    root_node = find_root(nodes)

    print(f"Part 1 answer is {root_node.name}.")  # Part 1 answer

    odd_node, difference = find_different_stack(root_node.children)

    # Find the node that has balanced children
    while True:
        result, difference_result = find_different_stack(odd_node.children)
        if result is None:
            break
        else:
            odd_node, result = result, difference_result

    print(odd_node, difference)
    print(odd_node.weight - difference)  # Part 2 answer


main()

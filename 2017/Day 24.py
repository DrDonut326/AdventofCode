from anytree import Node, PreOrderIter



# TODO: Use a tree structure to build all possibilities


def get_parts():
    parts = []
    with open("input.txt") as f:
        for line in f:
            line = line.rstrip()
            a, b = line.split('/')
            parts.append((int(a), int(b)))
    return parts


def build_tree(parent, open_port, parts):
    """Go through parts and add valid children to this node"""
    # Iterate through the parts
    for part in parts:

        # If that part fits, attach it and mark the other number as valid
        if open_port in part:
            new_node = Node(part, parent)

            if part[0] == open_port:
                new_open_port = part[1]
            else:
                new_open_port = part[0]

            # Get a new copy of the parts
            parts_copy = parts.copy()
            parts_copy.remove(part)
            build_tree(new_node, new_open_port, parts_copy)

def allpaths(start):
    skip = len(start.path) - 1
    return [leaf.path[skip:] for leaf in PreOrderIter(start, filter_=lambda node: node.is_leaf)]


def build_all_trees(parts):
    trees = []
    # Starts a new tree for each part that has 0.
    # Make a copy of the remaining parts and pass it along up the tree

    for part in parts:
        if 0 in part:
            parts_copy = parts.copy()
            parts_copy.remove(part)
            # Make a tree root
            r = Node(part)
            # Grow the tree
            build_tree(r, part[1], parts_copy)
            # Plant the tree
            trees.append(r)

    return trees


def get_sum_of_tree_path(path):
    n = 0
    for x in path:
        a, b = x.name
        n += a + b
    return n


def get_best_path_from_single_tree(tree):
    all_paths = allpaths(tree)
    best_score = 0
    best_path = None
    for path in all_paths:
        path_score = get_sum_of_tree_path(path)
        if best_path is None or path_score > best_score:
            best_score = path_score
            best_path = path
    return best_path, best_score


def find_strongest_bridge(trees):
    best_score = 0
    best_path = None
    for tree in trees:
        path, score = get_best_path_from_single_tree(tree)
        if best_path is None or score > best_score:
            best_score = score
            best_path = path

    return best_path, best_score


def get_longest_paths(trees):
    all_paths = []
    for tree in trees:
        that_tree_paths = allpaths(tree)
        for p in that_tree_paths:
            all_paths.append(p)

    longest_bridge_len = len(max(all_paths, key=len))

    long_paths = [x for x in all_paths if len(x) == longest_bridge_len]

    return long_paths


def get_best_long_bridge(longest_bridges):
    best_score = 0
    best_bridge = None
    for bridge in longest_bridges:
        b_sum = get_sum_of_tree_path(bridge)
        if best_bridge is None or b_sum > best_score:
            best_score = b_sum
            best_bridge = bridge
    return best_bridge, best_score


def main():
    parts = get_parts()
    trees = build_all_trees(parts)
    best_bridge, best_score = find_strongest_bridge(trees)
    print(f"Strongest bridge was {[x.name for x in best_bridge]}")
    print(f"Bridge strength was {best_score}")

    longest_bridges = get_longest_paths(trees)
    best_long_bridge, best_long_bridge_score = get_best_long_bridge(longest_bridges)

    print(f"Strongest-longest bridge was {best_long_bridge}")
    print(f"Long bridge strength was {best_long_bridge_score}")


main()

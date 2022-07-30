from anytree import Node, Walker
from functools import lru_cache


def get_nodes():
    added = set()
    nodes = dict()
    with open("input.txt") as f:
        for line in f:
            line = line.rstrip()
            center, orbiter = line.split(')')
            if center not in added:
                nodes[center] = Node(center)
                added.add(center)
            if orbiter in added:
                nodes[orbiter].parent = nodes[center]
            else:
                n = Node(orbiter, nodes[center])
                nodes[orbiter] = n
                added.add(orbiter)

    # Find root
    for n in nodes.values():
        if n.parent is None:
            root = n
            break
    return nodes, root


@lru_cache
def count_parents(node: Node):
    if node.parent is None:
        return 0
    else:
        return 1 + count_parents(node.parent)


def main():
    # Count how many orbits and sub-orbit each planet has
    nodes, root = get_nodes()
    total = 0
    for node in nodes.values():
        total += count_parents(node)
    print(total)  # Part 1 Answer

    # Use a walker object to find the shortest path
    walker = Walker()

    # Get your and Santa's orbital planets
    start = nodes['YOU'].parent
    finish = nodes['SAN'].parent

    # Get shortest path
    route = walker.walk(start, finish)
    total = 0
    for r in route:
        if type(r) == tuple:
            for node in r:
                print(node.name)
                total += 1
        else:
            print(r.name)
            total += 1

    # Subtract your starting planet to get the right answer
    print(total - 1)  # Part 2 answer


main()

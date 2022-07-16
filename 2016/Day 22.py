from dataclasses import dataclass

from Grids import DictGrid
from Pos import Pos


@dataclass
class Node:
    pos: Pos
    size: int
    used: int
    avail: int
    use_percent: int


def make_nodes():
    # Create all nodes
    nodes = []
    with open('input.txt') as f:
        f.readline()
        f.readline()
        for line in f:
            line = line.replace('/dev/grid/node-', '')
            pos, size, used, avail, use_percent = line.split()
            x, y = pos.split('-')
            x = int(x[1:])
            y = int(y[1:])
            pos = Pos(x, y)
            n = Node(pos, int(size[:-1]), int(used[:-1]), int(avail[:-1]), int(use_percent[:-1]))
            nodes.append(n)
    return nodes

def get_grid():
    nodes = make_nodes()
    grid = DictGrid(None)
    for node in nodes:
        grid.add_data_to_grid_at_pos(node, node.pos)
    x_min, x_max, y_min, y_max = grid.get_graph_min_max()
    grid.x_size = x_max + 1
    grid.y_size = y_max + 1
    return grid


def is_pair_viable(a, b):
    if a.used != 0:
        if a is not b:
            if a.used <= b.avail:
                return True
    return False


def count_viable_pairs(nodes):
    count = 0
    for a in nodes:
        for b in nodes:
            if is_pair_viable(a, b):
                count += 1
    return count


def get_goal_nodes(nodes):
    goal = max(nodes, key=lambda x: x.pos.x)
    return goal


def transfer_from_a_to_b(a: Node, b: Node):
    """Transfers ALL data between a and b and updates their data accordingly."""
    # Note, not updated used for now
    assert is_pair_viable(a, b)
    data_amount = a.used

    # Transfer to b
    b.used += data_amount
    b.avail -= data_amount

    # Update a
    a.used -= data_amount
    a.avail += data_amount

    assert a.used == 0


def get_neighbors_of_a(a, grid: DictGrid):
    neighbors = grid.get_neighbors_4way(a.pos, exist=True)
    return neighbors


def get_viable_pairs_from_node(a, grid):
    """Gets nodes such that a could transfer to b"""
    ans = []
    neighbors = get_neighbors_of_a(a, grid)
    for b in neighbors:
        if is_pair_viable(a, b):
            ans.append(b)
    return ans


def pretty_print(grid, goal_node):
    x_size = grid.x_size
    y_size = grid.y_size
    for y in range(y_size):
        row = ''
        for x in range(x_size):
            pos = Pos(x, y)
            node = grid.get_value_from_pos_object(pos)
            # Make sure each part is uniform
            if node == goal_node:
                row += 'G'
            elif node.pos.x == 0 and node.pos.y == 0:
                row += 'S'
            elif node.used > 99:
                row += '*'
            elif node.used == 0:
                row += 'E'
            else:
                row += '.'

        print(row)



def main():
    grid = get_grid()
    nodes = make_nodes()
    viable_pairs = count_viable_pairs(nodes)
    #print(viable_pairs) Part 1 answer
    goal = get_goal_nodes(nodes)


    pretty_print(grid, goal)



main()

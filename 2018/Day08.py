from anytree import Node, RenderTree, PreOrderIter
from Functions import render_a_tree




# Header is 2 numbers always
#  - Quanity of child nodes
#  - Quantity of metadata entries
# P1 answer = 43825  (add up all metadata entries)
# P2 answer = 19276 (





def get_input():
    with open("input.txt") as f:
        for line in f:
            return [int(x) for x in line.rstrip().split()]


def add_nodes(data, i):
    """i should always start at the number of children index"""
    this_node = Node(next(id_giver), data=[])
    num_children = data[i]
    num_meta = data[i+1]

    i += 2

    for _ in range(num_children):
        child_node, i = add_nodes(data, i)
        child_node.parent = this_node

    for _ in range(num_meta):
        this_node.data.append(data[i])
        i += 1

    return this_node, i


def id_gen():
    num = 1
    while True:
        yield num
        num += 1


def get_node_value(node: Node):
    if len(node.children) == 0:
        return sum(node.data)

    else:
        total = 0
        for i in node.data:
            adjusted_index = i - 1
            if adjusted_index < len(node.children):
                total += get_node_value(node.children[adjusted_index])
        return total

def main():
    data = get_input()
    node, i = add_nodes(data, 0)
    # print(RenderTree(node))
    total_data = 0
    for x in PreOrderIter(node):
        total_data += sum(x.data)
    print(total_data)    # Part 1 answer
    print(get_node_value(node))  # Part 2 answer


id_giver = id_gen()
main()

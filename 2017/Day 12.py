from collections import defaultdict


def get_input():
    ans = []
    with open('input.txt') as f:
        for line in f:
            left, right = line.split(' <-> ')
            left = int(left)
            right = right.split(', ')
            right = [int(x) for x in right]
            ans.append((left, right))
    return ans


def has_number_x(connections, visited, i, x):
    """Recurse through groups i and return if you ever see x"""
    i_subgroups = connections[i]
    if x in i_subgroups:
        return True
    else:
        for sub_i in i_subgroups:
            if sub_i not in visited:
                visited.add(sub_i)
                if has_number_x(connections, visited, sub_i, x):
                    return True
    return False


def create_connections(lines):
    """Creates a dict of relationships between pipes."""
    ans = defaultdict(set)
    for line in lines:
        a, connections = line
        for connection in connections:
            ans[a].add(connection)
            ans[connection].add(a)

    return ans


def count_program_size(connections, program_num):
    count = 0
    for num in connections:
        visited = set()
        if has_number_x(connections, visited, num, program_num):
            count += 1
    return count


def main():
    lines = get_input()
    connections = create_connections(lines)

    part_1 = count_program_size(connections, 0)
    print(part_1)

    groups = set()
    group_member = set()

    # Create a new group each time a key can't reach other nums
    for num in connections:
        # See if it is part of any other current groups
        for group in groups:
            visited = set()
            if has_number_x(connections, visited, group, num):
                group_member.add(num)

        # If not a group member, start a new group
        if num not in group_member and num not in groups:
            # Start a new group search
            groups.add(num)

    print(len(groups))  #Part 2 answer




main()

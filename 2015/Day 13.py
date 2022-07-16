from Functions import get_input
from collections import defaultdict
from itertools import permutations


def parse_line(line):
    line = line.replace('.', '')
    left, sitting_name = line.split(' happiness units by sitting next to ')
    name, remaining = left.split(' would ')
    if 'gain' in remaining:
        happy = int(remaining.replace('gain', ''))
    elif 'lose' in remaining:
        happy = -1 * int(remaining.replace('lose', ''))
    else:
        raise ValueError("No happiness or sadness only blackness.")
    return name, sitting_name, happy


def make_graph():
    lines = get_input('line')
    graph = defaultdict(dict)
    name_list = set()
    for line in lines:
        name, sitting_name, happy = parse_line(line)
        name_list.add(name)
        graph[name].update({sitting_name : happy})
    return graph, name_list


def get_total_happiness(name_list, graph):
    total_happiness = 0
    for a, b in zip(name_list, name_list[1:]):
        total_happiness += graph[a][b]
        total_happiness += graph[b][a]
    total_happiness += graph[name_list[0]][name_list[-1]]
    total_happiness += graph[name_list[-1]][name_list[0]]
    return total_happiness



def main():
    graph, all_names = make_graph()
    name_perms = permutations(all_names)
    best_name_list = ''
    best_happiness = 0
    for name_list in name_perms:
        happy = get_total_happiness(name_list, graph)
        if happy > best_happiness:
            best_happiness = happy
            best_name_list = name_list
    print(f"Part 1 Best name list:")
    print(best_name_list)
    print(f"Total Happiness: {best_happiness}")
    print()

    # Part 2
    graph['me'] = dict()
    for name in all_names:
        graph['me'].update({name: 0})
        graph[name].update({'me': 0})
    all_names.add('me')


    name_perms = permutations(all_names)
    best_name_list = ''
    best_happiness = 0
    for name_list in name_perms:
        happy = get_total_happiness(name_list, graph)
        if happy > best_happiness:
            best_happiness = happy
            best_name_list = name_list
    print(f"Part 2 Best name list:")
    print(best_name_list)
    print(f"Total Happiness: {best_happiness}")


main()

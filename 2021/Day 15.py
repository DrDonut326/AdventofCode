from Grids import DictGrid
from Functions import get_input


def wrap_increment(x):
    x += 1
    if x > 9:
        x = 1
    return x


def bigger_row(cave_input):
    """Takes in a block and returns that block x 5 cave logic"""
    ans = []
    for line in cave_input:
        # Ans line is the final super copy of an individual row
        ans_line = line.copy()

        # Mutate each line 4 more times
        next_line = line.copy()
        for _ in range(4):
            next_line = list(map(wrap_increment, next_line))
            for num in next_line:
                ans_line.append(num)

        ans.append(ans_line)
    return ans


def increase_single_cave(cave):
    ans = []
    for line in cave:
        ans.append(list(map(wrap_increment, line)))

    return ans





def biggify_cave(cave_input):
    new_cave = []


    for _ in range(5):
        # Add the row copy
        new_cave.append(bigger_row(cave_input))

        # Make the cave input larger
        cave_input = increase_single_cave(cave_input)


    final_ans = []
    for row in new_cave:
        for r in row:
            final_ans.append(r)


    return final_ans



def main():
    cave_input = get_input('line', int_split=True)

    # Part 2
    cave_input = biggify_cave(cave_input)

    graph = DictGrid(int)
    graph.add_2D_array_to_grid(cave_input)
    start = graph.make_pos_from_x_y(0, 0)

    # Get bottom right
    min_max = graph.get_graph_min_max()

    finish = graph.make_pos_from_x_y(min_max[1], min_max[3])
    shorest_path = graph.dijkstra(start, finish)
    print(shorest_path)

main()

def get_data():
    ans = []
    with open("input.txt") as f:
        for line in f:
            line = line.rstrip()
            for element in line:
                ans.append(int(element))
    return ans


def get_layers(data, w, h):
    ans = dict()
    layer_level = 0
    i = 0
    length = len(data)
    while i < length:
        layer = []
        # Get width pixels height times
        for a in range(h):
            row = []
            for b in range(w):
                row.append(data[i])
                i += 1
            layer.append(row)
        ans[layer_level] = layer
        layer_level += 1
    return ans


def count_num(n, layer):
    """Returns how many times n occurs in the given layer."""
    total = 0
    for row in layer:
        for element in row:
            if element == n:
                total += 1
    return total


def find_layer_with_fewest_x(layers, x):
    least = None
    best_layer = None
    for layer in layers.values():
        num_x = count_num(x, layer)
        if least is None or num_x < least:
            least = num_x
            best_layer = layer
    return best_layer


def find_first_non_2_at_x_y(layers, x, y):
    # Work from the front (first) to the back (last)
    for layer in layers.values():
        if layer[y][x] != 2:
            return layer[y][x]


def build_master_layer(layers):
    ans = []
    sample_layer = layers[1]
    for y, row in enumerate(sample_layer):
        ans_row = []
        for x, element in enumerate(row):
            ans_row.append(find_first_non_2_at_x_y(layers, x, y))
        ans.append(ans_row)
    return ans


def part_1(layers):
    smallest_zero_layer = find_layer_with_fewest_x(layers, 0)
    num_ones = count_num(1, smallest_zero_layer)
    num_twos = count_num(2, smallest_zero_layer)
    print(num_ones * num_twos)


def part_2(layers):
    master_layer = build_master_layer(layers)
    for row in master_layer:
        for element in row:
            if element == 1:
                print('*', end='')
            else:
                print(' ', end='')
        print()



def main():
    im_width = 25
    im_height = 6
    data = get_data()
    layers = get_layers(data, im_width, im_height)
    part_1(layers)
    part_2(layers)

main()

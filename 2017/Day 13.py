from dataclasses import dataclass




@dataclass
class Layer:
    depth: int
    range: int












def get_input():
    ans = dict()
    with open('input.txt') as f:
        for line in f:
            left, right = line.split(': ')
            l = Layer(int(left), int(right))
            ans[l.depth] = l
    return ans


def stream_runner_caught(layers, delay):
    """Returns if the runner was ever caught."""
    risk = 0
    max_num = max(layers.values(), key=lambda x: x.depth).depth
    for depth in range(max_num + 1):
        if depth in layers:
            # Range * 2 - -2
            r = layers[depth].range
            if (depth + delay) == 0 or (depth + delay) % (r * 2 - 2) == 0:
                return True
    return False


def stream_runner(layers, delay):
    risk = 0
    max_num = max(layers.values(), key=lambda x: x.depth).depth
    for depth in range(max_num + 1):
        if depth in layers:
            # Range * 2 - -2
            r = layers[depth].range
            if (depth + delay) == 0 or (depth + delay) % (r * 2 - 2) == 0:
                risk += depth * r
    return risk

def main():
    layers = get_input()
    delay = 0
    print(stream_runner(layers, delay))  # Part 1 answer

    while stream_runner_caught(layers, delay):
        delay += 1

    print(delay)  # Part 2 answer






main()

class Bot:
    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius

    def __repr__(self):
        return f"{self.pos}|{self.radius}"

    def is_x_in_range(self, x):
        # Get manhat distance between these two
        manhat = get_manhat_distance(self, x)

        # If equal to or greater than signal range, yes!
        return self.radius >= manhat

    def is_pos_in_range(self, pos):
        manhat = get_manhat_pos(self.pos, pos)
        return self.radius >= manhat


def get_nano_bots():
    bots = []
    with open("input.txt") as f:
        for line in f:
            line = line.rstrip()
            left, right = line.split(', ')
            left = left.replace('pos=<', '')
            left = left.replace('>', '')

            radius = int(right[2:])

            x, y, z = [int(q) for q in left.split(',')]

            bot = Bot((x, y, z), radius)
            bots.append(bot)
    return bots


def get_manhat_distance(a: Bot, b: Bot):
    return abs(a.pos[0] - b.pos[0]) + abs(a.pos[1] - b.pos[1]) + abs(a.pos[2] - b.pos[2])


def get_manhat_pos(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def how_many_bots_in_range(bot: Bot, bots):
    """Returns how many bots including itself are in range."""
    count = 0
    for b in bots:
        if bot.is_x_in_range(b):
            count += 1
    return count


def how_many_bots_in_range_pos(pos, bots):
    count = 0
    for b in bots:
        if b.is_pos_in_range(pos):
            count += 1
    return count


def get_minmax(bots):
    x_min = min(bots, key=lambda x: x.pos[0]).pos[0]
    x_max = max(bots, key=lambda x: x.pos[0]).pos[0]

    y_min = min(bots, key=lambda x: x.pos[1]).pos[1]
    y_max = max(bots, key=lambda x: x.pos[1]).pos[1]

    z_min = min(bots, key=lambda x: x.pos[2]).pos[2]
    z_max = max(bots, key=lambda x: x.pos[2]).pos[2]

    return x_min, x_max, y_min, y_max, z_min, z_max


def bin_search_x(min_val, max_val, start_pos, bots):
    x, y, z = start_pos

    for _ in range(6):
        # Test lower bound
        x = min_val
        min_bound = how_many_bots_in_range_pos((x, y, z), bots)

        # Test upper bound
        x = max_val
        max_bound =how_many_bots_in_range_pos((x, y, z), bots)

        # If lower is better, keep lower and make upper bound halfway between
        if min_bound >= max_bound:
            max_bound = (min_bound + max_bound) // 2

        # If upper is better, keep upper and make lower bound halfway
        else:
            min_bound = (min_bound + max_bound) // 2

        return x

def part_2(bots):
    # Get the min and max for each value
    x_min, x_max, y_min, y_max, z_min, z_max = get_minmax(bots)

    # Find average as starting point
    x_average = x_min + x_max // 2
    y_average = y_min + y_max // 2
    z_average = z_min + z_max // 2

    best = how_many_bots_in_range_pos((x_average, y_average, z_average), bots)
    print(best)
    best_x = x_average

    # Divide the x range into 100 equal parts
    x_dist = (x_max - x_min) // 100
    x = x_min
    for _ in range(100):
        x += x_dist
        result = how_many_bots_in_range_pos((x, y_average, z_average), bots)
        if result > best:
            best_x = x
    print(best)



def part_1(bots):
    prime_bot = max(bots, key=lambda x: x.radius)
    print(how_many_bots_in_range(prime_bot, bots))


def main():
    bots = get_nano_bots()
    part_1(bots)

    pos = (0, 0, 0)
    part_2(bots)


main()

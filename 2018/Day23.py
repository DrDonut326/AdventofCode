from Utility.Pathfinding import PriorityQueue


class Bot:
    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius

    def can_this_bot_broadcast_to_this_pos(self, pos):
        return manhattan_distance(self.pos, pos) <= self.radius


class OctBox:
    """Used for Oct-Tree searching."""
    def __init__(self, pos, size):
        self.min_pos = pos
        self.max_pos = (pos[0] + size, pos[1] + size, pos[2] + size)
        self.center = (pos[0] + size // 2, pos[1] + size // 2, pos[2] + size // 2)
        self.size = size

    def __lt__(self, other):  # In case there's an omega-tie and we need to compare two box objects.
        return self

    def subdivide(self):
        """Returns a list of positions that mark the min of an octbox."""
        half = self.size // 2

        ans = []

        p = self.min_pos

        # Bottom Back Left
        pos = p
        ans.append(pos)

        # Bottom Front Left
        pos = (p[0], p[1], p[2] + half)
        ans.append(pos)

        # Top Back Left
        pos = (p[0], p[1] + half, p[2])
        ans.append(pos)

        # Top Front Left
        pos = (p[0], p[1] + half, p[2] + half)
        ans.append(pos)

        # Bottom Back Right
        pos = (p[0] + half, p[1], p[2])
        ans.append(pos)

        # Bottom Front Right
        pos = (p[0] + half, p[1], p[2] + half)
        ans.append(pos)

        # Top Back Right
        pos = (p[0] + half, p[1] + half, p[2])
        ans.append(pos)

        # Top Front Right
        pos = (p[0] + half, p[1] + half, p[2] + half)
        ans.append(pos)

        return ans

    def get_corners(self):
        """Returns a list of positions of the corners of this box."""
        half = self.size

        ans = []

        p = self.min_pos

        # Bottom Back Left
        pos = p
        ans.append(pos)

        # Bottom Front Left
        pos = (p[0], p[1], p[2] + half)
        ans.append(pos)

        # Top Back Left
        pos = (p[0], p[1] + half, p[2])
        ans.append(pos)

        # Top Front Left
        pos = (p[0], p[1] + half, p[2] + half)
        ans.append(pos)

        # Bottom Back Right
        pos = (p[0] + half, p[1], p[2])
        ans.append(pos)

        # Bottom Front Right
        pos = (p[0] + half, p[1], p[2] + half)
        ans.append(pos)

        # Top Back Right
        pos = (p[0] + half, p[1] + half, p[2])
        ans.append(pos)

        # Top Front Right
        pos = (p[0] + half, p[1] + half, p[2] + half)
        ans.append(pos)

        return ans

    def does_a_bot_intersect_this_box(self, bot: Bot):
        """Returns true if a bot can hit one of the corners."""
        corners = self.get_corners()
        for corner in corners:
            if bot.can_this_bot_broadcast_to_this_pos(corner):
                return True
        return False


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


def part_1(bots):
    # Find bot with the largest signal radius
    big_boi = max(bots, key=lambda x: x.radius)

    # How many in range that bot?
    can_broadcast_to = [x for x in bots if big_boi.can_this_bot_broadcast_to_this_pos(x.pos)]

    print(len(can_broadcast_to))


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def get_bounds_for_box(bots: list[Bot]):
    min_x = min([z.pos[0] for z in bots])
    min_y = min([z.pos[1] for z in bots])
    min_z = min([z.pos[2] for z in bots])

    max_x = max([z.pos[0] for z in bots])
    max_y = max([z.pos[1] for z in bots])
    max_z = max([z.pos[2] for z in bots])

    return min_x, max_x, min_y, max_y, min_z, max_z


def are_all_bots_inside_this_box(bots, box):
    for bot in bots:
        if not box.min_pos[0] <= bot.pos[0] <= box.max_pos[0]:
            return False
        if not box.min_pos[1] <= bot.pos[1] <= box.max_pos[1]:
            return False
        if not box.min_pos[2] <= bot.pos[2] <= box.max_pos[2]:
            return False
    return True


def create_initial_box(bots: list[Bot]):
    """Creates a bounding octbox in growing powers of two until it encompasses all bots."""
    # Get inital bounds
    min_x, max_x, min_y, max_y, min_z, max_z = get_bounds_for_box(bots)

    box = OctBox((min_x, min_y, min_z), 2)
    while not are_all_bots_inside_this_box(bots, box):
        box = OctBox((min_x, min_y, min_z), box.size * 2)
    return box


def how_many_bots_in_range_of_this_box(bots: list[Bot], box: OctBox):
    count = 0
    for bot in bots:
        if box.does_a_bot_intersect_this_box(bot):
            count += 1
    return count


def how_many_bots_reach_this_position(bots: list[Bot], pos: tuple[int, int, int]):
    count = 0
    for bot in bots:
        if bot.can_this_bot_broadcast_to_this_pos(pos):
            count += 1
    return count


def get_best_corner(box: OctBox, bots: list[Bot]):
    """Gets the corner with the highest bot count.  Ties broken by how close to origin."""
    best_count = None
    best_corner = None
    for corner in box.get_corners():
        score = how_many_bots_reach_this_position(bots, corner)
        if best_count is None or score > best_count:
            best_count = score
            best_corner = corner

        elif score == best_count:
            current_best = manhattan_distance(best_corner, (0, 0, 0))
            if manhattan_distance(corner, (0, 0, 0)) < current_best:
                best_corner = corner

    return best_corner, best_count


def find_pos_in_range_with_most_bots(box: OctBox, bots: list[Bot]):
    # Create priority queue
    q = PriorityQueue()
    q.put(box, 0)

    # Setup variables to use in disgarding un-needed boxes later on
    current_best_count = None
    answer_pos_set = set()

    # While there are still boxes to search
    while not q.empty():
        # Get next box
        current: OctBox
        current = q.get()

        # If you find a 1x1x1 cube, set the limiting conditions and record possible answers
        if current.size == 1:
            best_corner_pos, best_count = get_best_corner(current, bots)

            # If this box is completely better, wipe old answers
            if current_best_count is None or best_count > current_best_count:
                current_best_count = best_count
                answer_pos_set.clear()
                answer_pos_set.add(best_corner_pos)

            # If tied, add it to the set
            elif current_best_count == best_count:
                answer_pos_set.add(best_corner_pos)

        # Disgard any boxes with a count less than the best count (if exists
        elif current_best_count is not None and how_many_bots_in_range_of_this_box(bots, current) < current_best_count:
            pass
        else:
            # Subdivide the box into positions
            pos_list = current.subdivide()

            # Create new boxes
            for pos in pos_list:
                new_box = OctBox(pos, current.size // 2)

                # Get how many bots are hitting the corners of this box
                in_range = how_many_bots_in_range_of_this_box(bots, new_box)

                # Get box's distance to origin
                to_origin = manhattan_distance(new_box.center, (0, 0, 0))

                # New box size
                new_size = new_box.size

                # Make priority tuple
                priority = (-in_range, to_origin, -new_size)

                # Add to queue
                q.put(new_box, priority)

    return answer_pos_set


def part_2(bots: list[Bot]):
    box = create_initial_box(bots)
    result = find_pos_in_range_with_most_bots(box, bots)
    print(sum(list(result)[0]))


def main():
    bots = get_nano_bots()
    part_1(bots)
    part_2(bots)


main()

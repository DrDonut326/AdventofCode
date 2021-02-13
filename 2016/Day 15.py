class Disc:
    def __init__(self, total_positions, starting_position):
        self.total_positions = total_positions
        self.starting_position = starting_position

    def get_position(self, time):
        return (self.starting_position + time) % self.total_positions

    def is_disc_clear(self, time):
        return self.get_position(time) == 0


def are_all_discs_clear(discs, time):
    for i, d in enumerate(discs):
        if not d.is_disc_clear(time + i + 1):
            return False
    return True


def main():
    discs = [Disc(13, 11), Disc(5, 0), Disc(17, 11), Disc(3, 0), Disc(7, 2), Disc(19, 17), Disc(11, 0)]
    time = 0
    result = are_all_discs_clear(discs, time)
    while not result:
        time += 1
        result = are_all_discs_clear(discs, time)
    print(time)

if __name__ == '__main__':
    main()

from collections import defaultdict


class Bus:
    """Data container class for the busses"""
    def __init__(self, value, index):
        self.value = value
        self.index = index

    def am_I_here(self, time):
        """Checks to see if the bus has 'arrived' for a particular time"""
        return time % self.value == 0


def get_busses():
    """Grabs all the busses from a textfile and converts them to Bus Objects"""
    ans = []
    with open("kodict_entry.txt") as f:
        line = f.readline().rstrip()
        line = line.split(',')
        for z in line:
            if z == 'x':
                ans.append(z)
            else:
                ans.append(int(z))
    busses = []
    for i, z in enumerate(ans):
        if z == 'x':
            busses.append('x')
        else:
            busses.append(Bus(z, i))
    return busses


def check_ans(busses, time):
    """Checks to see if there is a valid answer"""
    for i, bus in enumerate(busses):
        if bus != 'x' and not bus.am_I_here(time + i):
            return False
    return True

def how_many_correct_answers(busses, time):
    """Checks how many busses in a row are in the
    correct position for the given timestamp"""
    ans = 0
    for i, bus in enumerate(busses):
        if bus != 'x' and not bus.am_I_here(time + i):
            return ans
        else:
            if bus != 'x':
                ans += 1
    raise ValueError("If we got here, we found the answer but somehow missed it.")


def check_timeskip(busses, time, skip_dict, timeskip):
    """Checks to see if our timeskip can be increased to a larger size
    Exploits the idea that all valid answer will be equal distances apart.
    So we can use the distances between partial answers to slowly
    decrease the search space."""
    # Check how many answers are currently valid
    num_correct = how_many_correct_answers(busses, time)

    # If zero, don't need to change anything
    if num_correct == 0:
        return timeskip

    # If not, add it to the skip dictionary
    # Todo: Make this section only check once
    # Skip_dict contains a list of timestamps for each number of valid positions
    skip_dict[num_correct].append(time)

    # If the list is larger than two, find the distance between the two
    # valid answers, and update the timeskip number if it is bigger
    if len(skip_dict[num_correct]) > 1:
        t = skip_dict[num_correct][-1] - skip_dict[num_correct][-2]
        if t > timeskip:
            timeskip = t
    return timeskip



def main():
    # Setup stuff
    time = 0
    timeskip = 1
    skip_dict = defaultdict(list)
    busses = get_busses()
    while not check_ans(busses, time):
        # Not the right answer yet, so check to see if we can
        # update the timeskip before incrementing
        timeskip = check_timeskip(busses, time, skip_dict, timeskip)
        # Update our current time
        time += timeskip

    # Answer has been found so print it out.
    print(time)
    print(skip_dict.items())


main()

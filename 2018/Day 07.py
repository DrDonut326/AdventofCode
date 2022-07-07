from collections import defaultdict
from string import ascii_uppercase


class Step:
    def __init__(self, name, finished=False):
        self.name = name
        self.finished = finished
        self.working = False
        self.requirements = []

    def available(self):
        """Returns if this step is available or not."""
        # If I am done, not ready
        if self.finished or self.working:
            return False

        # If all my requirements are finished, them I'm available
        for r in self.requirements:
            if not r.finished:
                return False
        return True


def get_steps():
    # Get a set of all letters
    letters = set()
    with open("input.txt") as f:
        for line in f:
            line = line.rstrip()
            line = line.replace(' must be finished before step', '')
            line = line.replace('Step ', '')
            line = line.replace(' can begin.', '')
            a, b = line.split(' ')
            letters.add(a)
            letters.add(b)

    # Create step objects without requirements
    steps = dict()
    for letter in letters:
        steps[letter] = Step(letter)

    # Add in requirements
    with open("input.txt") as f:
        for line in f:
            line = line.rstrip()
            line = line.replace(' must be finished before step', '')
            line = line.replace('Step ', '')
            line = line.replace(' can begin.', '')
            a, b = line.split(' ')
            # a must be finished before b can begin
            # so a is a requirement of b
            steps[b].requirements.append(steps[a])

    return steps


def find_root(steps):
    for key in steps:
        if not steps[key].requirements:
            return key


def get_order(steps: dict):
    done = []
    while len(done) < len(steps):
        # Get the next available list
        avail_list = [x for x in steps.values() if x.available()]

        # Sort by alpha
        avail_list.sort(key=lambda x: x.name)

        # Get first one
        step = avail_list[0]

        # Change to done
        step.finished = True
        done.append(step.name)

    return ''.join(done)


def get_finish_time():
    steps = get_steps()
    time = -1
    letter_values = dict()
    for letter in ascii_uppercase:
        letter_values[letter] = ord(letter) - 64

    finished = []
    workers_avail = 5  # Change to 5 workers when not testing
    working = defaultdict(int)
    while len(finished) < len(steps):
        # Increment time
        time += 1

        # Increment any existing projects
        for letter in working:
            working[letter] -= 1
            # Check if any projects finished
            if working[letter] == 0:
                # Job done, mark in steps and workers
                workers_avail += 1
                steps[letter].finished = True
                finished.append(letter)

        # Remove any finished projects
        if len(working) > 0:
            working = {key: val for key, val in working.items() if val != 0}

        # Get the next available list
        avail_list = [x for x in steps.values() if x.available()]

        # Sort by alpha
        avail_list.sort(key=lambda x: x.name)

        # See if anyone is available to work
        while workers_avail > 0 and len(avail_list) > 0:

            # Get first one
            step = avail_list.pop(0)

            # Put into the working dict with a second already done (59 + letter value)
            working[step.name] = 60 + letter_values[step.name] #Change 0 to 60 when not testing!
            step.working = True

            # Decrement avail workers
            workers_avail -= 1

    return time


def main():
    steps = get_steps()
    order = get_order(steps)
    print(order)  # Part 1 answer
    time = get_finish_time()
    print(time)   # Part 2 answer


main()

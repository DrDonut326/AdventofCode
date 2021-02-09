from Utility import get_input
from collections import defaultdict


class Bot:
    def __init__(self):
        self.id = None
        self.lowgive_type = None
        self.highgive_type = None
        self.givelow = None
        self.givehigh = None
        self.values = []
        self.allbots = None
        self.outputs = None
        self.done = False

    def info(self):
        print(f"Bot #: {self.id} // Values stored: {self.values}")
        print(f"Giving low to {self.lowgive_type} {self.givelow}")
        print(f"Giving high to {self.highgive_type} {self.givehigh}")
        print()

    def get_num(self, n):
        self.values.append(n)
        if len(self.values) == 2:
            self.high = max(self.values)
            self.low = min(self.values)
            # Give to another bot

    def update(self):
        """Returns False if it hasn't done its job yet"""
        if not self.done:
            if len(self.values) == 2:
                if 61 in self.values and 17 in self.values:
                    print(f"Part 1 answer = {self.id}")
                self.done = True
                # Give low
                if self.lowgive_type == 'bot':
                    self.allbots[self.givelow].values.append(min(self.values))
                else:
                    self.outputs[self.givelow] = min(self.values)
                # Give high
                if self.highgive_type == 'bot':
                    self.allbots[self.givehigh].values.append(max(self.values))
                else:
                    self.outputs[self.givehigh] = max(self.values)
        return self.done


def build_bots(allbots, outputs):
    data = get_input('line')

    for line in data:
        if line.startswith('value'):
            val, bot_id = [int(x) for x in line[5:].split(' goes to bot ')]
            allbots[bot_id].id = bot_id
            allbots[bot_id].values.append(val)
            allbots[bot_id].outputs = outputs
        else:
            line = line.split(' ')
            bot_id = int(line[1])
            # Check lowgive
            if line[5] == 'bot':
                # bot
                lowgive_type = 'bot'
            else:
                # output
                lowgive_type = 'output'
            lowgive_id = int(line[6])

            # Check highgive
            if line[10] == 'bot':
                highgive_type = 'bot'
            else:
                highgive_type = 'output'
            highgive_id = int(line[-1])

            allbots[bot_id].id = bot_id
            allbots[bot_id].lowgive_type = lowgive_type
            allbots[bot_id].highgive_type = highgive_type
            allbots[bot_id].givelow = lowgive_id
            allbots[bot_id].givehigh = highgive_id
            allbots[bot_id].outputs = outputs

    for b in allbots.values():
        b.allbots = allbots
        b.outputs = outputs


def update_till_finished(allbots):
    done = False
    while not done:
        done = True
        for b in allbots.values():
            result = b.update()
            if not result:
                done = False


def main():
    allbots = defaultdict(Bot)
    outputs = defaultdict(int)
    build_bots(allbots, outputs)
    update_till_finished(allbots)
    print(f"Part 2 answer = {outputs[0] * outputs[1] * outputs[2]}")


if __name__ == '__main__':
    main()

from Functions import get_input
from collections import defaultdict

class Sue:
    def __init__(self, name, data):
        self.name = name
        self.data = data

    def get_score(self, clue):
        score = 0
        for key in clue:
            if key in self.data and self.data[key] == clue[key]:
                score += 1
        return score

    def get_score_2(self, clue):
        score = 0
        for key in clue:
            if key in self.data:
                if key == 'cats' or key == 'trees':
                    if self.data[key] > clue[key]:
                        score += 1
                elif key == 'pomeranians' or key == 'goldfish':
                    if self.data[key] < clue[key]:
                        score += 1
                else:
                    if self.data[key] == clue[key]:
                        score += 1
        return score


def get_sues():
    ans = []
    lines = get_input('line')
    for line in lines:
        i = line.index(':')
        name = line[:i]
        line = line[i + 2:]
        line = line.replace(' ', '')
        attributes = line.split(',')
        att_dict = dict()
        for attribute in attributes:
            key, value = attribute.split(':')
            att_dict.update({key: int(value)})
        ans.append(Sue(name, att_dict))
    return ans


def main():
    sues = get_sues()
    clue = {
        'children': 3,
        'cats': 7,
        'samoyeds': 2,
        'pomeranians': 3,
        'akitas': 0,
        'vizslas': 0,
        'goldfish': 5,
        'trees': 3,
        'cars': 2,
        'perfumes': 1
    }
    best = 0
    best_sue = ''
    best2 = 0
    best_sue2 = ''
    for sue in sues:
        # Part 1
        score = sue.get_score(clue)
        if score > best:
            best = score
            best_sue = sue.name

        # Part 2
        score2 = sue.get_score_2(clue)
        if score2 > best2:
            best2 = score2
            best_sue2 = sue.name

    print(f"Part 1 answer = {best_sue}")
    print(f"Part 2 answer = {best_sue2}")


main()

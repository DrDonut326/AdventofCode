from Functions import get_input
from collections import defaultdict


class Anagramize:
    def __init__(self, word):
        self.word = word
        self.counts = defaultdict(int)
        self.count_letters()

    def count_letters(self):
        for letter in self.word:
            self.counts[letter] += 1

    def get_key(self):
        # Get letter list and sort it
        letter_list = list(self.counts.keys())
        letter_list.sort()

        # Build the key
        key = ''
        for letter in letter_list:
            key += letter + str(self.counts[letter])
        return key


def part_1(phrases):
    count = 0
    for phrase in phrases:
        if len(set(phrase)) == len(phrase):
            count += 1
    print(count)


def part_2(phrases):
    count = 0
    for phrase in phrases:
        anagrams_group = set()
        for word in phrase:
            anagram = Anagramize(word)
            anagrams_group.add(anagram.get_key())
        if len(anagrams_group) == len(phrase):
            count += 1
    print(count)


def main():
    phrases = get_input('line', do_split=True,split_key=' ')
    part_1(phrases)
    part_2(phrases)


main()

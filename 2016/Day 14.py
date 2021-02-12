from collections import defaultdict
from hashlib import md5


class Hkey:
    """Data class for Hkeys. Length is 3 or 5 (triple or quint)"""
    def __init__(self, length, index, char, hash_string):
        self.length = length
        self.index = index
        self.char = char
        self.hash_string = hash_string


def get_bytes(s):
    """Convert a string into bytes for hash input"""
    return bytes(s, 'utf-8')


def get_hash():
    """Generate hashes based on the input salt"""
    salt = 'yjdafjpo'
    index = 0
    while True:
        yield md5(get_bytes(salt + str(index))).hexdigest(), index
        index += 1


def get_stretched_hash():
    """Generate hashes with 2016 stretches"""
    salt = 'yjdafjpo'
    index = 0
    while True:
        md_hash = md5(get_bytes(salt + str(index))).hexdigest()
        # Repeatedly Hash the hash
        for _ in range(2016):
            md_hash = md5(get_bytes(md_hash)).hexdigest()
        yield md_hash, index
        index += 1


def does_string_have_triples(s):
    """Sees if a string has a run of 3"""
    for a, b, c in zip(s, s[1:], s[2:]):
        if a == b == c:
            return True, a
    return False, -1


def does_string_have_quints(s):
    """Sees if a string has a run of 5"""
    for a, b, c, d, e in zip(s, s[1:], s[2:], s[3:], s[4:]):
        if a == b == c == d == e:
            return True, a
    return False, -1


def get_next_triple_or_quint(part):
    """Returns the next hkey that has triples or quints in it"""
    if part == 'part2':
        hash_gen = get_stretched_hash()
    else:
        hash_gen = get_hash()
    while True:
        # Get the next hash
        hash_string, index = next(hash_gen)
        # Add the triple or quint to the matching dict
        result, char = does_string_have_quints(hash_string)
        if result:
            hkey = Hkey(5, index, char, hash_string)
            yield hkey
        else:
            result, char = does_string_have_triples(hash_string)
            if result:
                hkey = Hkey(3, index, char, hash_string)
                yield hkey


def check_triples(triples, tq, found, ans_list):
    """Updates the answer list and found set with valid triples"""
    ans = []
    for c in triples[tq.char]:
        if c >= tq.index - 1000:
            if c not in found:
                ans_list.append(c)
                found.add(c)


def part1():
    tq_gen = get_next_triple_or_quint('part1')
    found = set()
    ans_list = []
    triples = defaultdict(set)
    quints = defaultdict(set)
    while len(ans_list) < 64:
        tq = next(tq_gen)
        if tq.length == 5:
            quints[tq.char].add(tq.index)
            check_triples(triples, tq, found, ans_list)
            triples[tq.char].add(tq.index)
        elif tq.length == 3:
            triples[tq.char].add(tq.index)

    ans_list.sort()
    print(f"Part 1 answer = {ans_list[-1]}")


def part2():
    tq_gen = get_next_triple_or_quint('part2')
    found = set()
    ans_list = []
    triples = defaultdict(set)
    quints = defaultdict(set)
    while len(ans_list) < 80:
        tq = next(tq_gen)
        if tq.length == 5:
            quints[tq.char].add(tq.index)
            check_triples(triples, tq, found, ans_list)
            triples[tq.char].add(tq.index)
        elif tq.length == 3:
            triples[tq.char].add(tq.index)

    ans_list.sort()
    print(f"Part 2 answer = {ans_list[63]}")


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()

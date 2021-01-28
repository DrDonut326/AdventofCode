from GetInput import get_input


def has_at_least_3_vowels(s):
    vowels = 'aeiou'
    count = 0
    for letter in s:
        if letter in vowels:
            count += 1
    return count >= 3


def has_2_in_a_row(s):
    for a, b in zip(s, s[1:]):
        if a == b:
            return True
    return False


def has_no_special(s):
    bad = ['ab', 'cd', 'pq', 'xy']
    for b in bad:
        if b in s:
            return False
    return True


def has_sandwich(s):
    for a, b, c in zip(s, s[1:], s[2:]):
        if a == c and b != a:
            return True
    return False


def has_pair(s):
    for a, b in zip(s, s[1:]):
        ab = a + b
        if s.count(ab) >= 2:
            return True
    return False





def main(part):
    strings = get_input('line')
    count = 0
    for s in strings:
        if part == 1:
            if has_no_special(s) and has_2_in_a_row(s) and has_at_least_3_vowels(s):
                count += 1
        else:
            # Part 2
            if has_sandwich(s) and has_pair(s):
                count += 1
    print(count)



main(2)

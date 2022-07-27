def do_always_increase(x):
    """Returns true if numbers in x always increase (to the right)"""
    s = str(x)
    for a, b in zip(s, s[1:]):
        if int(b) < int(a):
            return False
    return True


def has_doubled_digits(x):
    """Returns true if any adjacent digits are the same"""
    s = str(x)
    for a, b in zip(s, s[1:]):
        if a == b:
            return True
    return False


def find_possible_passwords():
    """Gets passwords matching part 1 criteria."""
    possible = []
    for x in range(367479, 893698 + 1):
        if do_always_increase(x):
            if has_doubled_digits(x):
                possible.append(x)
    return possible


def get_doubles(s):
    """Returns a set of digits that appear ajacent in the number"""
    ans = set()
    s = str(s)
    for a, b in zip(s, s[1:]):
        if a == b:
            ans.add(int(a))
    return ans

def get_trips(s):
    """Returns a set of digits that appear as triples in the number"""
    ans = set()
    s = str(s)
    for a, b, c in zip(s, s[1:], s[2:]):
        if a == b == c:
            ans.add(int(a))
    return ans


def find_more_possible_passwords():
    """Returns a list of numbers that match part 2 criteria."""
    ans = []
    possible = find_possible_passwords()
    for p in possible:
        # Get doubles
        doubles = get_doubles(p)
        # Get triples
        trips = get_trips(p)

        # Subtract any triples from the dubs
        good_dubs = doubles - trips
        if good_dubs:
            ans.append(p)

    return ans


def main():
    possible = find_possible_passwords()
    print(len(possible)) # Part 1
    more = find_more_possible_passwords()
    print(len(more))


main()

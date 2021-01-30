def build_next_number(s):
    # Break the number into arrays of same numbers
    splits = split_to_sames(s)
    ans = ''
    # Use the arrays to find out how many to add
    for split in splits:
        ans += str(len(split)) + split[0]
    return ans


def split_to_sames(s):
    """Returns a list of list
    Where each list is the same number
    Broken up from the input string"""
    if len(s) == 1:
        return [[s]]
    ans = []
    streak = []
    for a, b in zip(s, s[1:]):
        # Compare pairs
        if a == b:
            streak.append(a)
        else:
            streak.append(a)
            ans.append(streak)
            streak = []
    ans.append(streak)
    # What about the last one?
    if s[-1] == s[-2]:
        ans[-1].append(s[-1])
    else:
        ans[-1].append(s[-1])
    return ans


def main():
    # Put the puzzle input here
    input_num = '1113222113'

    for _ in range(40):
        input_num = build_next_number(input_num)
    print(f"Part 1 answer = {len(input_num)}")

    for _ in range(10):
        input_num = build_next_number(input_num)
    print(f"Part 2 answer = {len(input_num)}")


main()

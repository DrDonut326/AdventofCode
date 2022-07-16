from collections import defaultdict

from Functions import get_input


def get_answer(codes, part):
    """Returns the string made of the most common / least common character
    appearing in each position of the code words"""
    # Create a nested defaultdict to store the character position, and then each letter
    frequency_count = defaultdict(lambda: defaultdict(int))
    for code in codes:
        for i, letter in enumerate(code):
            frequency_count[i][letter] += 1
    ans = ''
    for i in range(len(codes[0])):
        # Get the max / min of the items() of the position
        # of each character in all the codes
        if part == 1:
            ans += max(frequency_count[i].items(), key=lambda x: x[1])[0]
        else:
            ans += min(frequency_count[i].items(), key=lambda x: x[1])[0]
    return ans


def main():
    codes = get_input('line')
    print(f"Part 1 answer = {get_answer(codes, 1)}")
    print(f"Part 2 answer = {get_answer(codes, 2)}")


main()

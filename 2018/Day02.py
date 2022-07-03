from Utility import get_input
from collections import defaultdict

def count_letters_in_string(x: str):
    count = defaultdict(int)
    for letter in x:
        count[letter] += 1
    return count


def has_two_of_any_letter(box_id: str):
    letter_count = count_letters_in_string(box_id)
    return 2 in letter_count.values()


def has_three_of_any_letter(box_id: str):
    letter_count = count_letters_in_string(box_id)
    return 3 in letter_count.values()


def has_one_difference(a: str, b: str):
    """Returns true if the two strings differ only by one."""
    error_count = 0
    for x, y in zip(a, b):
        if x != y:
            error_count += 1
            if error_count > 1:
                return False
    return True


def find_almost_same_pair(box_ids):
    for i, box_a in enumerate(box_ids):
        for j, box_b in enumerate(box_ids):
            if i != j:
                if has_one_difference(box_a, box_b):
                    return box_a, box_b


def remove_odd_one_out(same_pair):
    ans = ''
    for a, b in zip(same_pair[0], same_pair[1]):
        if a == b:
            ans += a
    return ans


def main():
    box_ids = get_input('line')
    num_3s = 0
    num_2s = 0

    for box in box_ids:
        if has_two_of_any_letter(box):
            num_2s += 1
        if has_three_of_any_letter(box):
            num_3s += 1

    print(num_3s * num_2s)  # Part 1 answer

    same_pair = find_almost_same_pair(box_ids)
    print(remove_odd_one_out(same_pair))  # Part 2 ans


main()

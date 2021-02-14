def generate_dragon(a):
    """Generates a modified dragon curve from the input string"""
    b = a
    b = b[::-1]
    b = flip_bits(b)
    return a + '0' + b


def get_dragon_curve_of_length_n(starting_string, n):
    result = generate_dragon(starting_string)
    while len(result) < n:
        result = generate_dragon(result)
    return result[:n]


def flip_bits(s):
    """Flips all bits in a string"""
    ans = ''
    for x in s:
        if x == '1':
            ans += '0'
        elif x == '0':
            ans += '1'
        else:
            raise ValueError("Not a 1 or 0 in input string.")
    return ans


def checksum_mini(s):
    """Iterates through pairs to get the intermediate steps of checksum calculation"""
    result = ''
    for a, b in zip(s[::2], s[1::2]):
        if a == b:
            result += '1'
        else:
            result += '0'
    return result


def calculate_checksum(s):
    """Returns the checksum of a modified dragon curve"""
    result = checksum_mini(s)
    while len(result) % 2 == 0:
        result = checksum_mini(result)
    return result


def main():
    initial_state = '11101000110010100'
    desired_length = 272
    dragon = get_dragon_curve_of_length_n(initial_state, desired_length)
    print(f"Part 1 answer = {calculate_checksum(dragon)}")
    desired_length = 35651584
    dragon = get_dragon_curve_of_length_n(initial_state, desired_length)
    print(f"Part 2 answer = {calculate_checksum(dragon)}")

if __name__ == '__main__':
    main()

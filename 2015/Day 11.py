def incremenet_password(password, nexts):
    ans = ''
    # Start with the last letter, and update it.
    # Only continue if you just updated a 'z'
    change = True
    for letter in password[::-1]:
        if change:
            t = nexts[letter]
            if t != 'a':
                change = False
            ans += t
        else:
            ans += letter

    # Reverse the password
    return ans[::-1]


def build_nexts():
    letters = 'abcdefghjkmnpqrstuvwxyz'
    nexts = dict()
    for a, b in zip(letters, letters[1:]):
        nexts[a] = b
    nexts[letters[-1]] = letters[0]

    # Special cases
    nexts['i'] = 'j'
    nexts['l'] = 'm'
    nexts['o'] = 'p'

    return nexts


def has_3_in_a_row(password):
    for a, b, c in zip(password, password[1:], password[2:]):
        if ord(b) == ord(a) + 1 and ord(c) == ord(a) + 2:
            return True
    return False


def has_2_pairs(password):
    count = 0
    searched = set()
    for a, b in zip(password, password[1:]):
        ab = a + b
        if ab not in searched and a == b:
            count += password.count(ab)
            searched.add(ab)
    return count >= 2


def has_no_bad_letters(password, bad):
    for letter in password:
        if letter in bad:
            return False
    return True


def fix_password(password, nexts):
    bad = ['i', 'l', 'o']
    ans = ''
    letters_left = len(password)
    for letter in password:
        if letter in password:
            if letter not in bad:
                ans += letter
                letters_left -= 1
            else:
                ans += nexts[letter]
                letters_left -= 1
                ans += 'a' * letters_left
                return ans
    return ans


def is_password_valid(password):
    return has_3_in_a_row(password) and has_2_pairs(password)


def main():
    # Dictionary of next letters for easy updating of passwords
    nexts = build_nexts()

    # Program input
    password = 'hxbxwxba'
    print(f"Starting password is {password}")

    # Fix any bad letters to not waste time
    password = fix_password(password, nexts)

    # Part 1
    while not is_password_valid(password):
        password = incremenet_password(password, nexts)
    print(f"Part 1 answer is: {password}")

    # Part 2
    password = incremenet_password(password, nexts)
    while not is_password_valid(password):
        password = incremenet_password(password, nexts)
    print(f"Part 2 answer is: {password}")


main()

from Functions import get_input




def part_1(code):
    i = 0
    count = 0

    while 0 <= i < len(code):
        # Get the jump value
        jump_value = code[i]

        # Increment the current space
        code[i] += 1

        # 'Jump' based on the jump value.  (change i)
        i = i + jump_value
        count += 1

        # Continue until you would jump outside the list

    return count


def part_2(code):
    i = 0
    count = 0

    while 0 <= i < len(code):
        # Get the jump value
        jump_value = code[i]

        # Increment the current space
        if jump_value >= 3:
            code[i] -= 1
        else:
            code[i] += 1

        # 'Jump' based on the jump value.  (change i)
        i = i + jump_value
        count += 1

        # Continue until you would jump outside the list

    return count


def main():
    code = get_input('line', int_convert=True)
    print(part_1(code))
    code = get_input('line', int_convert=True)
    print(part_2(code))


main()

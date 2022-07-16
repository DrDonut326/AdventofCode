from Functions import get_input


# Use ? for bad chars


def get_char_set(data):
    ans = set()
    for element in data:
        ans.add(element)
    return ans


def clean_chars(data):
    # Mark for termination
    for i, letter in enumerate(data):
        if letter == '!':
            data[i] = '?'
            data[i + 1] = '?'

    # Terminate
    while '?' in data:
        data.remove('?')


def standardize_garbage(data):
    """"Makes all garbage data '?'"""
    change = False
    for i, letter in enumerate(data):
        # If change is currently True, change things
        if change:
            # If We reach a closing string, turn off change
            if letter == '>':
                change = False
            else:
                data[i] = '?'                # TODO Count garbage later?
        else:
            # Change is False, check for start
            if letter == '<':
                change = True


def display_puzzle(data):
    print(''.join(data))


def count_groups(data):
    # Add to total every time a group is closed
    level = 0
    total = 0
    for letter in data:
        if letter == '{':
            level += 1

        elif letter == '}':
            total += level
            level -= 1
    return total





def main():
    puzzle = get_input('char')

    # Clean up data
    clean_chars(puzzle)
    standardize_garbage(puzzle)

    # Part 1
    score = count_groups(puzzle)
    print(score)

    # Part 2
    print(puzzle.count('?'))



main()

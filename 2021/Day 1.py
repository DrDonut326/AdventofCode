from token import NAME

from Functions import get_input


def main():
    input = get_input('line', int_convert=True)
    compare = input.pop(0)
    count = 0
    for x in input:
        if x > compare:
            count += 1
        compare = x
    print(count)


main()
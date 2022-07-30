from IntcodeComp import IntcodeComputer


def get_codes():
    ans = []
    with open("input.txt") as f:
        for line in f:
            line = line.rstrip().split(',')
            for element in line:
                ans.append(int(element))
    return ans


def inputer():
    return 5


def main():
    codes = get_codes()
    comp = IntcodeComputer(codes, inputer)
    comp.execute_codes()
    print(comp.outputs)


main()

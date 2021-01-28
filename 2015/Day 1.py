def get_input():
    with open("input.txt") as f:
        ans = []
        for line in f:
            line = line.rstrip()
            for c in line:
                ans.append(c)
    return ans


def main(part):
    commands = get_input()
    floor = 0
    com_dict = {'(': 1, ')':-1}
    if part == 1:
        for command in commands:
            floor += com_dict[command]
        print(f"The answer is {floor}.")
    else:
        for i, command in enumerate(commands):
            floor += com_dict[command]
            if floor == -1:
                print(f"The answer to part 2 is: {i + 1}.")
                break

# 1 for part 1
# 2 for part 2
main(2)

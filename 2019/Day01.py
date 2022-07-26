def get_input():
    ans = []
    with open('input.txt') as f:
        for line in f:
            ans.append(int(line.rstrip()))
    return ans


def find_module_fuel(weight):
    return weight // 3 - 2


def really_find_module_fuel(weight, total=0):
    # Recurse until the fuel value is zero or less
    fuel = find_module_fuel(weight)
    if fuel <= 0:
        return total
    else:
        # Treat fuel as the new input and add it to the total
        return really_find_module_fuel(fuel, total+fuel)


def part_1():
    total = 0
    for module in get_input():
        total += find_module_fuel(module)
    print(total)


def part_2():
    total = 0
    for module in get_input():
        total += really_find_module_fuel(module, 0)
    print(total)


def main():
    part_1()
    part_2()


main()

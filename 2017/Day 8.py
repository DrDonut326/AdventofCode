from math import inf


class Code:
    def __init__(self, register, direction, value, a, condition, b):
        self.register = register
        self.direction = direction
        self.value = int(value)
        self.a = a
        self.condition = condition
        self.b = int(b)

    def check_condition(self, registers):
        # {'<=', '<', '==', '>', '!=', '>='}
        c = self.condition

        # <=
        if c == '<=':
            return registers[self.a] <= self.b

        # <
        if c == '<':
            return registers[self.a] < self.b

        # ==
        if c == '==':
            return registers[self.a] == self.b

        # >
        if c == '>':
            return registers[self.a] > self.b

        # !=
        if c == '!=':
            return registers[self.a] != self.b

        # >=
        if c == '>=':
            return registers[self.a] >= self.b

        # Unknown condition
        raise EnvironmentError("Unknown conditional during condition check.")


    def execute(self, registers):
        """Executes the code if it passes the check"""
        # Check the condition
        if self.check_condition(registers):
            # Execute code
            if self.direction == 'inc':
                registers[self.register] += self.value
            elif self.direction == 'dec':
                registers[self.register] -= self.value
            else:
                raise EnvironmentError('Not adding or subtracting during code execution?')


def get_input(registers):
    ans = []
    with open("input.txt") as f:
        for line in f:
            line = line.rstrip()
            line = line.split(' ')

            # Initialize register
            registers[line[0]] = 0

            # Create Code
            register = line[0]
            direction = line[1]
            value = line[2]
            a = line[4]
            condition = line[5]
            b = line[6]
            code = Code(register, direction, value, a, condition, b)
            ans.append(code)

    return ans


def get_all_conditions(commands):
    ans = set()
    for command in commands:
        ans.add(command.condition)
    return ans


def main():
    registers = dict()
    commands = get_input(registers)
    max_value = -inf
    for command in commands:
        command.execute(registers)
        biggest_value = max(registers.items(), key=lambda x: x[1])[1]
        if biggest_value > max_value:
            max_value = biggest_value

    biggest_value = max(registers.items(), key=lambda x: x[1])
    print(biggest_value[1])  # Part 1 ans
    print(max_value)  # Part 2 ans

main()

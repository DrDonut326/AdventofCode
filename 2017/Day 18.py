from Utility import get_input
from collections import defaultdict
from queue import Queue


class Duet:
    def __init__(self, codes):
        self.codes = codes
        self.pointer = 0
        self.registers = defaultdict(int)
        self.last_played = None

    def execute_codes(self):
        """Exectute codes until recover is not none, or the program goes OOB"""
        while self.is_in_bounds():
            code = self.codes[self.pointer]
            result = self.execute(code)

            if result is not None:
                return result
        return 'Program finished with no recover'

    def execute(self, code):
        c = code[0]
        # Snd
        if c == 'snd':
            self.sound(code[1])
            return None

        # Set
        if c == 'set':
            self.set(code[1], code[2])
            return None

        # Add
        if c == 'add':
            self.add(code[1], code[2])
            return None

        # Mul
        if c == 'mul':
            self.mul(code[1], code[2])
            return None

        # Mod
        if c == 'mod':
            self.mod(code[1], code[2])
            return None

        # Recover
        if c == 'rcv':
            result = self.recover(code[1])
            return result


        # Jump
        if c == 'jgz':
            self.jgz(code[1], code[2])
            return None

        # Missed a command
        raise NotImplementedError(f"Didn't include command {c}")

    def increment_pointer(self, x=1):
        self.pointer += x

    def is_in_bounds(self):
        return 0 <= self.pointer < len(self.codes)

    def sound(self, x):
        if type(x) == int:
            self.last_played = x
        else:
            self.last_played = self.registers[x]

        self.increment_pointer()

    def set(self, x, y):
        # X string   Y int
        if type(x) == str and type(y) == int:
            self.registers[x] = y

        # Both strings
        else:
            self.registers[x] = self.registers[y]

        self.increment_pointer()

    def add(self, x, y):

        # X string   Y int
        if type(x) == str and type(y) == int:
            self.registers[x] += y

        # Both strings
        else:
            self.registers[x] += self.registers[y]

        self.increment_pointer()

    def mul(self, x, y):

        # X string   Y int
        if type(x) == str and type(y) == int:
            self.registers[x] *= y

        # Both strings
        else:
            self.registers[x] *= self.registers[y]

        self.increment_pointer()

    def mod(self, x, y):

        # X string   Y int
        if type(x) == str and type(y) == int:
            self.registers[x] %= y

        # Both strings
        else:
            self.registers[x] %= self.registers[y]

        self.increment_pointer()

    def recover(self, x):
        if type(x) == int:
            if x != 0:
                return self.last_played
        else:
            if self.registers[x] != 0:
                return self.last_played

        self.increment_pointer()

    def jgz(self, x, y):
        if self.registers[x] > 0:
            if type(y) == int:
                self.increment_pointer(y)
            else:
                self.increment_pointer(self.registers[y])
        else:
            self.increment_pointer()


class Dueter(Duet):
    def __init__(self, codes):
        super().__init__(codes)
        self.status = 'ok'






def get_codes(lines):
    ans = []
    for line in lines:
        line = line.split(' ')
        # Convert nums to ints
        for i, num in enumerate(line):
            if num.lstrip('-').isnumeric():
                line[i] = int(num)
        ans.append(line)
    return ans


def main():
    lines = get_input('line')
    codes = get_codes(lines)
    duet = Duet(codes)
    result = duet.execute_codes()
    print(result)  # Part 1 ans




main()

from Utility import get_input


class Bunnycomp:
    def __init__(self, codes):
        self.registers = {'a': 0, 'b': 0, 'c': 1, 'd': 0}
        self.pointer = 0
        self.codes = codes


    def update(self):
        while 0 <= self.pointer < len(self.codes):
            code = self.codes[self.pointer]
            command, variables = code[0], code[1:]
            if command == 'cpy':
                x, y = variables
                self.cpy(x, y)
            elif command == 'inc':
                x = variables[0]
                self.inc(x)
            elif command == 'dec':
                x = variables[0]
                self.dec(x)
            elif command == 'jnz':
                x, y = variables
                self.jnz(x, y)
            elif command == 'tgl':
                x = variables[0]
                self.tgl(x)


    def cpy(self, x, y):
        if type(x) == int:
            self.registers[y] = x
        else:
            self.registers[y] = self.registers[x]
        self.pointer += 1

    def inc(self, x):
        self.registers[x] += 1
        self.pointer += 1

    def dec(self, x):
        self.registers[x] -= 1
        self.pointer += 1

    def jnz(self, x, y):
        y = int(y)
        if type(x) == int:
            if x != 0:
                self.pointer += y
            else:
                self.pointer += 1
        else:
            if self.registers[x] != 0:
                self.pointer += y
            else:
                self.pointer += 1

    def tgl(self, x):
        modified_pointer = self.pointer + x
        instruction_to_change = self.codes[modified_pointer]
        


def build_codes():
    codes = get_input('line')
    ans = []
    for code in codes:
        parts = code.split(' ')
        for i, part in enumerate(parts):
            if part.isdigit():
                parts[i] = int(parts[i])
        ans.append(parts)
    return ans




def main():
    codes = build_codes()
    bunnycomp = Bunnycomp(codes)
    bunnycomp.update()
    print(bunnycomp.registers['a'])


if __name__ == '__main__':
    main()

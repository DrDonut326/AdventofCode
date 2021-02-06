from Utility import get_input


class Computer:
    def __init__(self, codes):
        self.registers = {'a': 0, 'b': 0}
        self.index = 0
        self.code_list = codes

    def run(self):
        while 0 <= self.index < len(self.code_list):
            code = self.code_list[self.index]
            self.execute_code(code)
        return self.registers['b']

    def execute_code(self, code):
        m = getattr(self, code[0])
        if code[0] == 'jie' or code[0] == 'jio':
            m(code[1], code[2])
        else:
            m(code[1])

    def hlf(self, r):
        self.registers[r] = self.registers[r] // 2
        self.index += 1

    def tpl(self, r):
        self.registers[r] *= 3
        self.index += 1

    def inc(self, r):
        self.registers[r] += 1
        self.index += 1

    def jmp(self, v):
        self.index += v

    def jie(self, r, v):
        if self.registers[r] % 2 == 0:
            self.index += v
        else:
            self.index += 1

    def jio(self, r, v):
        if self.registers[r] == 1:
            self.index += v
        else:
            self.index += 1


def get_codes(data):
    ans = []
    for line in data:
        if ',' not in line:
            command, right = line.split()
            if command == 'jmp':
                right = int(right)
            ans.append([command, right])
        else:
            left = line[0:3]
            line = line[4:]
            r, v = line.split(', ')
            v = int(v)
            ans.append([left, r, v])
    return ans

def main():
    data = get_input('line')
    codes = get_codes(data)
    computer = Computer(codes)
    print(f"Part 1 answer = {computer.run()}")

    computer = Computer(codes)
    computer.registers['a'] = 1

    print(f"Part 2 answer = {computer.run()}")


main()

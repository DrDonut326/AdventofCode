from Functions import get_input


class BunnyComp:
    def __init__(self, codes):
        self.registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
        self.pointer = 0
        self.codes = codes

    def run(self):
        while 0 <= self.pointer < len(self.codes):
            code = self.codes[self.pointer]
            self.execute_code(code)

    def increment_pointer(self, x=1):
        self.pointer += x

    def cpy(self, x, y):
        # Check if x string
        if type(x) == str:
            # Check if in registers (also checks for string numbers)
            if x in self.registers:
                # Check for string y
                if y in self.registers:
                    self.registers[y] = self.registers[x]

        # Check if x int
        elif type(x) == int:
            if y in self.registers:
                self.registers[y] = x

        # Increment
        self.increment_pointer()

    def mul(self, a, b, c):
        self.registers[c] = self.registers[a] * self.registers[b]
        self.increment_pointer()

    def inc(self, x):
        if x in self.registers:
            self.registers[x] += 1
        self.increment_pointer()

    def dec(self, x):
        if x in self.registers:
            self.registers[x] -= 1
        self.increment_pointer()

    def jnz(self, x, y):
        if type(x) == int:
            if x != 0:
                if type(y) == str:
                    if y in self.registers:
                        # Watch out for increase of 0
                        assert self.registers[y] != 0
                        self.pointer += self.registers[y]
                        return True
                elif type(y) == int:
                    assert y != 0
                    self.pointer += y
                    return True

        elif type(x) == str:
            if x in self.registers:
                if self.registers[x] != 0:
                    if type(y) == str:
                        if y in self.registers:
                            assert self.registers[y] != 0
                            self.pointer += self.registers[y]
                            return True
                    elif type(y) == int:
                        assert y != 0
                        self.pointer += y
                        return True

    def tgl(self, x):
        # Get the index of the code to modify
        if type(x) == int:
            i = self.pointer + x
        elif type(x) == str:
            if x in self.registers:
                i = self.pointer + self.registers[x]
            else:
                return
        else:
            raise EnvironmentError('Bad type for x')

        # If the pointer is bad, do nothing
        if i < 0 or i >= len(self.codes):
            return

        # Change the instruction
        code = self.codes[i]
        # Code name
        c = code[0]

        if c == 'inc':
            self.codes[i] = ['dec', code[1]]

        elif c in ['dec', 'tgl']:
            self.codes[i] = ['inc', code[1]]

        elif c == 'jnz':
            self.codes[i] = ['cpy', code[1], code[2]]

        elif c == 'cpy':
            self.codes[i] = ['jnz', code[1], code[2]]

    def execute_code(self, code):
        # Code name
        c = code[0]

        if c == 'cpy':
            self.cpy(code[1], code[2])

        elif c == 'inc':
            self.inc(code[1])

        elif c == 'dec':
            self.dec(code[1])

        elif c == 'jnz':
            result = self.jnz(code[1], code[2])
            if result is None:
                self.pointer += 1

        elif c == 'tgl':
            self.tgl(code[1])
            self.increment_pointer()

        elif c == 'mul':
            self.mul(code[1], code[2], code[3])

        else:
            raise NotImplementedError("uknown code name")


def build_codes():
    codes = get_input('line')
    ans = []
    for code in codes:
        parts = code.split(' ')
        for i, part in enumerate(parts):
            if part.replace('-', '').isdigit():
                parts[i] = int(parts[i])
        ans.append(parts)
    return ans


def main():
    # codes = build_codes()
    # bunnycomp = BunnyComp(codes)
    # bunnycomp.registers['a'] = 7
    # bunnycomp.run()
    # print(bunnycomp.registers['a'])
    # quit()

    codes = build_codes()
    bunnycomp = BunnyComp(codes)
    bunnycomp.registers['a'] = 12
    bunnycomp.run()
    print(bunnycomp.registers['a'])

    """
    Thanks reddit.  Need to change the program to optimize it.
    cpy b c
    inc a
    dec c
    jnz c -2
    dec d
    jnz d -5
    
    with:
    
    mul b d a
    jnz 0 0
    jnz 0 0
    jnz 0 0
    jnz 0 0
    jnz 0 0"""


main()


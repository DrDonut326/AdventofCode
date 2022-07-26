class IntcodeComputer:
    def __init__(self, codes):
        self.codes = codes
        self.pointer = 0

    def increment_pointer(self, x=4):
        self.pointer += x

    def execute_codes(self):
        while True:
            current_code = self.codes[self.pointer]
            match current_code:
                case 1:
                    self.add()
    
                case 2:
                    self.mul()
                
                case 99:
                    return

    def add(self):
        # Add the next two positions and store it in the third position after
        pa = self.codes[self.pointer + 1]
        pb = self.codes[self.pointer + 2]
        pc = self.codes[self.pointer + 3]
        self.codes[pc] = self.codes[pa] + self.codes[pb]
        self.increment_pointer()

    def mul(self):
        # Multiply the next two positions and store it in the third position after
        pa = self.codes[self.pointer + 1]
        pb = self.codes[self.pointer + 2]
        pc = self.codes[self.pointer + 3]
        self.codes[pc] = self.codes[pa] * self.codes[pb]
        self.increment_pointer()


def get_codes():
    with open('input.txt') as f:
        line = f.readline().rstrip()
        return [int(x) for x in line.split(',')]


def part_1(noun=12, verb=2):
    codes = get_codes()
    codes[1] = noun
    codes[2] = verb
    computer = IntcodeComputer(codes)
    computer.execute_codes()
    return computer.codes[0]


def part_2():
    target = 19690720
    for noun in range(0, 99 + 1):
        for verb in range(0, 99 + 1):
            print(f"Searching noun: {noun} and verb: {verb}...")
            result = part_1(noun, verb)
            if result == target:
                print(100 * noun + verb)
                return


def main():
    print(part_1())
    part_2()



main()

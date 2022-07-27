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
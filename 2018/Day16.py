from random import shuffle


class Device:
    def __init__(self):
        self.registers = [0, 0, 0, 0]
        self.opcode_dict = None

    def set_registers(self, before):
        for i, x in enumerate(before):
            self.registers[i] = x

    def set_opcodes(self, opcode_dict):
        self.opcode_dict = opcode_dict

    def display_info(self):
        print(self.registers)
        print(self.opcode_dict)

    def addr(self, a, b, c):
        self.registers[c] = self.registers[a] + self.registers[b]

    def addi(self, a, b, c):
        self.registers[c] = self.registers[a] + b

    def mulr(self, a, b, c):
        self.registers[c] = self.registers[a] * self.registers[b]

    def muli(self, a, b, c):
        self.registers[c] = self.registers[a] * b

    def banr(self, a, b, c):
        self.registers[c] = self.registers[a] & self.registers[b]

    def bani(self, a, b, c):
        self.registers[c] = self.registers[a] & b

    def borr(self, a, b, c):
        self.registers[c] = self.registers[a] | self.registers[b]

    def bori(self, a, b, c):
        self.registers[c] = self.registers[a] | b

    def setr(self, a, b, c):
        self.registers[c] = self.registers[a]

    def seti(self, a, b, c):
        self.registers[c] = a

    def gtir(self, a, b, c):
        self.registers[c] = 1 if a > self.registers[b] else 0

    def gtri(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] > b else 0

    def gtrr(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] > self.registers[b] else 0

    def eqir(self, a, b, c):
        self.registers[c] = 1 if a == self.registers[b] else 0

    def eqri(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] == b else 0

    def eqrr(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] == self.registers[b] else 0

    def run_program(self, instruction):
        code_num, a, b, c = instruction
        op_string = self.opcode_dict[code_num]
        # Run the command
        com = getattr(Device, op_string)
        com(self, a, b, c)


def get_tests():
    tests = []
    line = '.'
    with open("input.txt") as f:
        while line != '':
            # Before part
            line = f.readline().rstrip()
            line = line.replace('Before: [', '')
            line = line.replace(']', '')
            before = [int(x) for x in line.split(', ')]

            # Codes
            codes = f.readline().rstrip()
            codes = [int(x) for x in codes.split()]

            # After
            line = f.readline().rstrip()
            line = line.replace('After:  [', '')
            line = line.replace(']', '')
            after = [int(x) for x in line.split(', ')]

            line = f.readline()

            tests.append((before, codes, after))
    return tests


def get_random_association():
    operations = 'addr addi mulr muli banr bani borr bori setr seti gtir gtri gtrr eqir eqri eqrr'
    operations = operations.split(' ')

    # Shuffle then add numbers
    shuffle(operations)

    # Create dict
    opcode_dict = dict()
    for i, op in enumerate(operations):
        opcode_dict[i] = op

    return opcode_dict


def perform_test(device: Device, test, opcodes: dict):
    # Get test parameters
    before, instruction, after = test

    # Setup the device
    device.set_registers(before)
    device.set_opcodes(opcodes)

    # Run the program
    device.run_program(instruction)

    # Check the results
    return after == device.registers


def check_opcode(device, tests, op_string):
    """Checks every test with this op string and returns a list of numbers where there were no errors."""
    passed = set()
    failed = set()
    # When a code passes a test, add that number to the passed.  Failed = failed set

    for test in tests:
        # Get the number this test tests.
        opcode_num = test[1][0]
        opcode_dict = {opcode_num: op_string}

        if perform_test(device, test, opcode_dict):
            passed.add(opcode_num)
        else:
            failed.add(opcode_num)

    # Return all numbers that passed and never failed
    return [x for x in passed if x not in failed]


def check_all_opcodes(device, tests):
    # Setup operations strings
    operations = 'addr addi mulr muli banr bani borr bori setr seti gtir gtri gtrr eqir eqri eqrr'
    operations = operations.split(' ')

    possible_numbers = dict()

    for op_string in operations:
        # Get a list of passed numbers
        passed_nums = check_opcode(device, tests, op_string)

        # Update the possible_numbers dictionary
        possible_numbers[op_string] = passed_nums

    return possible_numbers


def part_1(device, tests):
    """Test each test against all codes and see how many have 3 or more passing tests"""

    # Get a list of all op strings
    operations = 'addr addi mulr muli banr bani borr bori setr seti gtir gtri gtrr eqir eqri eqrr'
    operations = operations.split(' ')

    # Counter for tests that have 3 or more passing strings
    ans_count = 0

    for test in tests:
        pass_count = 0
        for op_string in operations:
            opcode_num = test[1][0]
            opcode_dict = {opcode_num: op_string}  # Only need one item in the dictionary

            # Check if the test passed
            if perform_test(device, test, opcode_dict):
                pass_count += 1

        # If three tests passed, increment the answer
        if pass_count >= 3:
            ans_count += 1

    return ans_count

def part_2(device, opcode_dict):
    # Paste the program into input.txt before running

    # Setup the device
    device.set_registers([0, 0, 0, 0])
    device.set_opcodes(opcode_dict)

    # Run all program codes
    with open('input.txt') as f:
        for line in f:
            line = line.rstrip()
            instruction = [int(x) for x in line.split(' ')]

            # Run the program
            device.run_program(instruction)

    # Return register 0
    return device.registers[0]


def main():
    #tests = get_tests()
    device = Device()

    # Paste in only the top half before using

    # print(part_1(device, tests))  # Part 1 answer

    # Get a list of possible codes for each string for manual searching
    # results = check_all_opcodes(device, tests)

    # Make the final opcode dict
    opcode_dict = {
        11: 'addr',
        4:  'addi',
        13: 'mulr',
        1:  'muli',
        0:  'banr',
        10: 'bani',
        8:  'borr',
        2:  'bori',
        3:  'setr',
        14: 'seti',
        7:  'gtir',
        6:  'gtri',
        15: 'gtrr',
        12: 'eqir',
        9:  'eqri',
        5:  'eqrr'
    }

    print(part_2(device, opcode_dict))

main()



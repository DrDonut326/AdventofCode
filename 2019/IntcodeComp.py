class IntcodeComputer:
    def __init__(self, codes: list[int], get_input: callable, input_generator=None, input_mode=None):
        self.codes = codes
        self.pointer = 0
        self.input_generator = input_generator
        self.get_input = get_input
        self.outputs = []
        self.input_mode = input_mode
        self.ignore_input = False

    def increment_pointer(self, x=4):
        self.pointer += x

    def get_opcode_and_parameter_modes(self):
        # Raise an error if the pointer is negative or OOB
        if self.pointer < 0 or self.pointer >= len(self.codes):
            raise EnvironmentError('Bad pointer location.')

        # Get current code
        code = self.codes[self.pointer]

        # The the opcode from the rightmost 2 digit numbers
        # Convert to string for processing
        code = str(code)

        # Pad length if needed
        code = code.zfill(2)

        assert len(code) >= 2

        opcode = int(code[-2:])

        # Get rid of end
        param_code = code[0:-2]


        # Flip and convert to ints
        parameters = [int(x) for x in reversed(param_code)]

        # Add zeros as needed
        self.pad_parameters(opcode, parameters)

        return opcode, parameters

    def pad_parameters(self, opcode, p):
        num_fill = 0
        match opcode:
            case 1 | 2 | 7 | 8:
                num_fill = 3
            case 3 | 4:
                num_fill = 1
            case 5 | 6:
                num_fill = 2
        while len(p) < num_fill:
            p.append(0)

    def execute_codes(self):
        """Executes the current code."""
        while True:
            # Get the op code and parameter modes
            opcode, parameter_modes = self.get_opcode_and_parameter_modes()
            if opcode == 99:
                return
            # Send the parameters to the code for running
            match opcode:
                case 1:
                    self.add(parameter_modes)

                case 2:
                    self.mul(parameter_modes)

                case 3:
                    self.save(parameter_modes)

                case 4:
                    self.output(parameter_modes)

                case 5:
                    self.jnz(parameter_modes)

                case 6:
                    self.jif(parameter_modes)

                case 7:
                    self.less_than(parameter_modes)

                case 8:
                    self.equal(parameter_modes)

                case 99:
                    print("Job's done.")

    def add(self, parameter_modes):
        if parameter_modes[0] == 0:
            index = self.codes[self.pointer + 1]
            a = self.codes[index]
        else:
            a = self.codes[self.pointer + 1]

        if parameter_modes[1] == 0:
            index = self.codes[self.pointer + 2]
            b = self.codes[index]
        else:
            b = self.codes[self.pointer + 2]

        c = self.codes[self.pointer + 3]

        self.codes[c] = a + b

        self.increment_pointer(4)

    def mul(self, parameter_modes):
        if parameter_modes[0] == 0:
            index = self.codes[self.pointer + 1]
            a = self.codes[index]
        else:
            a = self.codes[self.pointer + 1]

        if parameter_modes[1] == 0:
            index = self.codes[self.pointer + 2]
            b = self.codes[index]
        else:
            b = self.codes[self.pointer + 2]

        c = self.codes[self.pointer + 3]

        self.codes[c] = a * b

        self.increment_pointer(4)

    def save(self, parameter_modes):
        if self.input_mode is None:
            to_store = self.get_input()
        elif self.input_mode == 'SELF':
            to_store = self.get_input(self)
        else:
            raise EnvironmentError('Bad input mode passed in')

        if parameter_modes[0] == 0:
            index = self.codes[self.pointer + 1]
            self.codes[index] = to_store
        else:
            raise EnvironmentError('bad store')
        self.increment_pointer(2)

    def output(self, parameter_modes):
        if parameter_modes[0] == 0:
            index = self.codes[self.pointer + 1]
            self.outputs.append(self.codes[index])
        else:
            self.outputs.append(self.codes[self.pointer + 1])

        self.increment_pointer(2)

    def jnz(self, parameter_modes):
        do_part_2 = False
        if parameter_modes[0] == 0:
            index = self.codes[self.pointer + 1]
            val = self.codes[index]
        else:
            val = self.codes[self.pointer + 1]

        if val != 0:
            do_part_2 = True

        if not do_part_2:
            self.increment_pointer(3)
            return

        if parameter_modes[1] == 0:
            index = self.codes[self.pointer + 2]
            val = self.codes[index]
            self.pointer = val
        else:
            val = self.codes[self.pointer + 2]
            self.pointer = val

    def jif(self, parameter_modes):
        do_part_2 = False
        if parameter_modes[0] == 0:
            index = self.codes[self.pointer + 1]
            val = self.codes[index]

        else:
            val = self.codes[self.pointer + 1]

        if val == 0:
            do_part_2 = True

        if not do_part_2:
            self.increment_pointer(3)
            return

        if parameter_modes[1] == 0:
            index = self.codes[self.pointer + 2]
            val = self.codes[index]
            self.pointer = val
        else:
            val = self.codes[self.pointer + 2]
            self.pointer = val

    def less_than(self, parameter_modes):
        if parameter_modes[0] == 0:
            index = self.codes[self.pointer + 1]
            a = self.codes[index]
        else:
            a = self.codes[self.pointer + 1]

        if parameter_modes[1] == 0:
            index = self.codes[self.pointer + 2]
            b = self.codes[index]
        else:
            b = self.codes[self.pointer + 2]

        index = self.codes[self.pointer + 3]
        if a < b:
            self.codes[index] = 1
        else:
            self.codes[index] = 0

        self.increment_pointer(4)

    def equal(self, parameter_modes):
        if parameter_modes[0] == 0:
            index = self.codes[self.pointer + 1]
            a = self.codes[index]
        else:
            a = self.codes[self.pointer + 1]

        if parameter_modes[1] == 0:
            index = self.codes[self.pointer + 2]
            b = self.codes[index]
        else:
            b = self.codes[self.pointer + 2]

        index = self.codes[self.pointer + 3]
        if a == b:
            self.codes[index] = 1
        else:
            self.codes[index] = 0

        self.increment_pointer(4)










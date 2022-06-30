from collections import defaultdict
from dataclasses import dataclass


@ dataclass
class Command:
    value: int
    move: int
    state: str


class Turing:
    def __init__(self, state, rules, checksum_time):
        self.tape = defaultdict(int)
        self.cursor = 0
        self.rules = rules
        self.state = state
        self.checksum_time = checksum_time
        self.counter = 0

    def run_program(self):
        while self.counter < self.checksum_time:
            self.update()
        return self.get_checksum()

    def update(self):
        """Take one step"""
        # Get current value
        current_value = self.tape[self.cursor]

        # ----Apply rule
        rule = self.rules[self.state][current_value]

        # Write value
        self.write_to_current_position(rule.value)

        # Change position
        self.change_position(rule.move)

        # Change state
        self.change_state(rule.state)

        # Update counter by one
        self.counter += 1

    def get_checksum(self):
        count = 0
        for x in self.tape.values():
            if x == 1:
                count += 1
        return count


    def write_to_current_position(self, x):
        self.tape[self.cursor] = x

    def change_position(self, x):
        self.cursor += x

    def change_state(self, x):
        self.state = x


def build_rules():
    rules = dict()
    with open('input.txt') as f:
        initial_state = f.readline().rstrip()[-2]
        checksum_time = int(f.readline().split(' after ')[1].split(' ')[0])

        f.readline()

        # Start building states
        line = f.readline().rstrip()

        while line != '':
            # Get state letter
            letter = line[-2]

            # Skip
            f.readline()

            # ---- if value is 0
            zero_value = int(f.readline().rstrip()[:-1].split(' value ')[1])
            move = f.readline().rstrip()[:-1].split(' to the ')[1]
            if move == 'right':
                zero_move = 1
            elif move == 'left':
                zero_move = -1
            else:
                raise EnvironmentError('Bad string parse.')
            zero_state = f.readline().rstrip()[:-1].split(' with state ')[1]

            zero_com = Command(zero_value, zero_move, zero_state)

            # Skip
            f.readline()

            # ----- if value is 1
            one_value = int(f.readline().rstrip()[:-1].split(' value ')[1])
            move = f.readline().rstrip()[:-1].split(' to the ')[1]
            if move == 'right':
                one_move = 1
            elif move == 'left':
                one_move = -1
            else:
                raise EnvironmentError('Bad string parse.')
            one_state = f.readline().rstrip()[:-1].split(' with state ')[1]

            one_com = Command(one_value, one_move, one_state)



            command_dict = {
                0: zero_com,
                1: one_com
            }

            rules[letter] = command_dict

            # Skip last line
            r = f.readline()

            # Set next line
            line = f.readline().rstrip()

    return initial_state, checksum_time, rules




def main():
    initial_state, checksum_time, rules = build_rules()
    turing = Turing(initial_state, rules, checksum_time)
    checksum = turing.run_program()
    print(checksum)

main()

from collections import defaultdict
from queue import Queue

from Functions import get_input


class Dueter:
    def __init__(self, codes, id_num):
        self.codes = codes
        self.pointer = 0
        self.registers = defaultdict(int)
        self.last_played = None
        self.status = 'OK'
        self.partner = None
        self.q = Queue()
        self.id_num = id_num
        # self.registers['p'] = self.id_num
        self.values_sent = 0
        self.mul_used = 0

    def execute_once(self):
        """Exectute until the result is false."""
        if self.pointer < 0 or self.pointer >= len(self.codes):
            self.status = 'DONE'
            return
        else:
            code = self.codes[self.pointer]
            result = self.execute(code)
            return result

    def execute(self, code):
        c = code[0]
        #print(f"Program {self.id_num} running {code}")
        # Snd
        if c == 'snd':
            return self.snd(code[1])


        # Set
        if c == 'set':
            return self.set(code[1], code[2])


        # Add
        if c == 'add':
            return self.add(code[1], code[2])


        # Mul
        if c == 'mul':
            return self.mul(code[1], code[2])

        # Mod
        if c == 'mod':
            return self.mod(code[1], code[2])

        # Rcv
        if c == 'rcv':
            result = self.rcv(code[1])
            return result


        # Jump
        if c == 'jgz':
            return self.jgz(code[1], code[2])

        if c == 'jnz':
            return self.jnz(code[1], code[2])

        if c == 'sub':
            return self.sub(code[1], code[2])

        # Missed a command
        raise NotImplementedError(f"Didn't include command {c}")

    def increment_pointer(self, x=1):
        self.pointer += x

    def snd(self, x):
        # Get the package ready
        if type(x) == str:
            package = self.registers[x]
        elif type(x) == int:
            package = x
        else:
            raise EnvironmentError('Bad type of x for send function.')

        self.partner.q.put(package)
        self.values_sent += 1
        self.increment_pointer()
        return True

    def rcv(self, x):
        if not self.q.empty():
            # Queue is not empty, so just get it and move on
            package = self.q.get()
            if type(x) == str:
                self.registers[x] = package
                self.status = 'OK'
                self.increment_pointer()
                return True
            else:
                raise EnvironmentError('Bad register name.')

        else:
            # Queue is empty, must WAIT for a value to arrive
            self.status = 'WTR'
            return True

    def set(self, x, y):
        assert type(x) == str

        if type(y) == str:
            self.registers[x] = self.registers[y]
        else:
            self.registers[x] = y

        self.increment_pointer()

    def add(self, x, y):

        if type(y) == str:
            self.registers[x] += self.registers[y]
        else:
            self.registers[x] += y

        self.increment_pointer()
        return True

    def sub(self, x, y):
        if type(y) == str:
            self.registers[x] -= self.registers[y]
        else:
            self.registers[x] -= y

        self.increment_pointer()
        return True

    def mul(self, x, y):
        assert type(x) == str

        if type(y) == int:
            self.registers[x] = self.registers[x] * y
        else:
            self.registers[x] = self.registers[x] * self.registers[y]

        self.mul_used += 1
        self.increment_pointer()
        return True

    def mod(self, x, y):

        # X string   Y int
        if type(x) == str and type(y) == int:
            self.registers[x] %= y

        # Both strings
        else:
            self.registers[x] %= self.registers[y]

        self.increment_pointer()
        return True

    def jnz(self, x, y):
        # Make sure you aren't defaultdicting a new register
        if type(x) == int:
            if x != 0:
                if type(y) == int:
                    self.increment_pointer(y)
                else:
                    self.increment_pointer(self.registers[y])
        else:
            if self.registers[x] != 0:
                if type(y) == int:
                    self.increment_pointer(y)
                else:
                    self.increment_pointer(self.registers[y])
            else:
                self.increment_pointer()
        return True





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

    duet_a = Dueter(codes, 0)
    duet_b = Dueter(codes, 1)

    duet_a.partner = duet_b
    duet_b.partner = duet_a

    duet_b.status = 'DONE'

    while True:

        duet_a.execute_once()
        duet_b.execute_once()

        # Check for double WTR
        if duet_a.status == 'WTR' and duet_b.status == 'WTR':
            break

        # Check for both done
        done_stati = ['DONE', 'WTR']
        if duet_a.status in done_stati and duet_b.status in done_stati:
            break

        print(f"a: {duet_a.registers} || b: {duet_b.registers}")


    print(duet_a.mul_used)

main()

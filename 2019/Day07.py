from IntcodeComp import IntcodeComputer
from itertools import permutations


def get_codes():
    with open("input.txt") as f:
        line = f.readline().rstrip()
        line = [int(x) for x in line.split(',')]
    return line


def phase_permuations_gen():
    for perm in permutations([0, 1, 2, 3, 4], 5):
        yield perm


def phase_permutations_gen_2():
    for perm in permutations([5, 6, 7, 8, 9], 5):
        yield perm


def create_func_gen(permutation, id_num, list_location):
    yield permutation[id_num]
    yield list_location[0]


def part_2_func_gen(permutation, id_num, list_location):
    yield permutation[id_num]
    if id_num == 0:
        yield 0
    while True:
        yield list_location[-1]


def input_func(self: IntcodeComputer):
    return next(self.input_generator)

def run_simulation(codes, perm):
    # Set up the five computers
    a_gen = create_func_gen(perm, 0, [0])
    a = IntcodeComputer(codes, input_func, a_gen, input_mode='SELF')

    b_gen = create_func_gen(perm, 1, a.outputs)
    b = IntcodeComputer(codes, input_func, b_gen, input_mode='SELF')

    c_gen = create_func_gen(perm, 2, b.outputs)
    c = IntcodeComputer(codes, input_func, c_gen, input_mode='SELF')

    d_gen = create_func_gen(perm, 3, c.outputs)
    d = IntcodeComputer(codes, input_func, d_gen, input_mode='SELF')

    e_gen = create_func_gen(perm, 4, d.outputs)
    e = IntcodeComputer(codes, input_func, e_gen, input_mode='SELF')

    a.execute_codes()
    b.execute_codes()
    c.execute_codes()
    d.execute_codes()
    e.execute_codes()

    return e.outputs[0]


def run_simulation_2(codes, perm):
    # Set up the five computers
    a_gen = part_2_func_gen(perm, 0, [0])
    a = IntcodeComputer(codes, input_func, a_gen, input_mode='SELF')

    b_gen = part_2_func_gen(perm, 1, a.outputs)
    b = IntcodeComputer(codes, input_func, b_gen, input_mode='SELF')

    c_gen = part_2_func_gen(perm, 2, b.outputs)
    c = IntcodeComputer(codes, input_func, c_gen, input_mode='SELF')

    d_gen = part_2_func_gen(perm, 3, c.outputs)
    d = IntcodeComputer(codes, input_func, d_gen, input_mode='SELF')

    e_gen = part_2_func_gen(perm, 4, d.outputs)
    e = IntcodeComputer(codes, input_func, e_gen, input_mode='SELF')

    # Redo a's gen
    a_gen = part_2_func_gen(perm, 0, e.outputs)
    a.input_generator = a_gen

    # Go until e halts
    while True:
        print('running...')
        a.execute_codes()
        b.execute_codes()
        c.execute_codes()
        d.execute_codes()
        e.execute_codes()
        if e.codes[e.pointer] == 99:
            return e.outputs[-1]

def part_1():
    # Create permutations generator
    perm_gen = phase_permuations_gen()

    # Get program code
    codes = get_codes()

    # Track best
    best = -1

    # Get the output of each possible permutation
    for perm in perm_gen:
        result = run_simulation(codes, perm)
        if result > best:
            best = result

    print(best)


def part_2():
    # Create permutations generator
    perm_gen = phase_permutations_gen_2()

    # Get program code
    codes = get_codes()

    # Track best
    best = -1

    # Get the output of each possible permutation
    for perm in perm_gen:
        result = run_simulation_2(codes, perm)
        if result > best:
            best = result

    print(best)

def main():
    #part_1()
    part_2()

main()

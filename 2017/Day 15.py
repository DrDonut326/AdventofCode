class Judge:
    def __init__(self, gen_a, gen_b):
        self.gen_a = gen_a
        self.gen_b = gen_b
        self.count = 0

    def compare_next_16(self):
        """Adds 1 to the count if the last 16 bits match"""
        a_num = next(self.gen_a)
        b_num = next(self.gen_b)
        a_16 = self.get_16_bin(a_num)
        b_16 = self.get_16_bin(b_num)

        if a_16 == b_16:
            self.count += 1

    def convert_to_32_bit(self, n):
        return bin(n)[2:].zfill(32)

    def get_16_bin(self, n):
        return self.convert_to_32_bit(n)[16:]

def make_generator(starting_value, factor, multiple=None):
    previous_value = starting_value
    while True:
        result = previous_value * factor % 2147483647
        if multiple is None:
            yield result
        else:
            while result % multiple != 0:
                previous_value = result
                result = previous_value * factor % 2147483647
        yield result
        previous_value = result

gen_a_start = 618
gen_b_start = 814

# gen_a = make_generator(gen_a_start, 16807)
# gen_b = make_generator(gen_b_start, 48271)
#
# judge = Judge(gen_a, gen_b)
# for _ in range(40000000):
#     judge.compare_next_16()
#
# print(judge.count) # Part 1 answer

gen_a = make_generator(gen_a_start, 16807, 4)
gen_b = make_generator(gen_b_start, 48271, 8)

judge = Judge(gen_a, gen_b)
for _ in range(5000000):
    judge.compare_next_16()

print(judge.count) # Part 2 answer

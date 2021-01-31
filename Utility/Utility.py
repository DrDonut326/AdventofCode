# Utility methods for quickly import data
from functools import reduce

def get_input(line_or_char, text_location='input.txt', do_split=False, split_key='', early_stop=False, stop_char=''):
    """Gets the input, and spits it into a list
    By default goes line-by-line
    Kwargs to control special features"""
    ans = []
    with open(text_location) as f:
        for line in f:
            line = line.rstrip()
            # Check for an early stop
            if early_stop:
                if line == stop_char:
                    return ans
            if do_split:
                line = line.split(split_key)
            if line_or_char == 'line':
                ans.append(line)
            else:
                for element in line:
                    ans.append(element)
    return ans


def factors(n):
    return set(reduce(list.__add__,
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))
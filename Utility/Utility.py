# Utility methods for quickly import data
from functools import reduce
from Pos import Pos


def get_input(line_or_char, text_location='input.txt', do_split=False, split_key='', early_stop=False, stop_char='', int_convert=False, int_split=False):
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
                if int_convert:
                    if type(line) == list:
                        ans.append([int(x) for x in line])
                    else:
                        ans.append(int(line))
                elif int_split:
                    ans.append([int(x) for x in list(line)])
                else:
                    ans.append(line)
            else:
                for element in line:
                    if int_convert:
                        ans.append(int(element))
                    else:
                        ans.append(element)
    return ans


def factors(n):
    g = list([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)
    if len(g) > 1:
        f = reduce(list.__add__, g)
    else:
        f = []
    return set(f)


def get_indices_of_substring(full_string, sub_string):
    """Returns a list of indicies of locations of the
    sub string in the full string"""
    assert sub_string in full_string
    ans = []
    i = 0
    while True:
        try:
            result = full_string.index(sub_string, i)
        except ValueError:
            return ans
        ans.append(result)
        i = result + 1


def get_new_string_with_substring_at_index(full_string, target, sub_string, i):
    """Used in combination with 'get_indices_of_substring'
    To replace all instances of a string with a substring"""
    assert type(full_string) == str and type(sub_string) == str and type(i) == int
    assert 0 <= i < len(full_string)
    return full_string[0: i] + full_string[i:].replace(target, sub_string, 1)


def manhat(a, b=(0, 0)):
    """Returns the manhatten distance between 2 points
    Accepts format (x,y) / (x,y)"""
    if type(a) == Pos or type(b) == Pos:
        raise EnvironmentError('Please use manhat_pos instead.')
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def manhat_pos(a, b=Pos(0, 0)):
    """Manhatten distance for Pos objects"""
    return abs(a.x - b.x) + abs(a.y - b.y)

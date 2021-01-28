# Utility methods for quickly import data


def get_input(line_or_char, text_location='input.txt', do_split=False, split_key=''):
    """Gets the input, and spits it into a list
    By default goes line-by-line
    Kwargs to control special features"""
    ans = []
    with open(text_location) as f:
        for line in f:
            line = line.rstrip()
            if do_split:
                line = line.split(split_key)
            if line_or_char == 'line':
                ans.append(line)
            else:
                for element in line:
                    ans.append(element)
    return ans
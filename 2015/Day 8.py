from Functions import get_input


def count_character(s):
    s = s[1:-1]
    count = 0
    i = 0
    while len(s) > 0:
        if s.startswith('\\x'):
            s = s[4:]
        elif s.startswith('\\\\'):
            s = s[2:]
        elif s.startswith('\\"'):
            s = s[2:]
        else:
            s = s[1:]
        count += 1

    return count


def encode_string(s):
    ans = '"'
    for element in s:
        if element == '\\' or element == '"':
            ans += '\\'
            ans += element
        else:
            ans += element
    ans += '"'
    return ans


def part_1(strings):
    len_total = 0
    char_total = 0
    for line in strings:
        len_total += len(line)
        char_total += count_character(line)
    print(len_total - char_total)

def part_2(strings):
    original_len_total = 0
    new_len_total = 0
    for line in strings:
        original_len_total += len(line)
        new_len_total += len(encode_string(line))
    print(new_len_total - original_len_total)


def main():
    string_lines = get_input('line')
    part_1(string_lines)
    part_2(string_lines)



main()

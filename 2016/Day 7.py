from Functions import get_input


def split_hypernets(s):
    """Returns a list of chunks of non and hyper strings"""
    non = []
    hyper = []
    non_write = True
    chunk = ''
    for x in s:
        if x == '[' or x == ']':
            if len(chunk) > 0:
                if non_write:
                    non.append(chunk)
                else:
                    hyper.append(chunk)
            non_write = not non_write
            chunk = ''
        else:
            chunk += x
    if len(chunk) > 0:
        if non_write:
            non.append(chunk)
        else:
            hyper.append(chunk)
    return non, hyper


def does_string_support_ABBA(s):
    if len(s) < 4:
        return False
    for a, b, c, d in zip(s, s[1:], s[2:], s[3:]):
        if a == d and b == c and a != b:
            return True
    return False


def does_code_support_TLS(code):
    non, hyper = split_hypernets(code)
    for h in hyper:
        if does_string_support_ABBA(h):
            return False
    for n in non:
        if does_string_support_ABBA(n):
            return True
    return False


def count_TLS(codes):
    count = 0
    for code in codes:
        if does_code_support_TLS(code):
            count += 1
    return count


def get_ABAs(supernet_list):
    ans = []
    for s in supernet_list:
        if len(s) < 3:
            continue
        for a, b, c in zip(s, s[1:], s[2:]):
            if a == c and a != b:
                ans.append(f"{a}{b}{a}")
    return ans


def get_ABA_inverse(aba):
    assert len(aba) == 3
    return aba[1] + aba[0] + aba[1]


def does_code_support_SSL(code):
    supernet, hypernet = split_hypernets(code)
    list_of_ABAs = get_ABAs(supernet)
    list_of_BABs = get_ABAs(hypernet)
    for aba in list_of_ABAs:
        if get_ABA_inverse(aba) in list_of_BABs:
            return True
    return False


def count_SSL(codes):
    count = 0
    for code in codes:
        if does_code_support_SSL(code):
            count += 1
    return count


def main():
    codes = get_input('line')
    print(f"Part 1 answer = {count_TLS(codes)}")
    print(f"Part 2 answer = {count_SSL(codes)}")


if __name__ == '__main__':
    main()

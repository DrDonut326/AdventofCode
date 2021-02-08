from hashlib import md5


def setup_hash_string(addition):
    # Put the puzzle input here ------------------------
    start = 'wtnhxymk'

    finish = start + str(addition)
    # Encodes it in utf-8
    finish = finish.encode('utf-8')
    return finish


def get_hash(x):
    hash_string = setup_hash_string(x)
    hash_obj = md5(hash_string)
    ans = hash_obj.hexdigest()
    return ans


def get_5_zeros(x):
    while True:
        ans = get_hash(x)
        if ans.startswith('00000'):
            yield ans
        x += 1


def part2():
    hash_gen = get_5_zeros(0)
    ans = [-1, -1, -1, -1, -1, -1, -1, -1]
    while -1 in ans:
        h = next(hash_gen)
        i = h[5]
        v = h[6]
        if i.isdigit() and 0 <= int(i) < len(ans) and ans[int(i)] == -1:
            ans[int(i)] = v
    ans = ''.join(ans)
    return ans


def part1():
    hash_gen = get_5_zeros(0)
    ans = ''
    for _ in range(8):
        h = next(hash_gen)
        ans += str(h)[5]
    ans = ''.join(ans)
    return ans


def main():
    print(f"Part 1 ans = {part1()}")
    print(f"Part 2 ans = {part2()}")


main()

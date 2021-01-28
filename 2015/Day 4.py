from hashlib import md5


def setup_hash_string(addition):
    # Put the puzzle input here ------------------------
    start = 'bgvyzdsv'

    finish = start + str(addition)
    # Encodes it in utf-8
    finish = finish.encode('utf-8')
    return finish


def get_hash(x):
    hash_string = setup_hash_string(x)
    hash_obj = md5(hash_string)
    ans = hash_obj.hexdigest()
    return ans


def main(part):
    x = 0
    if part == 1:
        while True:
            ans = get_hash(x)
            if ans.startswith('00000'):
                print(x)
                return
            x += 1
    else:
        while True:
            ans = get_hash(x)
            if ans.startswith('000000'):
                print(x)
                return
            x += 1


main(2)

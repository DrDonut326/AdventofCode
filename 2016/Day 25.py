def get_output(a):
    ans = []
    d = a + 2550
    counter = 0
    while True:
        a = d
        while a != 0:
            counter += 1
            if len(ans) > 1:
                if ans[-2] == ans[-1]:
                    return 'bad'
            if counter >= 100:
                return ''.join([str(x) for x in ans])
            b = a % 2
            a //= 2
            ans.append(b)

start_num = 0
while True:
    start_num += 1
    o = get_output(start_num)
    if o != 'bad':
        print(start_num)
        print(o)
        break

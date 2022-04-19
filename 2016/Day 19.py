from collections import deque



def joseph(n):
    n = deque(list(range(1, n + 1)))
    while len(n) > 1:
        if len(n) % 2 == 0:
            n.rotate(len(n) // 2)
            n.rotate()
        else:
            n.rotate(len(n) // 2 + 1)
        n.popleft()

        print(n)

    print(n)




joseph(5)
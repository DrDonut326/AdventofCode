from collections import deque



spinlock = deque([0])
i = 0
steps = 380

for x in range(2018):
    i = (i + steps) % len(spinlock)
    spinlock.insert(i + 1, x + 1)
    i += 1
magic_i = spinlock.index(2017)
print(spinlock[magic_i+1])

# -- Part 2

i = 0
steps = 380
part_2_ans = None
for x in range(50000001):
    i = (i + steps) % (x + 1)
    # Don't insert, just track if something inserts after 0
    if i == 0:
        part_2_ans = x + 1
    i += 1
print(part_2_ans)

from collections import defaultdict
from queue import Queue as q


def get_starting_numbers():
    with open("input.txt") as f:
        line = f.readline().rstrip()
        line = [int(x) for x in line.split(',')]
        ans = q()
        for n in line:
            ans.put(n)
    return ans



def say_a_number(starting_nums, num_dict, turn, spoken_list):
    # Are there any starting numbers left?
    # If so, say one of those numbers
    if not starting_nums.empty():
        # Say the number
        n = starting_nums.get()
        num_dict[n].append(turn)
        spoken_list.append(n)
        return
    # Get the last number spoken
    last = spoken_list[-1]

    # If it has only been said once, say 0
    if last not in num_dict or len(num_dict[last]) == 1:
        n = 0
        num_dict[n].append(turn)
        spoken_list.append(0)
        return
    # Else say the difference between the last and second last
    n = num_dict[last][-1] - num_dict[last][-2]
    num_dict[n].append(turn)
    spoken_list.append(n)


def main():
    num_dict = defaultdict(list)
    nums = get_starting_numbers()
    spoken_list = []
    turn = 1
    # Change this for part 1 to 2020
    for _ in range(30000000):

        say_a_number(nums, num_dict, turn, spoken_list)
        turn += 1

    print(spoken_list[-1])

main()

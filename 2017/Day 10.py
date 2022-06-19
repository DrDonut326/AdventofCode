from collections import deque


def ascii_convert(x):
    """Returns the input as a list of ascii codes"""
    assert type(x) == str
    ans = []
    for element in x:
        ans.append(ord(element))

    # Append th extra bit
    extra = [17, 31, 73, 47, 23]
    for ex in extra:
        ans.append(ex)

    return ans


def knot_hash(i, skip_size, puzzle_input, list_length, rounds=1):
    rotations = []
    main_list = list(range(list_length))

    for r in range(rounds):

        for p in puzzle_input:
            # --- Reverse that section of list (current position plus p)
            # Get the sub array
            sub_array = main_list[0: i + p]

            # Reverse the sub array
            sub_array.reverse()

            # Replace into the main list
            main_list[i: i + p] = sub_array

            # --- Increase current position by p + skip_size
            # Convert to deque
            deq_list = deque(main_list)

            # Rotate by p + skip size
            r = p + skip_size
            deq_list.rotate(-r)
            rotations.append(r)

            # Increment skip size
            skip_size += 1

            # Change back to list
            main_list = list(deq_list)

    # Undo rotations
    undo = deque(main_list)
    for r in rotations:
        undo.rotate(r)

    # Clear rotation list
    rotations.clear()

    # Back to main list
    main_list = list(undo)

    return main_list


def get_sixteen_blocks(sparse):
    ans = []
    count = 0
    current = []
    for i, letter in enumerate(sparse):
        current.append(letter)
        count += 1
        if count == 16:
            ans.append(current)
            current = []
            count = 0
    return ans


def get_xor_num(block):
    ans = 0
    for num in block:
        ans ^= num
    return ans


def get_dense_hash(sparse):
    # Get sixteen blocks
    sixteen_blocks = get_sixteen_blocks(sparse)
    dense_nums = []
    for block in sixteen_blocks:
        dense_nums.append(get_xor_num(block))
    return dense_nums


def dense_num_to_hex(num):
    return "{:02x}".format(num)


def part_1():
    list_length = 256
    puzzle_input = [46, 41, 212, 83, 1, 255, 157, 65, 139, 52, 39, 254, 2, 86, 0, 204]
    i = 0
    skip_size = 0
    final_list = knot_hash(i, skip_size, puzzle_input, list_length)
    print(final_list[0] * final_list[1])


def get_hex_string(dense_hash):
    ans = []
    for dense in dense_hash:
        ans.append(dense_num_to_hex(dense))
    return ''.join(ans)


def part_2(puzzle_input):

    puzzle_input = ascii_convert(puzzle_input)
    i = 0
    skip_size = 0

    sparse_hash = knot_hash(i, skip_size, puzzle_input, 256, 64)

    dense_hash = get_dense_hash(sparse_hash)

    hex_string = get_hex_string(dense_hash)

    print(hex_string)


def main():
    part_1()  # Part 1 answer
    part_2('46,41,212,83,1,255,157,65,139,52,39,254,2,86,0,204')  # Part 2 answer


main()

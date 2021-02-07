from Utility import get_input
from collections import defaultdict, deque


def get_rooms():
    ans = []
    lines = get_input('line')
    for line in lines:
        checksum = line[-6:-1]
        line = line[:-7]
        sector = line[-3:]
        room = line[:-4]
        ans.append((room, sector, checksum))
    return ans


def sort_top_5(line):
    splits = defaultdict(list)
    for x in line:
        splits[x[1]].append(x)
    for values in splits.values():
        values.sort(key=lambda x: x[0])
    keyvals = [x for x in splits.keys()]
    keyvals.sort(reverse=True)
    ans = []
    for x in keyvals:
        ans += splits[x]
    super_ans = ''
    for x in ans:
        super_ans += x[0]
    return super_ans

def get_top_5(line):
    # Build dictionary of letter counts
    top_dict = dict()
    for letter in line:
        if letter.isalpha():
            top_dict[letter] = line.count(letter)
    tops = list(top_dict.items())
    tops = sort_top_5(tops)
    return tops[:5]

def is_room_real(room):
    line, sector, checksum = room
    common_chars = get_top_5(line)
    return checksum == common_chars


def get_real_rooms(codes):
    ans = []
    for room in codes:
        line, sector, checksum = room
        if is_room_real(room):
            ans.append(room)
    return ans


def sum_sector_ids(rooms):
    count = 0
    for r in rooms:
        count += int(r[1])
    return count


def get_alpha_deque(starting_letter):
    """Gets an alpha deq starting at that letter"""
    ans = deque()
    if starting_letter == '-':
        ans.append('-')
        return ans
    for letter in "abcdefghijklmnopqrstuvwxyz":
        ans.append(letter)
    while ans[0] != starting_letter:
        ans.rotate(1)
    return ans



def deqify_string(s):
    """Converts a string to a series of deques made of the alphabet"""
    ans = []
    for letter in s:
        ans.append(get_alpha_deque(letter))
    return ans


def uncode_string(deqed_string, sector_id):
    ans = ''
    for d in deqed_string:
        if d[0] == '-':
            ans += ' '
        else:
            d.rotate(-int(sector_id))
            ans += d[0]
    return ans



def decode_room_name(room):
    room, sectod_id, c = room
    room_string = deqify_string(room)
    ans = uncode_string(room_string, sectod_id)
    return ans



def main():
    codes = get_rooms()
    real_rooms = get_real_rooms(codes)
    print(f"Part 1 answer = {sum_sector_ids(real_rooms)}")
    for room in real_rooms:
        decoded = decode_room_name(room)
        if 'north' in decoded:
            print(f"Part 2 answer = {room[1]}")

if __name__ == '__main__':
    main()

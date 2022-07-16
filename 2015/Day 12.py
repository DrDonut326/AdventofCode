import json
from Functions import get_input


def add_up(data):
    assert data != None
    data_type = type(data)

    ans = 0
    # Check if data is a str
    if data_type == str:
        return 0

    elif data_type == int:
        return data

    # Not a string, list or dict?
    elif data_type == list:
        if len(data) == 0:
            return 0
        for element in data:
            ans += add_up(element)

    elif data_type == dict:
        if len(data.keys()) == 0:
            return 0
        for element in data.keys():
            if element.isdigit():
                ans += int(element)
            ans += add_up(data[element])
    else:
        raise ValueError("What are you?")

    return ans

def add_up_no_red(data):
    data_type = type(data)

    ans = 0
    # Check if data is a str
    if data_type == str:
        return 0

    elif data_type == int:
        return data

    # Not a string, list or dict?
    elif data_type == list:
        if len(data) == 0:
            return 0
        for element in data:
            ans += add_up_no_red(element)

    elif data_type == dict:
        # Gotta check for red
        if len(data.keys()) == 0:
            return 0
        # ----------- ****** RED CHECK RED CHECK ******** -----------
        for x in data.values():
            if x == 'red':
                return 0
        # ----------- ****** RED CHECK RED CHECK ******** -----------

        for element in data.keys():
            if element.isdigit():
                ans += int(element)
            ans += add_up_no_red(data[element])
    else:
        raise ValueError("What are you?")

    return ans


def main():
    puzzle_data = get_input('line')
    json_data = json.loads(puzzle_data[0])
    total = add_up(json_data)
    print(f"Part 1 answer = {total}")
    total2 = add_up_no_red(json_data)
    print(f"Part 2 answer = {total2}")

main()

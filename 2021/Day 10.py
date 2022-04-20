from Utility import get_input






def find_first_error(line):
    opens = "([{<"
    closes = ")]}>"
    open_stack = []
    matches = {')': '(', ']': '[', '}': '{', '>': '<'}

    for item in line:
        # If it's an opening bracket, put it in and add to stack
        if item in opens:
            open_stack.append(item)

        elif item in closes:
            # If it matches the last open, pop the stack and move on
            if matches[item] == open_stack[-1]:
                open_stack.pop()
            else:
                # If There's a closing bracket but it doesn't match the last one in open stack,
                # Then return that character as the first error
                return item
    return 'no error'

def test_stack(line):
    opens = "([{<"
    closes = ")]}>"
    open_stack = []
    matches = {')': '(', ']': '[', '}': '{', '>': '<'}

    for item in line:
        # If it's an opening bracket, put it in and add to stack
        if item in opens:
            open_stack.append(item)

        elif item in closes:
            # If it matches the last open, pop the stack and move on
            if matches[item] == open_stack[-1]:
                open_stack.pop()
            else:
                # If There's a closing bracket but it doesn't match the last one in open stack,
                # Then return that character as the first error
                return item
    return open_stack


def get_incomplete_lines(lines):
    ans = []
    for line in lines:
        if find_first_error(line) == 'no error':
            ans.append(line)
    return ans

def main():
    lines = get_input('line')
    points = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
        'no error': 0
    }
    incomplete_lines = get_incomplete_lines(lines)

    score_counts = []
    matches = {'(': ')', '[': ']', '{': '}', '<': '>'}
    for line in incomplete_lines:
        stack = test_stack(line)
        ending = [matches[x] for x in list(reversed(stack))]
        count = 0
        for e in ending:
            count *= 5
            count += points[e]
        score_counts.append(count)

    score_counts.sort()
    print(score_counts[len(score_counts) // 2])




main()

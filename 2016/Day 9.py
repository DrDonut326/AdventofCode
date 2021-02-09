from Utility import get_input


def decompress(s):
    i = 0
    ans = ''
    while i < len(s):
        if s[i] != '(':
            ans += s[i]
            i += 1
        else:
            # copy code
            code = ''
            i += 1
            while s[i] != ')':
                code += s[i]
                i += 1
            repeat_length, repeat_amount = [int(z) for z in code.split('x')]
            i += 1
            # Get repeat string
            r = s[i:i+repeat_length]
            # Add to the answer
            ans += r * repeat_amount
            # Jump to the end of the repeat length
            i += repeat_length
    return ans


def hyper_decompress(s, m):
    """Returns the length of a hyper decompressed string"""
    count = 0
    i = 0
    while i < len(s):
        if s[i] != '(':
            count += m
            i += 1
        else:
            # Found a multiplier
            # copy code
            code = ''
            i += 1
            while s[i] != ')':
                code += s[i]
                i += 1
            repeat_length, repeat_amount = [int(z) for z in code.split('x')]
            i += 1
            # Get repeat string
            r = s[i:i+repeat_length]
            # Increase the count by the recursion of that string
            # With the multiplier increased
            count += hyper_decompress(r, m * repeat_amount)
            # Move i forward
            i += repeat_length

    return count


def main():
    code = get_input('line')[0]
    decompressed_code = decompress(code)
    print(f"Part 1 answer = {len(decompressed_code)}")
    print(f"Part 2 answer = {hyper_decompress(code, 1)}")


if __name__ == '__main__':
    main()

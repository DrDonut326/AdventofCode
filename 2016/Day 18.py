def get_new_tile(a, b, c):
    if '^' not in [a, b, c]:
        return '.'
    if a == '^' and b == '^' and c == '.':
        return '^'
    if b == '^' and c == '^' and a == '.':
        return '^'
    if a == '^' and b == '.' and c == '.':
        return '^'
    if a == '.' and b == '.' and c == '^':
        return '^'
    return '.'


def build_next_row(tilemap):
    """Returns a dict map of tiles"""
    last_row = tilemap[-1]
    new_row = ''
    # Handle first character
    new_row += get_new_tile('.', last_row[0], last_row[1])
    # Handle middle characters
    for a, b, c in zip(last_row, last_row[1:], last_row[2:]):
        new_row += get_new_tile(a, b, c)
    # Handle last character
    new_row += get_new_tile(last_row[-2], last_row[-1], '.')
    return new_row


def print_tilemap(tilemap):
    for x in tilemap:
        print(x)


def count_safe(tilemap):
    count = 0
    for row in tilemap:
        for tile in row:
            if tile == '.':
                count += 1
    return count


def get_answer(puzzle_input, size):
    tilemap = [puzzle_input]
    for _ in range(size - 1):
        tilemap.append(build_next_row(tilemap))
    return count_safe(tilemap)


def main():
    puzzle_input = '.^^.^^^..^.^..^.^^.^^^^.^^.^^...^..^...^^^..^^...^..^^^^^^..^.^^^..^.^^^^.^^^.^...^^^.^^.^^^.^.^^.^.'
    print(f"Part 1 answer = {get_answer(puzzle_input, 40)}")
    print(f"Part 2 answer = {get_answer(puzzle_input, 400000)}")


if __name__ == '__main__':
    main()

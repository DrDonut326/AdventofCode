from collections import deque


class Elf:
    def __init__(self, recipe_index, scoreboard):
        self.recipe_index = recipe_index
        self.scoreboard = scoreboard

    def get_new_recipe_index(self):
        n = 1 + self.scoreboard[self.recipe_index] + self.recipe_index
        n = n % len(self.scoreboard)
        self.recipe_index = n % len(self.scoreboard)

class Kitchen:
    def __init__(self, scoreboard: list, puzzle_string='blah', part=1):
        self.scoreboard = scoreboard
        self.elf_a = Elf(0, scoreboard)
        self.elf_b = Elf(1, scoreboard)
        self.puzzle_string = puzzle_string
        self.part = part
        self.puzzle_len = len(self.puzzle_string)
        self.window = deque()  # Use to create a list of last appearing numbers

    def create_recipe(self):
        # Add current recipes
        combined_number = self.scoreboard[self.elf_a.recipe_index] + self.scoreboard[self.elf_b.recipe_index]

        # Add new
        if combined_number > 9:
            self.scoreboard.append(combined_number // 10)
            if self.part == 2:
                self.update_window()
        self.scoreboard.append(combined_number % 10)
        if self.part == 2:
            self.update_window()


    def update_elves(self):
        self.elf_a.get_new_recipe_index()
        self.elf_b.get_new_recipe_index()

    def update(self):
        self.create_recipe()
        self.update_elves()

    def display_inf(self):
        print(self.scoreboard)
        print(f"Elf a: ({self.scoreboard[self.elf_a.recipe_index]})   Elf b: [{self.scoreboard[self.elf_b.recipe_index]}]")

    def get_ten_after_n(self, n):
        x = self.scoreboard[n:n+10]
        return ''.join(str(z) for z in x)

    def is_x_in_recipes(self, x):
        check_string = ''.join([str(z) for z in self.scoreboard])
        return x in check_string

    def get_index_of_x(self, x):
        check_string = ''.join([str(z) for z in self.scoreboard])
        return check_string.index(x)

    def update_window(self):
        self.window.append(self.scoreboard[-1])
        if len(self.window) > self.puzzle_len:
            self.window.popleft()
        # Check for win
        stringy = ''.join([str(x) for x in list(self.window)])
        if stringy == self.puzzle_string:
            print(len(self.scoreboard) - len(self.puzzle_string))
            quit()


def part_1(puzzle_input):
    scoreboard = [3, 7]
    kitchen = Kitchen(scoreboard)

    recipe_repeat = puzzle_input
    while len(kitchen.scoreboard) < recipe_repeat + 10:
        kitchen.update()
    print(kitchen.get_ten_after_n(recipe_repeat))  # Part 1 answer


def part_2(puzzle_input):
    scoreboard = [3, 7]
    search_string = str(puzzle_input)
    kitchen = Kitchen(scoreboard, search_string, 2)
    # Program ends when part 2 answer is found
    while True:
        kitchen.update()

def main():
    puzzle_input = 556061
    part_1(puzzle_input)
    part_2(puzzle_input)



main()

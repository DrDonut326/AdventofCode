from itertools import combinations_with_replacement as comb
from Functions import get_input
from time import time


class Ingredient:
    def __init__(self, name, capacity, durability, flavor, texture, calories):
        self.name = name
        self.capacity = capacity
        self.durability = durability
        self.flavor = flavor
        self.texture = texture
        self.calories = calories


def get_flavors():
    ans = []
    lines = get_input('line', do_split=True, split_key=', ')
    for line in lines:
        name, capacity = line[0].split(': capacity ')
        capacity = int(capacity)

        durability = line[1].replace('durability ', '')
        durability = int(durability)

        flavor = line[2].replace('flavor ', '')
        flavor = int(flavor)

        texture = line[3].replace('texture ', '')
        texture = int(texture)

        calories = line[4].replace('calories ', '')
        calories = int(calories)

        ans.append(Ingredient(name, capacity, durability, flavor, texture, calories))
    return ans


def get_recipe_score(combination):
    capacity = 0
    durability = 0
    flavor = 0
    texture = 0
    calories = 0

    for c in combination:
        capacity += c.capacity
        durability += c.durability
        flavor += c.flavor
        texture += c.texture
        calories += c.calories

    if capacity < 0 or durability < 0 or durability < 0 or flavor < 0 or texture < 0:
        return 0, calories
    return capacity * durability * flavor * texture, calories


def main():
    flavors = get_flavors()
    combinations = comb(flavors, 100)
    total_combinations = 0
    start = time()

    high_score = 0
    high_score_lite = 0
    for c in combinations:
        total_combinations += 1
        score, calories = get_recipe_score(c)
        if score > high_score:
            high_score = score
        if calories == 500 and score > high_score_lite:
            high_score_lite = score
    print(f"Searched a total of {total_combinations} combinations in {time() - start} seconds")
    print(f"Part 1 answer: {high_score}")
    print(f"Part 2 answer: {high_score_lite}")


main()



# flavs = ['sugar', 'salt', 'caramel', 'flavor']
# x = comb(flavs, 5)


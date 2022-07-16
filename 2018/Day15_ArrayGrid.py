from math import inf

from Grids import ArrayGrid
from Pathfinding import bfs


class Creature:
    def __init__(self, race, pos: tuple, atk=3):
        self.race = race
        self.pos = pos
        self.hp = 200
        self.atk = atk
        self.state = 'ALIVE'

    def __repr__(self):
        return f"{self.race}@{self.pos}HP:{self.hp}"


class Battle:
    def __init__(self, grid: ArrayGrid, creature_dict, elf_stop=False):
        self.grid = grid
        self.creature_dict = creature_dict
        self.rounds = 0
        self.elf_stop = elf_stop  # Used to stop the simulation early if an elf dies
        self.elf_died = False

    def round(self):
        # Get a list of creatures objects for turn order
        turn_order = self.get_turn_order()

        # Each creature takes their turn
        for creature in turn_order:
            turn_result = self.take_turn(creature)

            # Test if combat is over
            if turn_result == 'DONE':
                return turn_result

        # After all turns are done increment the turn counter
        self.rounds += 1

    def take_turn(self, creature):
        # Make sure I'm alive
        if creature.hp <= 0:
            return
        # Identify enemy targets
        enemy_targets = self.get_enemey_targets(creature)

        # If there are no enemy targets, combat is over
        if not enemy_targets:
            return 'DONE'

        # Get a SET of open squares of targets
        open_squares = self.get_open_squares(enemy_targets)

        # Check to see if this creature is in range of an enemy adjacent square
        can_immediately_attack, attack_targets = self.is_adjacent_to_enemy_square(creature, enemy_targets)

        # If you can't then proceed to the move part
        if not can_immediately_attack:
            self.move(creature, open_squares)

            # After moving update the attack possibility status again
            can_immediately_attack, attack_targets = self.is_adjacent_to_enemy_square(creature, enemy_targets)

        # If you can attack, attack!
        if can_immediately_attack:
            return self.attack(creature, attack_targets)

    # -------------- MOVE ----------------------
    def move(self, creature: Creature, open_squares):

        # Which open squares can be reached in the fewest steps
        closest_squares = self.get_closest_open_squares(creature, open_squares)

        # If none, end turn
        if not closest_squares:
            return

        # Sort by reading order
        closest_squares.sort(key=lambda x: [x[1], x[0]])

        # The first position should be the one to step towards.
        x, y = closest_squares[0]

        # Create a cost_grid from the target
        target_cost_grid = bfs(self.grid, x, y)

        # Get this creatures cheapest next steps
        next_possible_steps = self.get_cheapest_next_steps(creature, target_cost_grid)

        # Sort by reading order
        next_possible_steps.sort(key=lambda x: [x[1], x[0]])

        # The step they will take should be the first one
        next_step = next_possible_steps[0]

        # Move to that step
        self.take_a_step(next_step, creature)


    def attack(self, creature, attack_targets):
        # Sort attack targets by lowest hp then reading order
        attack_targets.sort(key=lambda x: [x.hp, x.pos[1], x.pos[0]])

        attack_target = attack_targets[0]

        # Strike and check for deaths
        attack_target.hp -= creature.atk
        if attack_target.hp <= 0:
            return self.handle_death(attack_target)

    def is_adjacent_to_enemy_square(self, creature: Creature, enemy_targets):
        """Returns if this creature is immediately adjacent to an enemy creature
        and returns a list of such creature objects"""
        enemies = []
        # Iterate through enemy positions
        for enemy in enemy_targets:
            enemy_neighbors = self.grid.get_neighbors_4way(enemy.pos[0], enemy.pos[1])
            for enemy_pos in enemy_neighbors:
                if enemy_pos == creature.pos:
                    enemies.append(enemy)
        if enemies:
            return True, enemies
        else:
            return False, None

    def display_map(self):
        rgb = {'G': (255, 0, 0), 'E': (0, 255, 0)}
        self.grid.display_grid_with_highlighted_values(rgb)  # todo port to arraygrid

    def get_turn_order(self):
        order = []
        for creature in self.creature_dict.values():
            # Check if alive
            if creature.hp > 0:
                # Add to list
                order.append(creature)
        order.sort(key=lambda x: [x.pos[1], x.pos[0]])
        return order

    def get_enemey_targets(self, creature):
        """Get all living creatures that don't belong to this race."""
        return [x for x in self.creature_dict.values() if x.race != creature.race and x.hp > 0]

    def get_open_squares(self, enemy_targets):
        open_squares = set()
        for enemy in enemy_targets:
            # Get neighboring positions of that enemy
            neighbors = self.grid.get_neighbors_4way(enemy.pos[0], enemy.pos[1])

            # For each neighbor, if it lands on a '.', add it to the set
            for neighbor in neighbors:
                x, y = neighbor
                if self.grid.grid[y][x] == '.':
                    open_squares.add(neighbor)

        return open_squares


    def get_closest_open_squares(self, creature, open_squares):
        """Return a list of squares that are both reachable and tied for cheapest cost to reach"""
        ans = []
        cheapest_cost = inf

        # Get a new cost grid only as needed
        cost_grid = bfs(self.grid, creature.pos[0], creature.pos[1]) if open_squares else {}
        for open_pos in open_squares:
            if open_pos in cost_grid:
                travel_cost = cost_grid[open_pos]

                # New fastest square found
                if travel_cost < cheapest_cost:
                    ans = []
                    ans.append(open_pos)
                    cheapest_cost = travel_cost
                # Tie for fastest
                elif travel_cost == cheapest_cost:
                    ans.append(open_pos)
        return ans

    def get_cheapest_next_steps(self, creature: Creature, target_cost_grid):
        ans = []
        creature_neighbors = self.grid.get_neighbors_4way(creature.pos[0], creature.pos[1])
        cheapest_step = inf
        for pos in creature_neighbors:
            if pos in target_cost_grid:
                travel_cost = target_cost_grid[pos]
                if travel_cost < cheapest_step:
                    ans = []
                    ans.append(pos)
                    cheapest_step = travel_cost
                elif travel_cost == cheapest_step:
                    ans.append(pos)
        return ans

    def take_a_step(self, next_step, creature):
        # After taking a step, update all the dijkstra stuff as the map has changed!!

        # Mark this square as being empty
        self.grid.grid[creature.pos[1]][creature.pos[0]] = '.'

        # Remove the old creature dict entry
        del self.creature_dict[creature.pos]

        # Move the unit
        creature.pos = next_step

        # Update the new grid square
        self.grid.grid[creature.pos[1]][creature.pos[0]] = creature.race

        # Update the creature_dict entry
        self.creature_dict[creature.pos] = creature



    def handle_death(self, dead_creature):
        assert dead_creature.hp <= 0
        # Stop early if needed
        if self.elf_stop:
            if dead_creature.race == 'E':
                self.elf_died = True
                return 'DONE'
        # Change state
        dead_creature.state = 'DEAD'

        # Take this creature out of the creature dict
        del self.creature_dict[dead_creature.pos]

        # Update the map
        self.grid.grid[dead_creature.pos[1]][dead_creature.pos[0]] = '.'


    def finish_combat(self):
        if self.elf_died:
            return 'G', 0, self.rounds
        else:
            remaining_hp = sum([x.hp for x in self.creature_dict.values() if x.hp > 0])
            winning_race = [x for x in self.creature_dict.values()][0].race
            return winning_race, remaining_hp, self.rounds


def get_map():
    # Get 2D array
    grid = []
    with open("input.txt") as f:
        for line in f:
            line = line.rstrip()
            row = []
            for element in line:
                row.append(element)
            grid.append(row)

    # Make arraygrid
    ans = ArrayGrid(grid, {'#', 'G', 'E'})

    return ans


def get_creatures(grid, atk=3):
    creature_dict = dict()
    # Iterate through array and add any creatures you find
    for y, row in enumerate(grid.grid):
        for x, element in enumerate(row):
            if element == 'E':
                creature = Creature('E', (x, y), atk)
                creature_dict[(x, y)] = creature
            elif element == 'G':
                creature = Creature('G', (x, y), 3)
                creature_dict[(x, y)] = creature
    return creature_dict


def simulate_full_battle(atk=3, elf_stop=False):
    # Get Arraygrid of the input map
    grid = get_map()

    # Get a dictionary of creatures [(x, y)]: creature object
    creature_dict = get_creatures(grid, atk)

    # Get the battle object to control the battle
    battle = Battle(grid, creature_dict, elf_stop)

    # Run the battle until it is over
    done = False
    while not done:
        result = battle.round()
        if result == 'DONE':
            done = True
    winning_race, remaining_hp, rounds = battle.finish_combat()
    return winning_race, remaining_hp, rounds


def part_1():
    winning_race, remaining_hp, rounds = simulate_full_battle()
    print(f"Combat ends after {rounds}")
    print(f"{winning_race} win with {remaining_hp} total hit points left.")
    print(f"Outcome: {rounds} * {remaining_hp} = {rounds * remaining_hp}")
    print()


def part_2():
    elf_attack = 4
    winning_race, remaining_hp, rounds = simulate_full_battle(atk=elf_attack, elf_stop=True)
    while winning_race == 'G':
        elf_attack += 1
        winning_race, remaining_hp, rounds = simulate_full_battle(atk=elf_attack, elf_stop=True)
    print(f"Combat ends after {rounds}")
    print(f"{winning_race} win with {remaining_hp} total hit points left.")
    print(f"Outcome: {rounds} * {remaining_hp} = {rounds * remaining_hp}")
    print(f"Winning elf attack power was {elf_attack}")

def main():
    part_1()
    part_2()


main()

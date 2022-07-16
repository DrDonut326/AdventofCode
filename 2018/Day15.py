from Pathfinding import dijkstra
from Grids import DictGrid
from Pos import Pos
from math import inf


class Creature:
    def __init__(self, race, pos, atk=3):
        self.race = race
        self.pos = pos
        self.hp = 200
        self.atk = atk
        self.state = 'ALIVE'
        self.cost_grid = None

    def __repr__(self):
        return f"{self.race}@{self.pos}HP:{self.hp}"

    def set_cost_grid(self, grid):
        cost_grid = dijkstra(grid, self.pos)
        self.cost_grid = cost_grid


class Battle:
    def __init__(self, grid: DictGrid, creature_dict, elf_stop=False):
        self.grid = grid
        self.creature_dict = creature_dict
        self.rounds = 0
        self.update_all_cost_dicts()
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
        if len(enemy_targets) == 0:
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
        if len(closest_squares) == 0:
            return

        # Sort by reading order
        closest_squares.sort(key=lambda x: [x.y, x.x])

        # The first position should be the one to step towards.
        target_pos = closest_squares[0]

        # Create a cost_grid from the target
        target_cost_grid = dijkstra(self.grid, target_pos)

        # Get this creatures cheapest next steps
        next_possible_steps = self.get_cheapest_next_steps(creature, target_cost_grid)
        assert len(next_possible_steps) > 0  # Should be possible to get there

        # Sort by reading order
        next_possible_steps.sort(key=lambda x: [x.y, x.x])

        # The step they will take should be the first one
        next_step = next_possible_steps[0]

        # Move to that step and UPDATE ALL THE THINGS
        self.take_a_step(next_step, creature)


    def attack(self, creature, attack_targets):
        assert len(attack_targets) > 0
        # Sort attack targets by lowest hp then reading order
        attack_targets.sort(key=lambda x: [x.hp, x.pos.y, x.pos.x])

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
            enemy_neighbors = enemy.pos.get_neighbors_4way()
            for enemy_pos in enemy_neighbors:
                if enemy_pos == creature.pos:
                    enemies.append(enemy)
        if len(enemies) > 0:
            return True, enemies
        else:
            return False, None

    def display_map(self):
        rgb = {'G': (255, 0, 0), 'E': (0, 255, 0)}
        self.grid.display_grid_with_highlighted_values(rgb)

    def get_turn_order(self):
        order = []
        for creature in self.creature_dict.values():
            # Check if alive
            if creature.hp > 0:
                # Add to list
                order.append(creature)
        order.sort(key=lambda x: [x.pos.y, x.pos.x])
        return order

    def get_enemey_targets(self, creature):
        """Get all living creatures that don't belong to this race."""
        return [x for x in self.creature_dict.values() if x.race != creature.race and x.hp > 0]

    def get_open_squares(self, enemy_targets):
        open_squares = set()
        for enemy in enemy_targets:
            # Get neighboring positions of that enemy
            neighbors = enemy.pos.get_neighbors_4way()

            # For each neighbor, if it lands on a '.', add it to the set
            for neighbor in neighbors:
                if self.grid.grid[neighbor] == '.':
                    open_squares.add(neighbor)

        return open_squares

    def update_all_cost_dicts(self):
        for creature in self.creature_dict.values():
            creature.set_cost_grid(self.grid)

    def get_closest_open_squares(self, creature, open_squares):
        """Return a list of squares that are both reachable and tied for cheapest cost to reach"""
        ans = []
        cheapest_cost = inf

        for open_pos in open_squares:
            if open_pos in creature.cost_grid:
                traveL_cost = creature.cost_grid[open_pos]

                # New fastest square found
                if traveL_cost < cheapest_cost:
                    ans.clear()
                    ans.append(open_pos)
                    cheapest_cost = traveL_cost
                # Tie for fastest
                elif traveL_cost == cheapest_cost:
                    ans.append(open_pos)
        return ans

    def get_cheapest_next_steps(self, creature: Creature, target_cost_grid):
        ans = []
        creature_neighbors = creature.pos.get_neighbors_4way()
        cheapest_step = inf
        for pos in creature_neighbors:
            if pos in target_cost_grid:
                travel_cost = target_cost_grid[pos]
                if travel_cost < cheapest_step:
                    ans.clear()
                    ans.append(pos)
                    cheapest_step = travel_cost
                elif travel_cost == cheapest_step:
                    ans.append(pos)
        return ans

    def take_a_step(self, next_step, creature):
        # After taking a step, update all the dijkstra stuff as the map has changed!!

        # Mark this square as being empty
        self.grid.grid[creature.pos] = '.'

        # Remove the old creature dict entry
        del self.creature_dict[creature.pos]

        # Move the unit
        creature.pos = next_step

        # Update the new grid square
        self.grid.grid[creature.pos] = creature.race

        # Update the creature_dict entry
        self.creature_dict[creature.pos] = creature

        # Update all create cost dicts
        self.update_all_cost_dicts()

    def handle_death(self, dead_creature):
        assert dead_creature.hp <= 0
        # Stop early if needed
        if self.elf_stop:
            if dead_creature.race == 'E':
                print(f"Stopping early at round {self.rounds}")
                self.elf_died = True
                return 'DONE'
        # Change state
        dead_creature.state = 'DEAD'

        # Take this creature out of the creature dict
        del self.creature_dict[dead_creature.pos]

        # Update the map
        self.grid.grid[dead_creature.pos] = '.'

        # Update all cost dicts
        self.update_all_cost_dicts()

    def finish_combat(self):
        if self.elf_died:
            return 'G', 0, self.rounds
        else:
            remaining_hp = sum([x.hp for x in self.creature_dict.values() if x.hp > 0])
            winning_race = [x for x in self.creature_dict.values()][0].race
            return winning_race, remaining_hp, self.rounds


def get_map():
    grid = DictGrid(None, {'#', 'G', 'E'}, bounded=True)
    with open("input.txt") as f:
        for y, line in enumerate(f):
            line = line.rstrip()
            for x, element in enumerate(line):
                pos = Pos(x, y)
                grid.add_data_to_grid_at_pos(pos, element)
    return grid


def get_creatures(grid, atk=3):
    creature_dict = dict()
    for pos, element in grid.grid.items():
        if element == 'E':
            creature = Creature('E', pos, atk)
            creature_dict[pos] = creature
        elif element == 'G':
            creature = Creature('G', pos, 3)
            creature_dict[pos] = creature
    return creature_dict


def simulate_full_battle(atk=3, elf_stop=False):
    # Get everything from scratch

    # Get dictgrid of the input map
    grid = get_map()

    # Get a dictionary of creatures [pos]: creature object
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

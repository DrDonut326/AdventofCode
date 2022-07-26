class Army:
    def __init__(self, team, num_units, unit_hp, weaknesses, immunities, attack_type, attack_power, initiative, armies, group):
        self.team = team
        self.num_units = num_units
        self.unit_hp = unit_hp
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.attack_type = attack_type
        self.attack_power = attack_power
        self.initiative = initiative
        self.armies = armies
        self.target = None
        self.being_targetted_by = None
        self.alive = True
        self.group = group

    def __repr__(self):
        return f"{self.num_units} units each with {self.unit_hp} hit points (weak to {self.weaknesses}; immune to {self.immunities}) with an attack that does {self.attack_power} {self.attack_type} damage at initative {self.initiative}"

    def display_sort_data(self):
        print(f"{self.get_effective_power()}|{self.initiative}")

    def get_effective_power(self):
        return self.num_units * self.attack_power

    def select_target(self):
        assert self.alive
        # Among armies of the enemy team that have not already been targetted
        # And that are alive
        possible_targets = [t for t in self.armies if t.team != self.team and t.being_targetted_by == None and t.alive]

        # Check for no possible targets
        if not possible_targets:
            self.target = None
            return

        # Choose the target this army would deal the most damage to.
        possible_targets.sort(key=lambda x: (-x.simulate_being_attacked(self), -x.get_effective_power(), -x.initiative))


        # First in the list should be the most
        target = possible_targets[0]

        if target.simulate_being_attacked(self) == 0:
            self.target = None
        else:
            self.target = target
            self.target.being_targetted_by = self

    def simulate_being_attacked(self, enemy: 'Army'):
        assert self.alive
        assert enemy.alive
        """Returns what damage would occur if attacked by enemy."""
        if enemy.attack_type in self.immunities:
            return 0

        damage = enemy.get_effective_power()

        if enemy.attack_type in self.weaknesses:
            damage *= 2

        return damage

    def get_attacked(self, enemy: 'Army'):
        """Gets attacked by the enemy.  Returns how many units perished."""

        assert self.alive
        assert enemy.alive
        # Get damage to be sustained
        damage = self.simulate_being_attacked(enemy)

        # Get the amount of units to lose
        units_to_lose = damage // self.unit_hp   # use integer division to avoid remainders

        # If there was overkill, adjust it to the current number of units
        if units_to_lose > self.num_units:
            units_to_lose = self.num_units

        # Remove that many units
        self.num_units -= units_to_lose

        # Check for death
        if self.num_units <= 0:
            self.alive = False

        return units_to_lose

    def attack(self):
        """Attacks the currently selected target"""
        # Check to see if I'm still alive
        if self.alive:
            # Check to see if this army has a target
            if self.target is not None:
                units_lost = self.target.get_attacked(self)
                if debug:
                    print(f"{self.team} group {self.group} attacks defending group {self.target.group}, killing {units_lost} units")
                return units_lost
        return 0


class Battle:
    def __init__(self, armies: list[Army]):
        self.armies = armies
        self.deadlock_counter = 0

    def sort_for_target_selection(self):
        self.armies.sort(key=lambda x: (-x.get_effective_power(), -x.initiative))

    def sort_for_attack(self):
        self.armies.sort(key=lambda x: -x.initiative)

    def display_sort_data(self):
        for a in self.armies:
            a.display_sort_data()

    def carry_out_full_battle(self):
        done = False
        while not done:
            done = self.carry_out_round()
        result, remaining_health = self.display_battle_ending(done)
        return result, remaining_health

    def carry_out_round(self):
        # --- Print out starting information
        if debug:
            self.print_starting_information()

        # --- Target phase
        # Sort the armies for target selection
        self.sort_for_target_selection()

        # Select all targets
        for a in self.armies:
            a.select_target()

        # Print out targeting information
        if debug:
            self.print_targeting()

        # --- Attack phase
        # Sort for initiative
        self.armies.sort(key=lambda x: x.initiative, reverse=True)
        total_damage = 0
        for a in self.armies:
            total_damage += a.attack()

        if total_damage == 0:
            self.deadlock_counter += 1
            if self.deadlock_counter >= 10:
                return 'DEADLOCK', 0

        # After the dust settles
        # Prune all the dead armies away
        self.armies = [x for x in self.armies if x.alive]

        # Reset all targetting info to None
        for army in self.armies:
            army.target = None
            army.being_targetted_by = None

        # Return if the round is over or not
        result = self.is_battle_finished()
        # The winning team will be returned as a string, thus creating a true test
        if result:
            return result
        else:
            return False

    def print_starting_information(self):
        # Get immune system info
        print("Immune System:")

        # Get all immune armies sorted by group number
        immunes = [x for x in self.armies if x.team == 'Immune']

        # Sort by group number
        immunes.sort(key=lambda x: x.group)

        # Display starting strength
        for army in immunes:
            print(f"Group {army.group} contains {army.num_units} units")

        # Get infection system info
        print("Infection:")

        # Get all immune armies sorted by group number
        infections = [x for x in self.armies if x.team == 'Infection']

        # Sort by group number
        infections.sort(key=lambda x: x.group)

        # Display starting strength
        for army in infections:
            print(f"Group {army.group} contains {army.num_units} units")

    def print_targeting(self):
        # Print blank line
        print()
        infections = [x for x in self.armies if x.team == 'Infection']
        infections.sort(key=lambda x: x.group)
        immunes = [x for x in self.armies if x.team == 'Immune']
        immunes.sort(key=lambda x: x.group)

        # Infection possible damaging
        for i in infections:
            for enemy in immunes:
                if enemy.simulate_being_attacked(i) != 0:
                    print(f"Infection group {i.group} would deal defending group {enemy.group} {enemy.simulate_being_attacked(i)} damage")

        # Immune possible damaging
        for i in immunes:
            for enemy in infections:
                if enemy.simulate_being_attacked(i) != 0:
                    print(
                        f"Immune System group {i.group} would deal defending group {enemy.group} {enemy.simulate_being_attacked(i)} damage")
        print()

    def is_battle_finished(self):
        """Returns False if both sides have units.
        Returns the name of the winning side if otherwise."""
        infections = [x for x in self.armies if x.team == 'Infection']
        immunes = [x for x in self.armies if x.team == 'Immune']



        if not infections:
            return 'IMMUNE'

        elif not immunes:
            return 'INFECTION'
        else:
            return False

    def display_battle_ending(self, done):
        # Sort armies by group
        self.armies.sort(key=lambda x: x.group)

        if debug:

            print(f"Immune System:")
            if done == 'INFECTION':
                print("No groups remain.")
            else:
                for army in self.armies:
                    print(f"Group {army.group} contains {army.num_units} units")

            print("Infection:")
            if done == 'IMMUNE':
                print("No groups remain.")
            else:
                for army in self.armies:
                    print(f"Group {army.group} contains {army.num_units} units")

            # Print the sum of all remaining units
            print(f"Remaining units total: {sum([x.num_units for x in self.armies])}")

        return done, sum([x.num_units for x in self.armies])


def get_armies(boost=0):
    armies = []
    group_counter = 0
    with open("input.txt") as f:
        # Get the first army
        team_1 = f.readline().rstrip().split(' ')[0]
        line = f.readline()
        while line != '\n':
            group_counter += 1
            line = line.rstrip()

            # Check for immunities or weaknesses
            if '(' in line:
                unit_info, right = line.split('(')
                weaknesses_immunities, attack = right.split(') with an attack that does ')
                attack, initative = attack.split(' damage at ')

                # Unit number and health
                unit_info = unit_info.split(' ')
                num_units = int(unit_info[0])
                unit_hp = int(unit_info[4])

                # Weaknesses and immunities
                stat_dict = get_immune_and_weak(weaknesses_immunities)

                # Attack power and type
                attack_power, atk_type = attack.split(' ')
                attack_power = int(attack_power) + boost
                initative = initative.split(' ')[1]
                initative = int(initative)

            else:
                line = line.split(' ')
                num_units = int(line[0])
                unit_hp = int(line[4])
                stat_dict = {'immune': [], 'weak': []}
                atk_type = line[13]
                attack_power = int(line[12]) + boost
                initative = int(line[-1])

            army = Army(team_1, num_units, unit_hp, stat_dict['weak'], stat_dict['immune'], atk_type, attack_power,\
                        initative, armies, group_counter)
            armies.append(army)

            line = f.readline()

        team_2 = f.readline().rstrip().replace(':', '')
        group_counter = 0
        for line in f:
            group_counter += 1
            line = line.rstrip()
            unit_info, right = line.split('(')
            weaknesses_immunities, attack = right.split(') with an attack that does ')
            attack, initative = attack.split(' damage at ')

            # Unit number and health
            unit_info = unit_info.split(' ')
            num_units = int(unit_info[0])
            unit_hp = int(unit_info[4])

            # Weaknesses and immunities
            stat_dict = get_immune_and_weak(weaknesses_immunities)

            # Attack power and type
            attack_power, atk_type = attack.split(' ')
            attack_power = int(attack_power)

            initative = initative.split(' ')[1]
            initative = int(initative)

            army = Army(team_2, num_units, unit_hp, stat_dict['weak'], stat_dict['immune'], atk_type, attack_power,
                        initative, armies, group_counter)
            armies.append(army)
    return armies


def get_immune_and_weak(s: str):
    ans = {'immune': [], 'weak': []}
    if ';' in s:
        # Multiple types, need to split
        left, right = s.split('; ')
        middle_status(ans, left)
        middle_status(ans, right)
    else:
        middle_status(ans, s)
    return ans


def middle_status(stat_dict, s):

    if s.startswith('weak'):
        s = s.replace('weak to ', '')
        add_status(stat_dict, 'weak', s)
    else:
        s = s.replace('immune to ', '')
        add_status(stat_dict, 'immune', s)


def add_status(stat_dict: dict, stat_type: str, s: str):
    # If commas, split the string
    if ',' in s:
        multiple = s.split(', ')
        for m in multiple:
            stat_dict[stat_type].append(m)
    else:
        stat_dict[stat_type].append(s)


def part_1():
    armies = get_armies()
    battle = Battle(armies)
    result, remaining_health = battle.carry_out_full_battle()
    print(result, remaining_health)


def part_2():
    result = 'INFECTION'
    boost = 0
    while result == 'INFECTION' or result == 'DEADLOCK':
        boost += 1
        armies = get_armies(boost)
        battle = Battle(armies)
        result, remaining_health = battle.carry_out_full_battle()
        if type(result) == tuple:
            result = result[0]


    print(boost, remaining_health)


def main():
    part_1()
    part_2()



debug = False
main()


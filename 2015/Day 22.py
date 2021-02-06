from collections import deque


class Player:
    def __init__(self):
        self.hp = 50
        self.mana = 500
        self.shield = False
        self.shield_timer = 0
        self.recharge = False
        self.recharge_timer = 0

    def update(self):
        """Updates status effects"""
        if self.shield:
            self.shield_timer -= 1
            if self.shield_timer == 0:
                self.shield = False
        if self.recharge:
            self.recharge_timer -= 1
            self.mana += 101
            if self.recharge_timer == 0:
                self.recharge = False


class Boss:
    def __init__(self):
        self.hp = 71
        self.damage = 10
        self.poison = False
        self.poison_timer = 0

    def update(self):
        """Updates status effects"""
        if self.poison:
            self.hp -= 3
            self.poison_timer -= 1
            if self.poison_timer == 0:
                self.poison = False


def take_player_turn(player, boss, spell, hard=False):
    spell_cost_dict = {
        'magic missile': 53,
        'drain': 73,
        'shield': 113,
        'poison': 173,
        'recharge': 229
    }

    if hard:
        player.hp -= 1
        if player.hp <= 0:
            return 'lose'

    player.update()
    boss.update()

    if boss.hp <= 0:
        return 'win'

    if player.mana < spell_cost_dict[spell]:
        return 'lose'

    # Cast spell
    if spell == 'magic missile':
        player.mana -= 53
        boss.hp -= 4
    elif spell == 'drain':
        player.mana -= 73
        boss.hp -= 2
        player.hp += 2
    elif spell == 'shield':
        player.mana -= 113
        player.shield = True
        player.shield_timer = 6
    elif spell == 'poison':
        player.mana -= 173
        boss.poison = True
        boss.poison_timer = 6
    elif spell == 'recharge':
        player.mana -= 229
        player.recharge = True
        player.recharge_timer = 5
    else:
        raise ValueError('Unknown spell cast.')

    if boss.hp <= 0:
        return 'win'


def take_boss_turn(player, boss):
    player.update()
    boss.update()

    if boss.hp <= 0:
        return 'win'
    hit = boss.damage
    if player.shield:
        hit -= 7
    if hit <= 0:
        hit = 1
    player.hp -= hit
    if player.hp <= 0:
        return 'lose'
    return 'draw'


def simulate_turn_path(spell_list, explored, hard=False):
    explored.add(str(spell_list))
    """'win', 'draw', 'lose'"""
    player = Player()
    boss = Boss()

    for spell in spell_list:
        result = take_player_turn(player, boss, spell, hard)
        if result == 'win':
            return result
        if result == 'lose':
            return result

        result = take_boss_turn(player, boss)
        if result == 'win':
            return result
        if result == 'lose':
            return result

    # Run out of spells, try again
    return 'draw'


def get_answer(starting_spells, hard=False):
    queue = deque()
    explored = set()
    to_explore = deque()
    for spell in starting_spells:
        queue.append([spell])

    while len(queue) > 0:
        test_path = queue.popleft()

        # Test to see if this path wins
        # If it does win, should??? be the cheapest path to victory
        result = simulate_turn_path(test_path, explored, hard)
        if result == 'win':
            return test_path
        elif result == 'draw':
            # Not finished with this path, need to mutate it more
            # Mutate the paths
            mutants = []
            for spell in starting_spells:
                t = test_path.copy()
                t.append(spell)
                assert str(t) not in explored
                mutants.append(t)
            # Put the mutants in the queue
            for m in mutants:
                to_explore.append(m)
        else:
            assert result == 'lose'

        if len(queue) == 0 and len(to_explore) > 0:
            while len(to_explore) > 0:
                queue.append(to_explore.popleft())
            to_explore.clear()


def count_spell_mana(path):
    ans = 0
    spell_cost_dict = {
        'magic missile': 53,
        'drain': 73,
        'shield': 113,
        'poison': 173,
        'recharge': 229
    }
    for spell in path:
        ans += spell_cost_dict[spell]
    return ans



def main():
    spell_list = ['magic missile', 'drain', 'shield', 'poison', 'recharge']

    ans = get_answer(spell_list)
    cost = count_spell_mana(ans)

    print(f"Part 1 Winning list was: {ans}")
    print(f"Part 1 Total mana cost: {cost}")
    print()

    ans = get_answer(spell_list, hard=True)
    cost = count_spell_mana(ans)

    print(f"Part 2 Winning List was: {ans}")
    print(f"Part 2 Total mana cost: {cost}")



main()

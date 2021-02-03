from itertools import combinations as comb


class Shop:
    def __init__(self):
        self.weapons = []
        self.armor = []
        self.rings = []

    def make_ring_combos(self):
        """Returns all combinations of rings"""
        ans = []
        combos = comb(self.rings, 2)
        for c in combos:
            ans.append(c)
        ans.sort(key=lambda x: x[0].cost + x[1].cost)
        for a, b in zip(ans, ans[1:]):
            if b[0].cost + b[1].cost < a[0].cost + a[1].cost:
                raise ValueError('rings not sorted')
        self.rings = ans

    def dump_inventory(self):
        for w in self.weapons:
            print(w.name, w. cost, w.dam, w.arm)
            print()
        for w in self.armor:
            print(w.name, w. cost, w.dam, w.arm)
            print()
        for a, b in self.rings:
            print(a.name, b.name)


class Item:
    def __init__(self, name, equip_type, cost, dam, arm):
        self.name = name
        self.equip_type = equip_type
        self.cost = cost
        self.dam = dam
        self.arm = arm


class Character:
    def __init__(self, name, power=0, toughness=0):
        self.name = name
        self.equipment = []
        self.gold = 0
        self.hp = 100
        self.power = power
        self.toughness = toughness

    def attack(self, target):
        atk_power = self.power
        for item in self.equipment:
            atk_power += item.dam
        target.receive_attack(atk_power)

    def receive_attack(self, atk_power):
        def_power = self.toughness
        for item in self.equipment:
            def_power += item.arm
        atk_power -= def_power
        if atk_power <= 0:
            atk_power = 1
        self.hp -= atk_power

    def get_price_of_inventory(self):
        ans = 0
        for x in self.equipment:
            ans += x.cost
        return ans


def build_item_shop():
    shop = Shop()
    with open("input.txt") as f:
        f.readline()
        for _ in range(5):
            line = f.readline().rstrip()
            line = ' '.join(line.split())
            name, cost, damage, armor = line.split(' ')
            shop.weapons.append(Item(name, 'weapon', int(cost), int(damage), int(armor)))

        f.readline()
        f.readline()
        shop.armor.append(Item('Nothing', 'armor', 0, 0, 0))
        for _ in range(5):
            line = f.readline().rstrip()
            line = ' '.join(line.split())
            name, cost, damage, armor = line.split(' ')
            shop.armor.append(Item(name, 'armor', int(cost), int(damage), int(armor)))

        f.readline()
        f.readline()
        shop.rings.append(Item('Nothing1', 'ring', 0, 0, 0))
        shop.rings.append(Item('Nothing2', 'ring', 0, 0, 0))
        for _ in range(6):
            line = f.readline().rstrip()
            line = line.replace(' ', '', 1)
            line = ' '.join(line.split())
            name, cost, damage, armor = line.split(' ')
            shop.rings.append(Item(name, 'ring', int(cost), int(damage), int(armor)))

    shop.rings.sort(key=lambda x: x.cost)
    shop.make_ring_combos()
    return shop


def fight(player, boss):
    """Fights to the death.
    Returns True if the player wins"""
    while True:
        player.attack(boss)
        if boss.hp <= 0:
            return True
        boss.attack(player)
        if player.hp <= 0:
            return False


def all_equipment_combos_generator(shop):
    # Iterate through swords, which are mandatory
    for w in shop.weapons:
        for a in shop.armor:
            for ring_combo in shop.rings:
                yield w, a, ring_combo[0], ring_combo[1]


def display_equipment_combo(c):
    for x in c:
        print(x.name)


def main():
    shop = build_item_shop()
    equipment_giver = all_equipment_combos_generator(shop)

    cheap_win = 99999999
    expensive_loss = 0
    for equip in equipment_giver:
        player = Character('player', 0, 0)
        boss = Character('boss', 8, 2)
        player.equipment = equip
        fight_result = fight(player, boss)
        if fight_result:
            g = player.get_price_of_inventory()
            if g < cheap_win:
                cheap_win = g
        else:
            g = player.get_price_of_inventory()
            if g > expensive_loss:
                expensive_loss = g

    print(f"The cheapest win was {cheap_win}.")
    print(f"The most expensive loss was {expensive_loss}.")


main()

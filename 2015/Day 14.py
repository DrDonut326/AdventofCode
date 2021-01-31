from Utility import get_input


class Reindeer:
    def __init__(self, name, speed, stamina, rest_time):
        self.name = name
        self.speed = speed
        self.stamina = stamina
        self.rest_time = rest_time
        self.resting = False
        self.timer = self.stamina
        self.distance_traveled = 0
        self.points = 0

    def info(self):
        print(f"{self.name}: SPD:{self.speed} STAM:{self.stamina} REST: {self.rest_time}")
        print(f" Distance Travel: {self.distance_traveled}")

    def update(self):
        if self.resting:
            self.timer += 1
            if self.timer == self.rest_time:
                self.resting = False
                self.timer = self.stamina
        else:
            self.distance_traveled += self.speed
            self.timer -= 1
            if self.timer == 0:
                self.resting = True


def get_deer():
    ans = []
    lines = get_input('line')
    for line in lines:
        left, right = line.split(' seconds, but then must rest for ')

        # name and speed
        name, t = left.split(' can fly ')
        speed, stamina = t.split(' km/s for ')

        # Rest
        rest_time = right.replace(" seconds.", '')

        speed = int(speed)
        stamina = int(stamina)
        rest_time = int(rest_time)

        ans.append(Reindeer(name, speed, stamina, rest_time))
    return ans


def award_points(reindeer_list):
    best = max(reindeer_list, key= lambda x: x.distance_traveled).distance_traveled
    for r in reindeer_list:
        if r.distance_traveled == best:
            r.points += 1

def main():
    reindeer_list = get_deer()
    for _ in range(2503):
        for r in reindeer_list:
            r.update()
        award_points(reindeer_list)
    print(f"Part 1 answer = {max(reindeer_list, key=lambda x: x.distance_traveled).distance_traveled}")
    print(f"Part 2 answer = {max(reindeer_list, key=lambda x: x.points).points}")

main()

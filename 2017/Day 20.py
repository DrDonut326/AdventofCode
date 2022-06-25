from collections import defaultdict
from dataclasses import dataclass


class Starfield:
    def __init__(self, particles):
        self.particles = particles
        self.locations = defaultdict(list)

    def update(self):
        # Clear locations dict
        self.locations = defaultdict(list)

        # Update positions
        for p in self.particles:
            p.update()
            self.locations[p.get_pos_key()].append(p)

        # Check for collisions
        # Iterate through locations data and only take single length ones
        new_particles = []
        for location in self.locations.values():
            if len(location) == 1:
                new_particles.append(location[0])

        # See as current particles
        self.particles = new_particles

    def get_closest_to_origin(self):
        winner = None
        winner_name = None
        for p in self.particles:
            m = p.dist()
            if winner is None or m < winner:
                winner = m
                winner_name = p.name
        return winner_name

    def simulate(self, n):
        """Runs for n rounds"""
        for _ in range(n):
            self.update()



@dataclass
class Particle:
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int
    ax: int
    ay: int
    az: int
    name: int

    def update(self):
        # Update acceleration
        self.vx += self.ax
        self.vy += self.ay
        self.vz += self.az

        # Update position
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    def dist(self):
        """Return manhat dist."""
        return abs(self.x) + abs(self.y) + abs(self.z)

    def get_pos_key(self):
        return f"x{self.x}y{self.y}z{self.z}"


def get_particles():
    ans = []
    name = 0
    with open("input.txt") as f:
        for line in f:
            line = line.rstrip()
            line = line.split(', ')
            p, v, a = [x[3:-1] for x in line]

            p = [int(x) for x in p.split(',')]
            v = [int(x) for x in v.split(',')]
            a = [int(x) for x in a.split(',')]

            ans.append(Particle(p[0], p[1], p[2], v[0], v[1], v[2], a[0], a[1], a[2], name))
            name += 1
    return ans


def main():
    particles = get_particles()
    starfield = Starfield(particles)
    starfield.simulate(10000)
    print(starfield.get_closest_to_origin())  # Part 1 answer
    print(len(starfield.particles)) # Part 2 answer


main()

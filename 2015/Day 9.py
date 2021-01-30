from collections import defaultdict
from GetInput import get_input
from queue import Queue


class Route:
    def __init__(self, departure, destination, distance):
        self.departure = departure
        self.destination = destination
        self.distance = distance

    def info(self):
        print(f"{self.departure} to {self.destination} is {self.distance} units long.")


def get_routes():
    data = get_input('line')
    routes = defaultdict(list)

    for line in data:
        cities, distance = line.split(' = ')
        distance = int(distance)
        departure, destination = cities.split(' to ')

        routes[departure].append(Route(departure, destination, distance))
        routes[destination].append(Route(destination, departure, distance))

    return routes


def get_all_possible_routes(routes):
    # Prepare the explore queue
    explore = Queue()
    ans = []
    for city in routes:
        explore.put([city])

    # Pop off queue.  If that route is full, put it in the answer list
    while not explore.empty():
        route = explore.get()
        if len(route) == len(routes.keys()):
            ans.append(route)
        else:
            # Find all cities not in that route
            for city in routes:
                if city not in route:
                    t = route.copy()
                    t.append(city)
                    explore.put(t)
    return ans


def distance_from_a_to_b(routes, a, b):
    destination_objects = routes[a]
    for d in destination_objects:
        if d.departure == a and d.destination == b:
            return d.distance


def main():
    routes = get_routes()
    all_routes = get_all_possible_routes(routes)
    distances = set()
    for r in all_routes:
        total = 0
        for a, b in zip(r, r[1:]):
            total += distance_from_a_to_b(routes, a, b)
        distances.add(total)

    print(f"Part 1 answer is {min(distances)}")
    print(f"Part 2 answer is {max(distances)}")


main()

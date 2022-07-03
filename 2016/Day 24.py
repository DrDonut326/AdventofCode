from Pos import Pos
from Grids import DictGrid
from random import choice, randint
from time import sleep
from itertools import permutations, combinations
import os
from copy import deepcopy


# TODO: Check if step dict is actually finishing. Optimize it.

class Crawler:
    """Crawls around the grid trying to collect all numbers"""
    def __init__(self, pos: Pos, grid: DictGrid, visited: set):
        self.pos = pos
        self.grid = grid
        self.visited = visited
        self.visited.add(self.pos)
        self.numbers_found = set()
        self.state = 'exploring'
        self.steps = 0
        self.goal_nums = ['1', '2', '3', '4']
        self.path = []  # Treat like a stack
        self.rgb = (randint(0, 255), randint(0, 255), randint(0, 255))

    def clone(self):
        c = Crawler(Pos(self.pos.x, self.pos.y), self.grid, deepcopy(self.visited))
        c.numbers_found = deepcopy(self.numbers_found)
        c.state = self.state
        c.steps = self.steps
        c.path = deepcopy(self.path)
        return c

    def find_all_nums_step(self):
        # First always look down and check for numbers. Finish if done
        see = self.look_down()
        if see in self.goal_nums:
            self.numbers_found.add(see)
            if len(self.numbers_found) == len(self.goal_nums):
                return self.steps

        # ----- if exploring
        if self.state == 'exploring':
            # Get unvisited neighbors
            neighbors = self.get_neighbors()

            # If one spot, move there
            if len(neighbors) == 1:
                self.pos = neighbors[0]
                self.steps += 1
                self.path.append(self.pos)
                self.visited.add(self.pos)

            # If more than one spot, clone yourself as much as needed
            elif len(neighbors) > 1:

                # Make clones
                my_clones = []
                for _ in range(len(neighbors) - 1):
                    my_clones.append(self.clone())

                # Then take one direction
                prime_pos = neighbors.pop()  # No change pos after cloning
                self.pos = prime_pos
                self.steps += 1
                self.path.append(self.pos)
                self.visited.add(self.pos)


                assert len(my_clones) == len(neighbors)
                # Other clone (or clones) take other directions
                for c, n in zip(my_clones, neighbors):
                    c.pos = n
                    c.steps += 1
                    c.path.append(c.pos)
                    c.visited.add(c.pos)
                    clones.append(c)

            # If you reach a dead end (no unexplored neighbors) switch to backtrack mode
            elif len(neighbors) == 0:
                # Remove the current path pos
                self.path.pop()

                # Move to the last known place
                self.pos = self.path.pop()
                self.steps += 1

                # Switch state to backtracking
                self.state = 'backtracking'

            else:
                # Weird thing happening with neighbors?
                raise EnvironmentError("Neighbors list has no length?")


        # ----- if backtracking
        elif self.state == 'backtracking':

            # Travel backwards until you come to an unexplored node
            neighbors = self.get_neighbors()

            # If backtracking and come to an unexplored node, switch to exploring mode
            if len(neighbors) > 0:
                # Change state to exploring and run this function again
                self.state = 'exploring'
                self.find_all_nums_step()

            else:
                # Make sure there is path to backtrack.
                assert len(self.path) > 0

                # Nothing new, keep backtracking
                self.pos = self.path.pop()
                self.steps += 1

    def take_step(self):
        """Tries to explore unexplores squares.  If dead ends, switches to backtrack."""
        pass

    def look_down(self):
        return self.grid.get_value_from_pos_object(self.pos)

    def get_neighbors(self):
        # Get basic neighbors
        neighbors = self.grid.get_neighbors_4way(self.pos, exist=True, wall='#')

        # Prune visited
        ans = []
        for n in neighbors:
            if n not in self.visited:
                ans.append(n)
        return ans


class PathFinder(Crawler):
    def __init__(self, pos: Pos, finish: Pos, grid: DictGrid, visited: set):
        super().__init__(pos, grid, visited)
        self.finish = finish

    def clone(self):
        c = PathFinder(Pos(self.pos.x, self.pos.y), self.finish, self.grid, deepcopy(self.visited))
        c.numbers_found = deepcopy(self.numbers_found)
        c.state = self.state
        c.steps = self.steps
        c.path = deepcopy(self.path)
        return c

    def find_path_step(self):
        # Check if current pos is the goal pos
        if self.pos == self.finish:
            return self.steps

        # ----- if exploring
        if self.state == 'exploring':
            # Get unvisited neighbors
            neighbors = self.get_neighbors()

            # If one spot, move there
            if len(neighbors) == 1:
                self.pos = neighbors[0]
                self.steps += 1
                self.path.append(self.pos)
                self.visited.add(self.pos)

            # If more than one spot, clone yourself as much as needed
            elif len(neighbors) > 1:

                # Make clones
                my_clones = []
                for _ in range(len(neighbors) - 1):
                    my_clones.append(self.clone())

                # Then take one direction
                prime_pos = neighbors.pop()  # No change pos after cloning
                self.pos = prime_pos
                self.steps += 1
                self.path.append(self.pos)
                self.visited.add(self.pos)


                assert len(my_clones) == len(neighbors)
                # Other clone (or clones) take other directions
                for c, n in zip(my_clones, neighbors):
                    c.pos = n
                    c.steps += 1
                    c.path.append(c.pos)
                    c.visited.add(c.pos)
                    clones.append(c)

            # If you reach a dead end just die, because the shortest path won't involve backtracking
            elif len(neighbors) == 0:
                self.state = 'dead'

            else:
                # Weird thing happening with neighbors?
                raise EnvironmentError("Neighbors list has no length?")


def get_grid(walls):
    grid = DictGrid(walls=walls, datatype=str, bounded=True)
    with open('input.txt') as f:
        lines = []
        for line in f:
            lines.append(line.rstrip())

    for y, row in enumerate(lines):
        for x, element in enumerate(row):
            pos = Pos(x, y)
            grid.add_data_to_grid_at_pos(pos, element)

    grid.set_size()

    return grid


def clear():
    os.system('cls')


def colored(r, g, b, text):
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"


def display_crawlers(grid):
    min_x, max_x, min_y, max_y = grid.get_graph_min_max()
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            t = Pos(x, y)
            if t in grid.grid:
                to_print = grid.grid[t]
                # Check for crawler
                for c in crawlers:
                    if c.pos == t:
                        # Print this crawler's color
                        r, g, b = c.rgb
                        to_print = colored(r, g, b, '@')
                print(to_print, end='')
            else:
                print('.', end='')
        print()


def all_take_1_step(grid):
    # Iterate crawlers
    for crawl in crawlers:
        result = crawl.find_all_nums_step()
        if result is not None:
            return result

    # Add clones
    for crawl in clones:
        crawlers.append(crawl)
    clones.clear()


def get_pos_of_all_POI(grid):
    ans = []
    for item in grid.grid.items():
        pos, value = item
        if value.isnumeric():
            ans.append(pos)
    return ans


def get_travels_lists(POI_list, start):
    ans = []

    # Get combinations of POIs
    perms = permutations(POI_list, len(POI_list))

    # Insert start to the beginning of each one
    for p in perms:
        travel = [start]
        for pos in p:
            travel.append(pos)
        ans.append(travel)

    return ans


def get_POI_parts(POI_list):
    """Returns a list of pairs of POIs."""
    # No repeating element.  Be sure to to A -> B and also B -> A
    combs = combinations(POI_list, 2)
    return combs


def get_shortest_steps(a, b, grid):
    assert type(a) == Pos
    assert type(b) == Pos
    pathfinders.clear()
    clones.clear()

    pathfinder = PathFinder(a, b, grid, set())
    pathfinders.append(pathfinder)

    result = None
    while result is None:
        # Update pathfinders
        for p in pathfinders:
            result = p.find_path_step()
            if result is not None:
                break

        # Remove dead pathfinders
        t = [x for x in pathfinders if x.state != 'dead']

        # Add clones in
        for c in clones:
            t.append(c)

        # Wipe clones and pathfinders
        pathfinders.clear()
        clones.clear()

        # Re-add
        for p in t:
            pathfinders.append(p)

    return result


def get_shortest_path_dict(pairs, grid):
    """Returns a dict of how many steps it takes to get from a to b
    Dict key is a b concatenated."""
    ans = dict()
    a: Pos
    b: Pos
    for pair in pairs:
        a, b = pair
        steps = grid.dijkstra(a, b, all_cost=1)
        # Add both versions
        ab_key = str(a) + ' ' + str(b)
        ba_key = str(b) + ' ' + str(a)
        ans[ab_key] = steps
        ans[ba_key] = steps
    return ans


def find_smallest_steps(travel_lists, step_dict):
    best = None
    best_travel = None
    for t in travel_lists:
        count = 0
        for a, b in zip(t, t[1:]):
            count += step_dict[str(a) + ' ' + str(b)]
        if best is None or count < best:
            best = count
            best_travel = t
    return best, best_travel


def find_zero(grid):
    for key, value in grid.grid.items():
        if value == '0':
            return grid.get_pos_object_from_value('0')


def main():
    walls = set('#')
    grid = get_grid(walls)

    # Get all points of interest
    POI_list = get_pos_of_all_POI(grid)

    # Get shortest path between all POIs in the grid
    POI_pair_list = get_POI_parts(POI_list)
    step_dict = get_shortest_path_dict(POI_pair_list, grid)

    # Get start and remove it from POIs
    start_pos = find_zero(grid)
    POI_list.remove(start_pos)

    # Get all combinations of travel between POIs
    travel_lists = get_travels_lists(POI_list, start_pos)

    # smallest_total_steps, best_travel = find_smallest_steps(travel_lists, step_dict)

    #print(best_travel)
    #print(smallest_total_steps)  # Part 1 answer

    # -------- Part 2 ----------
    # Append start to the end of all travel lists
    new_travel_lists = []
    for t in travel_lists:
        t.append(start_pos)
        new_travel_lists.append(t)

    smallest_total_steps, best_travel = find_smallest_steps(new_travel_lists, step_dict)

    print(best_travel)
    print(smallest_total_steps)  # Part 2 answer


main()


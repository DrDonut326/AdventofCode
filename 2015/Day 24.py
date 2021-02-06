from Utility import get_input, factors


def greedily_get_not_explored_list(path, nums, k, explored):
    """Gets the next path of integers that sum to k
    that haven't yet been explored yet"""

    # If the path sums to k, return it as a success!
    if sum(path) == k:
        return path, nums

    # If the length is zero, that's no good
    if len(nums) == 0:
        return False

    # If the sum is greater than the total, we can stop looking
    if sum(path) > k:
        return False

    # Find the biggest path that isn't searched yet
    for x in nums:
        # Iterate through the remaining numbers
        # Copy the path to not mess up the original
        t_path = path.copy()
        t_nums = nums.copy()
        t_path.append(x)

        # Check to see if it has been explored
        if str(t_path) not in explored:
            # hash as a string
            explored.add(str(t_path))
            # Remove the number added
            t_nums.remove(x)
            # Send it back in to check
            result = greedily_get_not_explored_list(t_path, t_nums, k, explored)
            if result is not False:
                return result


def get_all_ways(nums, k, explored):
    """Gets all the ways to sum up to k with the given nums"""
    ans = []
    result = 'poop'
    # Cycles through until greedy can't find any more
    while result is not None:
        if result != 'poop':  # All my code is poop
            ans.append(result)
        path = []
        t = nums.copy()
        result = greedily_get_not_explored_list(path, t, k, explored)
    return ans


def part1(weights, sum_weights, num_splits):
    # Get the goal balance of all sides
    k = sum_weights / num_splits
    # Set the set for exploring
    explored = set()
    # Get all possible (hopefully) ways to add up to the goal weight
    ways = get_all_ways(weights, k, explored)
    # Discard the loads that are not balanced on the other side
    balanced_loads = [x for x in ways if sum(x[1]) == k * 2]
    # Assume through black magic that we have a working solution
    low_product = None
    for l in balanced_loads:
        x = 1
        for z in l[0]:
            x *= z
        if low_product is None or x < low_product:
            low_product = x
    return f"Part 1 answer = {low_product}"


def part2(weights, sum_weights, num_splits):
    k = sum_weights / num_splits
    explored = set()
    ways = get_all_ways(weights, k, explored)
    balanced_loads = [x for x in ways if sum(x[1]) == k * 3]
    low_product = None
    for l in balanced_loads:
        x = 1
        for z in l[0]:
            x *= z
        if low_product is None or x < low_product:
            low_product = x
    return f"Part 1 answer = {low_product}"


def main():
    # Get input
    weights = [int(x) for x in get_input('line')]
    # reverse to hopefully speed up searching
    weights.reverse()
    sum_weights = sum(weights)
    print(part1(weights, sum_weights, 3))
    print(part2(weights, sum_weights, 4))


main()

from Grids import DictGrid
from Pos import Pos


def get_input():
    coords = []
    folds = []
    with open("input.txt") as f:
        line = f.readline()
        while line != '\n':
            line = line.rstrip()
            x, y = [int(x) for x in line.split(',')]
            coords.append(Pos(x, y))
            line = f.readline()

        for line in f:
            line = line.rstrip()
            folds.append(line)

    return coords, folds

def is_this_pos_in_this_list(pos, pos_list):
    for p in pos_list:
        if pos.x == p.x and pos.y == p.y:
            return True
    return False



def prune_duplicates(coords):
    ans = []

    for c in coords:
        if not is_this_pos_in_this_list(c, ans):
            ans.append(c)

    return ans


def fold_paper(fold, coords):
    # x=5 is a vertical fold to the left
    # y=5 is a horizontal fold up
    fold = fold.replace('fold along ', '')
    axis, n = fold.split('=')
    n = int(n)



    if axis == 'y':
        # Horizontal up
        for i, coord in enumerate(coords):
            # Check if y coord is greater than n
            if coord.y > n:
                # Find the distance
                dist = coord.y - n
                new_coord = Pos(coord.x, coord.y - dist * 2)
                coords[i] = new_coord

    elif axis == 'x':
        # Vertical left
        for i, coord in enumerate(coords):
            # Check if x coord is greater than n
            if coord.x > n:
                # Find distance
                dist = coord.x - n
                new_coord = Pos(coord.x - dist * 2, coord.y)
                coords[i] = new_coord

    else:
        raise EnvironmentError('Axis label not x or y')


    return prune_duplicates(coords)


def main():
    # X increased right  Y increasing down
    coords, folds = get_input()
    for fold in folds:
        coords = fold_paper(fold, coords)

    grid = DictGrid(str)
    for co in coords:
        grid.add_data_to_grid_at_pos('#', co)

    grid.display_grid_ascii()


main()

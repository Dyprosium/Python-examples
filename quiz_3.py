# Randomly generates a grid with 0s and 1s, whose dimension is controlled by user input,
# as well as the density of 1s in the grid, and finds out, for given step_number >= 1
# and step_size >= 2, the number of stairs of step_number many steps,
# with all steps of size step_size.
#
# A stair of 1 step of size 2 is of the form
# 1 1
#   1 1
#
# A stair of 2 steps of size 2 is of the form
# 1 1
#   1 1
#     1 1
#
# A stair of 1 step of size 3 is of the form
# 1 1 1
#     1
#     1 1 1
#
# A stair of 2 steps of size 3 is of the form
# 1 1 1
#     1
#     1 1 1
#         1
#         1 1 1
#
# The output lists the number of stairs from smallest step sizes to largest step sizes,
# and for a given step size, from stairs with the smallest number of steps to stairs
# with the largest number of stairs.
#
# Written by Daniel Yang and Eric Martin for COMP9021


from random import seed, randint
import sys
from collections import defaultdict
from copy import deepcopy


def display_grid():
    for i in range(len(grid)):
        print('   ', ' '.join(str(int(grid[i][j] != 0)) for j in range(len(grid))))

def stairs_in_grid():
    d = {}
    for size in range(2,(dim+1)//2 + 1):
        array = deepcopy(grid)
        steps_and_stairs = defaultdict(int)
        for i in range(dim - size + 1):
            for j in range(dim - 2*size + 2):
                if array[i][j] > 0 and 0 not in array[i][j:j+size]:
                    x = i
                    y = j + size - 1
                    stepCounter = 0
                    while x + size - 1 < dim and y + size - 1 < dim:
                        if 0 not in [array[e][y] for e in range(x,x+size)]:
                            x += size - 1
                            array[x][y] = -1
                            if 0 not in array[x][y:y+size]:
                                y += size - 1
                                stepCounter += 1
                            else:
                                break
                        else: 
                            break
                    if stepCounter:
                        steps_and_stairs[stepCounter] += 1
        if steps_and_stairs:
            d[size] = sorted([(x, steps_and_stairs[x]) for x in steps_and_stairs])
    return d

try:
    arg_for_seed, density, dim = input('Enter three nonnegative integers: ').split()
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    arg_for_seed, density, dim = int(arg_for_seed), int(density), int(dim)
    if arg_for_seed < 0 or density < 0 or dim < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(arg_for_seed)
grid = [[randint(0, density) for _ in range(dim)] for _ in range(dim)]
print('Here is the grid that has been generated:')
display_grid()
# A dictionary whose keys are step sizes, and whose values are pairs of the form
# (number_of_steps, number_of_stairs_with_that_number_of_steps_of_that_step_size),
# ordered from smallest to largest number_of_steps.
stairs = stairs_in_grid()
for step_size in sorted(stairs):
    print(f'\nFor steps of size {step_size}, we have:')
    for nb_of_steps, nb_of_stairs in stairs[step_size]:
        stair_or_stairs = 'stair' if nb_of_stairs == 1 else 'stairs'
        step_or_steps = 'step' if nb_of_steps == 1 else 'steps'
        print(f'     {nb_of_stairs} {stair_or_stairs} with {nb_of_steps} {step_or_steps}')

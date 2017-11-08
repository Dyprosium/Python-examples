# Randomly fills a grid of size 10 x 10 with digits between 0
# and bound - 1, with bound provided by the user.
# Given a point P of coordinates (x, y) and an integer "target"
# also all provided by the user, finds a path starting from P,
# moving either horizontally or vertically, in either direction,
# so that the numbers in the visited cells add up to "target".
# The grid is explored in a depth-first manner, first trying to move north,
# always trying to keep the current direction,
# and if that does not work turning in a clockwise manner.
#
# Written by Daniel Yang and Eric Martin for COMP9021

import sys
from random import seed, randrange

from stack_adt import *

def display_grid():
    for i in range(len(grid)):
        print('   ', ' '.join(str(grid[i][j]) for j in range(len(grid[0]))))

def explore_depth_first(x, y, target):
    nextDirs = {"N":["W", "S", "E", "N"], "E":["N", "W", "S", "E"], "S":["E", "N", "W", "S"], "W":["S", "E", "N", "W"]}
    delta_i_j = {"N": (-1, 0), "S":(1, 0), "W":(0, -1), "E":(0, 1)}
    stack = Stack()
    stack.push([(x,y), "N", grid[x][y]])
    
    while not stack.is_empty():
        path = stack.pop()
        sum = path.pop()    
        direction = path.pop()
        (i, j) = path[-1]
        if sum == target:
            return path
        for nextDir in nextDirs[direction]:
            next_i, next_j = i + delta_i_j[nextDir][0], j + delta_i_j[nextDir][1]
            if (next_i, next_j) not in path and 0 <= next_i <= 9 and 0 <= next_j <= 9 and sum + grid[next_i][next_j] <= target:
                stack.push(path + [(next_i, next_j)] + [nextDir] + [sum + grid[next_i][next_j]])

try:
    for_seed, bound, x, y, target = [int(x) for x in input('Enter five integers: ').split()]
    if bound < 1 or x not in range(10) or y not in range(10) or target < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(for_seed)
grid = [[randrange(bound) for _ in range(10)] for _ in range(10)]
print('Here is the grid that has been generated:')
display_grid()
path = explore_depth_first(x, y, target)
if not path:
    print(f'There is no way to get a sum of {target} starting from ({x}, {y})')
else:
    print('With North as initial direction, and exploring the space clockwise,')
    print(f'the path yielding a sum of {target} starting from ({x}, {y}) is:')
    print(path)
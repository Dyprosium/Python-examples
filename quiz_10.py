# Randomly generates N distinct integers with N provided by the user,
# inserts all these elements into a priority queue, and outputs a list
# L consisting of all those N integers, determined in such a way that:
# - inserting the members of L from those of smallest index of those of
#   largest index results in the same priority queue;
# - L is preferred in the sense that the last element inserted is as large as
#   possible, and then the penultimate element inserted is as large as possible, etc.
#
# Written by Daniel Yang and Eric Martin for COMP9021


import sys
from random import seed, sample

from priority_queue_adt import *
    
def preferred_sequence():
    L = pq._data[ :len(pq)+1]
    nums_left = sorted(L[1: ], reverse = True)
    output = []  
    while nums_left:
        path = []
        i = len(L) - 1
        while i:
            path.insert(0, i)
            i //= 2
        for num in nums_left:
            pos_in_queue = L.index(num)
            try:
                valid = True
                for ind in path[path.index(pos_in_queue) + 1: ]:
                    if (ind % 2 and L[ind] < L[ind - 1]) or (not ind % 2 and ind + 1 < len(L) and L[ind] < L[ind + 1]):
                        valid = False
                        break
                if valid:
                    for i in range(path.index(pos_in_queue), len(path) - 1):
                        L[path[i]] = L[path[i+1]]
                    L = L[:-1]
                    output.insert(0, num)
                    nums_left.remove(num)
                    break
            except ValueError:
                continue
    return output        

try:
    for_seed, length = [int(x) for x in input('Enter 2 nonnegative integers, the second one no greater than 100: ').split()]
    if for_seed < 0 or length > 100:
        raise ValueError
except ValueError:
    print('Incorrect input (not all integers), giving up.')
    sys.exit()    
seed(for_seed)
L = sample(list(range(length * 10)), length)
pq = PriorityQueue()
for e in L:
    pq.insert(e)
print('The heap that has been generated is: ')
print(pq._data[ : len(pq) + 1])
print('The preferred ordering of data to generate this heap by successsive insertion is:')
print(preferred_sequence())
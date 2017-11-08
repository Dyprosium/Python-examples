# Written by Daniel Yang and Eric Martin for COMP9021


'''
Generates a list L of random nonnegative integers smaller than the length of L,
whose value is input by the user, and outputs two lists:
- a list M consisting of L's middle element, followed by L's first element,
  followed by L's last element, followed by L's second element, followed by
  L's penultimate element...;
- a list N consisting of L[0], possibly followed by L[L[0]], possibly followed by
  L[L[L[0]]]..., for as long as L[L[0]], L[L[L[0]]]... are unused, and then,
  for the least i such that L[i] is unused, followed by L[i], possibly followed by
  L[L[i]], possibly followed by L[L[L[i]]]..., for as long as L[L[i]], L[L[L[i]]]...
  are unused, and then, for the least j such that L[j] is unused, followed by L[j],
  possibly followed by L[L[j]], possibly followed by L[L[L[j]]]..., for as long as
  L[L[j]], L[L[L[j]]]... are unused... until all members of L have been used up.
'''
import sys
from random import seed, randrange

def posindex(lst):
    return [i for i in range(len(lst)) if lst[i]>=0]

try:
    arg_for_seed, length = input('Enter two nonnegative integers: ').split()
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    arg_for_seed, length = int(arg_for_seed), int(length)
    if arg_for_seed < 0 or length < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(arg_for_seed)
L = [randrange(length) for _ in range(length)]
K = L.copy()
J = L.copy()
print('\nThe generated list L is:')
print('  ', L)
M = []
N = []

i = 0
while K != [-1] * len(K):
    if K[i] != -1:
        N.append(K[i])
        K[i] = -1
        i = N[-1]
    else:
        i = posindex(K)[0]

try:
    M.append(J.pop(len(J)//2))
    while J != []:
        M.append(J.pop(0))
        if J != []:
            M.append(J.pop(-1))
except IndexError:
    pass

print('\nHere is M:')
print('  ', M)
print('\nHere is N:')
print('  ', N)
print('\nHere is L again:')
print('  ', L)
from collections import deque
from sys import exit
   
def row_exchange(L):
    return tuple(reversed(L))

def right_circular_shift(L):
    return tuple(L[e] for e in [3, 0, 1, 2, 5, 6, 7, 4])

def middle_clockwise_rotation(L):
    return tuple(L[e] for e in [0, 6, 1, 3, 4, 2, 5, 7])

try:
    goal = input("Input final configuration: ").replace(" ","")
    goal = tuple(int(x) for x in goal)
    if len(goal) != 8 or set(goal) != set(range(1,9)):
        raise ValueError
except ValueError:
    print("Incorrect configuration, giving up...")
    exit()

checkCases = deque()
checkCases.append((tuple(range(1,9)), 0))
seen = set()   

while (len(checkCases)):
    state, numTrans = checkCases[0]
    if state == goal:
        break;
    if state not in seen:
        if row_exchange(state) not in seen:
            checkCases.append((row_exchange(state), numTrans + 1))
        if right_circular_shift(state) not in seen:
            checkCases.append((right_circular_shift(state), numTrans + 1))
        if middle_clockwise_rotation(state) not in seen:
            checkCases.append((middle_clockwise_rotation(state), numTrans + 1))
        seen.add(state)
    checkCases.popleft()
        
step_or_steps = "step" if numTrans in {0,1} else "steps" 
is_or_are = "is" if numTrans in {0,1} else "are"   
print(f"{numTrans} {step_or_steps} {is_or_are} needed to reach the final configuration.")
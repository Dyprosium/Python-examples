#Returns position of next corner cell
def getNextCorner(num):
    i, j = 1, 1
    
    while j <= num:
        j += i
        if j > num:
            break
        j += i
        i += 1
    return j

#Returns the state of the die after a given number of steps in the given direction
def move(faces, direction, steps):
    steps = steps%4
    facesToChange = {"up":[0,1], "down":[1,0], "left":[0,2], "right":[2,0]}
    
    for _ in range(steps):
        temp = faces[facesToChange[direction][0]]
        faces[facesToChange[direction][0]] = faces[facesToChange[direction][1]]
        faces[facesToChange[direction][1]] = 7-temp
    return faces
        
while True:
    try:
        goal = int(input("Enter the desired goal cell number: "))
        if goal <= 0:
            raise ValueError
        else:
            break
    except ValueError:
        print("Incorrect value, try again")

#Die state saved as [U, F, R]
die = [3, 2, 1]
cell = 1
direction = "right"

changeDirection = {"right":"down", "down":"left", "left":"up", "up":"right"}

while cell < goal:
    if getNextCorner(cell) <= goal:
        die = move(die, direction, getNextCorner(cell)-cell)
        cell = getNextCorner(cell)
        direction = changeDirection[direction]
    else:
        die = move(die, direction, goal-cell)
        cell = goal

print(f"On cell {goal}, {die[0]} is at the top, {die[1]} at the front, and {die[2]} on the right.")
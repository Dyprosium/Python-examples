from random import randint
from collections import Counter

def pokerHand(hand):
    numUniques = len(set(hand))
    highestNo = Counter(hand).most_common(1)[0][1]
    d = {(1,5):"Five of a kind", (2,4):"Four of a kind", (2,3):"Full house", (3,3):"Three of a kind", (3,2): "Two pair", (4,2): "One pair"}
    
    if numUniques == 5:
        if  not (0 in hand and 5 in hand):
            return "Straight"
        else:
            return "Bust"
    else:
        return d[(numUniques,highestNo)]
        
def subMultiSet(L, M):
    sub = Counter(L)
    superMultiSet = Counter(M)
    for item, count in sub.items():
        if count > superMultiSet[item] or item not in superMultiSet:
            return False
    return True

def play():
    keptDice = []
    faces = {0:"Ace", 1:"King", 2:"Queen", 3:"Jack", 4:"10", 5:"9"}
    facesRev = {"Ace":0, "King":1, "Queen":2, "Jack":3, "10":4, "9":5}
    
    for i in range(3):
        roll = sorted([randint(0,5) for _ in range(5-len(keptDice))] + keptDice)
        print("The roll is: " + " ".join([faces[e] for e in roll]))
        print(f"It is a {pokerHand(roll)}")
        if i != 2:
            second_or_third = "second" if i == 0 else "third"
            while True:
                try:
                    keep = input(f"Which dice do you want to keep for the {second_or_third} roll? ")
                    keptDice = [facesRev[e] for e in keep.split() if keep not in {"all","All"}]
                    if keep in {"all", "All"} or sorted(keptDice) == roll:
                        print("Ok, done.")
                        return
                    elif not subMultiSet(keptDice,roll):
                        raise KeyError
                    break
                except KeyError:
                    print("That is not possible, try again!")

def simulate(n):
    count = {"Five of a kind":0, "Four of a kind":0, "Full house":0, "Straight":0, "Three of a kind":0, "Two pair":0, "One pair":0}
    for _ in range(n):
        outcome = pokerHand([randint(0,5) for _ in range(5)])
        if outcome in count:
            count[outcome] += 1
    for hand in count:
        print(f"{hand:<15}: {count[hand]/n:.2%}")
from sys import exit
from itertools import permutations

def wordScore(word):
    letterValue = {"a":2, "b":5, "c":4, "d":4, "e":1, "f":6, "g":5, "h":5, "i":1, "j":7, "k":6, "l":3, "m":5, "n":2, "o":3, "p":5, "q":7, "r":2, "s":1, "t":2, "u":4, "v":6, "w":6, "x":7, "y":5, "z":7}
    return sum(letterValue[letter] for letter in word)

letters = [x for x in input("Enter between 3 and 10 lowercase letters: ").replace(" ","")]
if not all(e.islower() for e in letters) or len(letters) not in range(3,11):
    print("Incorrect input, giving up...")
    exit()

letterPerms = {"".join(e) for n in range(len(letters)) for e in permutations(letters,n+1)}
words = []
with open("wordsEn.txt") as dictionary:
    for word in dictionary: 
        if word.rstrip("\n") in letterPerms:
            words.append(word.rstrip("\n"))

words = [word for word in words if wordScore(word) == wordScore(max(words, key = wordScore))]
if not words:
    print("No word is built from some of those letters.")
else:
    print(f"The highest score is {wordScore(words[0])}.")
    if len(words) == 1:
        print(f"The highest scoring word is {words[0]}")
    else:
        print("The highest scoring words are, in alphabetical order:\n   ", "\n    ".join(words)) 
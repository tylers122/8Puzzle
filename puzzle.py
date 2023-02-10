import time
from queue import PriorityQueue

#a tuple of tuples, since tuples are unchangeable
#0 represents empty tile
goalState = ((1, 2 ,3), (4, 5, 6), (7, 8, 0))

#each node will be a puzzle state
class Node:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.heuristic = 0      #h(n)
        self.depth = 0          #g(n)
        self.emptyX = 0         #blank space's x/column value (0-2)
        self.emptyY = 0         #blank space's y/row value (0-2)

#cleaned up main function/put everything together
def main():
    print("Welcome to the 8 Puzzle solver!\n")

    puzzle = getPuzzle()
    while True:
        print("Choose an algorithm (1, 2, 3):")
        print("1. Uniform Cost Search")
        print("2. A* with Misplaced Tile Heuristic")
        print("3. A* with Euclidean Distance Heuristic")
        alg = int(input())

        if alg == 1 or alg == 2 or alg == 3:
            break

    search(puzzle, alg)

    


def search(puzzle, alg):
    #use priority queue for frontier
    currPuzzle = Node(puzzle)                       #initial state
    currPuzzle.heuristic = getAlgo(puzzle, alg)     #gets algorithm heuristic from user

#gets a default puzzle or lets user create custom puzzle
def getPuzzle():
    while True:
        print("Select a puzzle:")
        print("1 - Premade Puzzle")
        print("2 - Custom Puzzle")
        choice = int(input())

        if choice == 1:
            return preMadePuzzles()
        elif choice == 2:
            return createPuzzle()

#determines which algorithm to used based on user input
def getAlgo(puzzle, alg):
    while True:
        if alg == 1:
            return uniformCost()
        elif alg == 2:
            return misplacedTile(puzzle)
        elif alg == 3:
            return euclidian(puzzle)


#premade puzzles based on user input difficulty
def preMadePuzzles():
    puzzles = (((1, 2, 3), (4, 5, 6), (7, 8, 0)),   #trivial
               ((1, 2, 3), (4, 5, 6), (7, 0, 8)),   #very easy
               (())) #add more later
    
    while True:
        level = int(input("Enter a difficulty level from 1 - 9 (easy - hard): "))
        if level >= 1 and level <= 9:
            printPuzzle(puzzles[level - 1])
            return puzzles[level - 1]
            

def createPuzzle():
    print("Enter a puzzle! Use 0 for a blank space.")
    userPuzzle = []     #use list since tuples are unchangeable
    
    #input custom puzzle
    for i in range(3):
        print("Enter in row #" + str(i + 1) + ". Use a space between each number.")
        row = input()
        userPuzzle.append(row.split(" "))   #appends input separated by space

    for i in range(len(userPuzzle)):
        for j in range(len(userPuzzle)):
            userPuzzle[i][j] = int(userPuzzle[i][j])    #convert every number to int from str

    userPuzzle = tuple(userPuzzle)  #convert list to tuple, now unchangeable
    printPuzzle(userPuzzle)
    return userPuzzle

#prints puzzle
def printPuzzle(puzzle):
    result = ""
    for i in range(len(puzzle)):
        result += str(puzzle[i]) + "\n"
    
    print(result)
        


#heuristic functions
def uniformCost():
    #no heuristic, return 0
    return 0

def misplacedTile(puzzle):
    pass
    
def euclidian(puzzle):
    pass


main()

import time

#a tuple of tuples, since tuples are unchangeable
#0 represents empty tile
goalState = ((1, 2 ,3), (4, 5, 6), (7, 8, 0))

def main():
    print("Welcome to the 8 Puzzle solver!")
    print("Choose an algorithm (1, 2, 3):")
    print("1. Uniform Cost Search")
    print("2. A* with Misplaced Tile Heuristic")
    print("3. A* with Euclidean Distance Heuristic")
    alg = input()

#default puzzles based on user input difficulty
def defaultPuzzles():
    puzzles = (((1, 2, 3), (4, 5, 6), (7, 8, 0)),   #trivial
               ((1, 2, 3), (4, 5, 6), (7, 0, 8)),   #very easy
               (())) #add more later
    
    level = int(input("Enter a difficulty level from 1 - 9 (easy - hard): "))
    finish = False
    while not finish:
        if level >= 1 and level <= 9:
            printPuzzle(puzzles[level - 1])
            return puzzles[level - 1]
        level = int(input("Enter a difficulty level from 1 - 9 (easy - hard): "))

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

def misplacedTile():
    pass

def euclidian():
    pass


# main()
createPuzzle()

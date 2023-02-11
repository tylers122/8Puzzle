import time
import copy
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
        self.blankRow = 0       #blank space's row value(0-2)
        self.blankCol = 0       #blank space's column value (0-2)

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

    

#follows pseudocode given from project description doc https://docs.google.com/document/d/1dvHD8SyuXkMND-GpRxB21DEzvkfBVL5t/edit
def search(puzzle, alg):
    #use priority queue for frontier
    currPuzzle = Node(puzzle)                       #initial state of frontier
    currPuzzle.heuristic = getAlgo(puzzle, alg)     #gets algorithm heuristic from user
    explored = set()                                #initialize explored set    https://www.w3schools.com/python/python_sets.asp
    expanded = 0                                    #expanded nodes count
    max = 0                                         #max queue size
    queue = PriorityQueue()

    queue.put(currPuzzle)
    explored.add(currPuzzle.puzzle)                 
    max += 1

    while queue.qsize() != 0:                       #if the frontier is empty then return failure
        currPuzzle = queue.get()                    #choose a leaf node and remove it from the frontier
        if currPuzzle.puzzle == goalState:          #if the node contains a goal state then return the corresponding solution
            return currPuzzle
        expanded += 1
        
        expandNode(currPuzzle, queue, explored, alg)#expand the chosen node, adding the resulting nodes to the frontier

    print("Impossible puzzle. No solution found.")  
    exit(0)


    #psuedocode taken from project doc:
    # loop do
    #     if the frontier is empty then return failure
    #     choose a leaf node and remove it from the frontier
    #     if the node contains a goal state then return the corresponding solution
    #     add the node to the explored set
    #     expand the chosen node, adding the resulting nodes to the frontier
    #         only if not in the frontier or explored set

def expandNode(puzzle, queue, explored, alg):
    #find row and column of blank space (0)
    for i in range(len(puzzle.puzzle)):
        for j in range(len(puzzle.puzzle)):
            if puzzle.puzzle[i][j] == 0:
                puzzle.blankRow = i
                puzzle.blankCol = j

    if puzzle.blankRow != 0:
        #move blank tile up
        move(puzzle, queue, explored, puzzle.blankRow - 1, puzzle.blankCol, alg)
        return
    elif puzzle.blankRow < len(puzzle.puzzle) - 10:
        #move blank tile down
        move(puzzle, queue, explored, puzzle.blankRow + 1, puzzle.blankCol, alg)
        return
    elif puzzle.blankCol != 0:
        #move blank tile left
        move(puzzle, queue, explored, puzzle.blankRow, puzzle.blankCol - 1, alg)
        return
    elif puzzle.blankCol < len(puzzle.puzzle) - 1:
        #move blank tile right
        move(puzzle, queue, explored, puzzle.blankRow, puzzle.blankCol + 1, alg)
        return

def move(puzzle, queue, explored, row, col, alg):
    child = copy.copy(puzzle.puzzle)            #copy tuple of tuples
    
    #move blank tile accordingly
    child = makeList(child)
    child[puzzle.blankRow][puzzle.blankCol] = child[row][col]
    child[row][col] = 0
    child = makeTuple(child)

    #new puzzle
    if child not in explored:
        explored.add(child)
        childNode = Node(child)
        childNode.heuristic = getAlgo(childNode.puzzle, alg)
        childNode.depth = puzzle.depth + 1
        queue.put(childNode)

    

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

    #convert every number to int from str
    for i in range(len(userPuzzle)):
        for j in range(len(userPuzzle)):
            userPuzzle[i][j] = int(userPuzzle[i][j])    

    userPuzzle = makeTuple(userPuzzle)  #convert list to tuple, now unchangeable
    printPuzzle(userPuzzle)
    return userPuzzle

#convert puzzle from list to tuple
def makeTuple(puzzle):
    temp = ()
    list = []

    #convert each row to tuple
    for i in range(len(puzzle)):
        temp = tuple(puzzle[i])
        list.append(temp)
    list = tuple(list)
    return list

#convert puzzle from tuple to list
def makeList(puzzle):
    temp = []

    #convert each row to list
    for i in range(len(puzzle)):
        temp.append(list(puzzle[i]))
    temp = tuple(temp)
    return temp

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
    misplaced = 0
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if puzzle[i][j] != goalState[i][j]:
                if puzzle[i][j] != 0:
                    misplaced += 1
    return misplaced

def euclidian(puzzle):
    euclidian = 0
    goal = 0
    misplaced = 0

    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if puzzle[i][j] != goalState[i][j]:
                if puzzle[i][j] != 0:
                    misplaced = puzzle[i][j]
                    #FINISH LATER
                     #FINISH LATER
                      #FINISH LATER
    return


main()

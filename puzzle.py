#Works Cited:
#https://stackoverflow.com/questions/68630/are-tuples-more-efficient-than-lists-in-python
#https://www.geeksforgeeks.org/python-__lt__-magic-method/
#https://www.w3schools.com/python/python_sets.asp
#https://docs.python.org/3/library/queue.html
#https://stackoverflow.com/questions/15214404/how-can-i-copy-an-immutable-object-like-tuple-in-python
#https://machinelearningmastery.com/distance-measures-for-machine-learning/#:~:text=Euclidean%20distance%20calculates%20the%20distance,floating%20point%20or%20integer%20values.

import time
import copy
import math
from queue import PriorityQueue

#a tuple of tuples, since tuples are unchangeable
#tuples also faster than list of lists
#https://stackoverflow.com/questions/68630/are-tuples-more-efficient-than-lists-in-python
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

    #magic method allows comparison between two objects
    #lets priority queue work for objects
    #https://www.geeksforgeeks.org/python-__lt__-magic-method/
    def __lt__(self, node2):
        self.distance = self.heuristic + self.depth
        node2.distance = node2.heuristic + node2.depth

        #force search to choose smaller depth, or else infinite loop occurs
        if self.distance == node2.distance:
            return node2.depth > self.depth
        return node2.distance > self.distance

#cleaned up main function/put everything together
def main():
    print("Welcome to the 8 Puzzle solver!\n")

    puzzle = getPuzzle()                                    #use premade puzzle or have user create custom puzzle
    while True:                                             #ask user to choose algorithm
        print("Choose an algorithm (1, 2, 3):")
        print("1. Uniform Cost Search")
        print("2. A* with Misplaced Tile Heuristic")
        print("3. A* with Euclidean Distance Heuristic")
        alg = int(input())

        if alg == 1 or alg == 2 or alg == 3:
            break


    startTime = time.time()                                 #start time of search
    goalState, expanded, maxNum = search(puzzle, alg)
    endTime = time.time()                                   #end time of search
    searchTime = endTime - startTime                        #total search time

    printPuzzle(goalState.puzzle)                           #print goal state
    print("Goal!")
    print("Solution depth:", str(goalState.depth))          #print solution depth
    print("Expanded nodes:", str(expanded))                 #print nodes expanded
    print("Max nodes in queue:", str(maxNum))               #print max nodes in queue
    print("Search time:", str(round(searchTime, 4)) + "s")  #print search time




    

#follows pseudocode given from project description doc https://docs.google.com/document/d/1dvHD8SyuXkMND-GpRxB21DEzvkfBVL5t/edit
def search(puzzle, alg):
    #use priority queue for frontier
    currPuzzle = Node(puzzle)                           #initial state of frontier
    currPuzzle.heuristic = getAlgo(puzzle, alg)         #gets algorithm heuristic from user
    explored = set()                                    #initialize explored set    https://www.w3schools.com/python/python_sets.asp
    expanded = 0                                        #expanded nodes count
    maxNum = 0                                          #max queue size
    queue = PriorityQueue()                             #use Python Priority Queue  https://docs.python.org/3/library/queue.html

    queue.put(currPuzzle)                               #add initial state to priority queue
    explored.add(currPuzzle.puzzle)                     #explored initial state
    maxNum += 1                                         #initial state in queue

    while queue.qsize() != 0:                           #if the frontier is empty then return failure
        maxNum = max(queue.qsize(), maxNum)             #find max queue size between priority queue and current max
        currPuzzle = queue.get()                        #choose a leaf node and remove it from the frontier
        if currPuzzle.puzzle == goalState:              #if the node contains a goal state then return the corresponding solution
            return currPuzzle, expanded, maxNum
        expanded += 1
        
        printPuzzle(currPuzzle.puzzle)
        expandNode(currPuzzle, queue, explored, alg)    #expand the chosen node, adding the resulting nodes to the frontier

    print("Impossible puzzle. No solution found.")      #if the frontier is empty then return failure
    exit(0)


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
    if puzzle.blankRow < len(puzzle.puzzle) - 1:
        #move blank tile down
        move(puzzle, queue, explored, puzzle.blankRow + 1, puzzle.blankCol, alg)
    if puzzle.blankCol != 0:
        #move blank tile left
        move(puzzle, queue, explored, puzzle.blankRow, puzzle.blankCol - 1, alg)
    if puzzle.blankCol < len(puzzle.puzzle) - 1:
        #move blank tile right
        move(puzzle, queue, explored, puzzle.blankRow, puzzle.blankCol + 1, alg)

def move(puzzle, queue, explored, row, col, alg):
    #deepcopy to create own instance of tuples within tuples 
    #https://stackoverflow.com/questions/15214404/how-can-i-copy-an-immutable-object-like-tuple-in-python
    child = copy.deepcopy(puzzle.puzzle)            

    #move blank tile accordingly
    child = makeList(child)
    child[puzzle.blankRow][puzzle.blankCol] = child[row][col]
    child[row][col] = 0
    child = makeTuple(child)

    #unexplored puzzle
    if child not in explored:
        explored.add(child)                                     #add to explored set
        childNode = Node(child)                                 #create new node with new puzzle state
        childNode.heuristic = getAlgo(childNode.puzzle, alg)    #calculate new heuristic for new puzzle state
        childNode.depth = puzzle.depth + 1                      #increase depth by 1
        queue.put(childNode)                                    #add new puzzle to priority queue

    

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

#determines which algorithm to use based on user input
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
    puzzles = (((1, 2, 3), (4, 5, 6), (7, 8, 0)),   #trivial    1
               ((1, 2, 3), (4, 5, 6), (7, 0, 8)),   #very easy  2
               ((1, 2, 3), (4, 5, 6), (0, 7, 8)),
               ((1, 2, 0), (4, 5, 3), (7, 8, 6)),   #easy       4
               ((1, 5, 2), (4, 0, 3), (7, 8, 6)),
               ((0, 1, 2), (4, 5, 3), (7, 8, 6)),   #doable     6
               ((4, 1, 2), (7, 5, 3), (8, 6, 0)),
               ((8, 7, 1), (6, 0, 2), (5, 4, 3)),   #oh boy     8
               ((8, 7, 1), (6, 4, 2), (0, 5, 3)))
    
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

#gets goal position for euclidian distance
def getGoal(goal, misplaced):
    for i in range(len(goal)):
        for j in range(len(goal)):
            if (goal[i][j] == misplaced):
                return i, j

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
    #use distance formula between position of current node and goal position:
    #sqrt(|x2 - x1| + |y2 - y1|)
    #sqrt(|goalX - misplacedX| + |goalY - misplacedY|)
    #https://machinelearningmastery.com/distance-measures-for-machine-learning/#:~:text=Euclidean%20distance%20calculates%20the%20distance,floating%20point%20or%20integer%20values.

    euclidian = 0
    goalRow = 0
    goalCol = 0
    misplaced = 0
    misRow = 0
    misCol = 0

    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if puzzle[i][j] != goalState[i][j]:
                if puzzle[i][j] != 0:
                    misplaced = puzzle[i][j]
                    misRow = i
                    misCol = j
                    goalRow, goalCol = getGoal(goalState, misplaced)
                    euclidian += math.sqrt(abs(goalRow - misRow) + abs(goalCol - misCol))
    return euclidian


main()

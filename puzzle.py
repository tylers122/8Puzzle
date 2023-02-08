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


#heuristic functions
def uniformCost():
    #no heuristic, return 0
    return 0

def misplacedTile():
    pass

def euclidian():
    pass


main()

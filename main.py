import random
import os
import sys
from time import perf_counter

# Priority queue
class PriorityQueue(object):
    def __init__(self):
        self.__elements = [None, None]
        self.__length = 0

    def enqueue(self, x):
        if self.__length == 0:
            self.__elements[1] = x
            self.__length += 1
        else:
            self.__elements.append(x)
            self.__length += 1
            self.move_up()

    def dequeue(self):
        if self.__length == 0:
            return None
        elif self.__length == 1:
            element = self.__elements.pop(1)
        else:
            element = self.__elements[1]
            self.__elements[1] = self.__elements.pop(self.__length)
            self.__length -= 1
            self.move_down()
        return element

    def move_down(self):
        n = 1
        while n != self.__length:
            child = n * 2
            if child > self.__length:
                break
            if child + 1 <= self.__length and self.__elements[child + 1][1] < self.__elements[child][1]:
                child += 1
            if self.__elements[n][1] < self.__elements[child][1]:
                break
            else:
                self.__elements[n], self.__elements[child] = self.__elements[child], self.__elements[n]
                n = child

    def move_up(self):
        n = self.__length
        while n != 1:
            m = n // 2
            if self.__elements[n][1] < self.__elements[m][1]:
                self.__elements[n], self.__elements[m] = self.__elements[m], self.__elements[n]
            else:
                break
            n = m

# Node class representing the fifteen puzzle state
class Node:
    def __init__(self, table, parent, zeroPos, h, moves):
        self.table = table # - fifteen puzzle state
        self.parent = parent # - pointer to previous state
        self.zeroPos = zeroPos # - position of zero (blank tile)
        self.h = h # - heuristic value
        self.moves = moves # number of moves up to this state


# Count inversions: comparing elements 'a' and 'b' at indices 'i' and 'j' respectively; when a > b & i > j, it's called an inversion
def countInversions(table):
        counter = 0
        for k in range(15):
            t1 = table[k] 
            for i in range(k+1, 16):
                t2 = table[i]
                if t1 > t2 and t2 != 0 and t1 != 0:
                    counter += 1
        return counter

# Determine the row containing zero. Row indices here are 1..4 starting from the bottom row
def detectRank(table):
    pos = table.index(0)    
    emptyRank = 4 - pos//4
    return emptyRank

def isSolvable(table):
        rank = detectRank(table)
        if (countInversions(table) % 2) != (rank % 2):
            return True
        else:
            return False

# Randomly shuffle the table
def shuffle(table):
    random.shuffle(table)
    while not isSolvable(table):
        random.shuffle(table)
    return table

# Heuristic
def manhattan_LC(table):
        h = 0
        for i in range(16):
            tile = table[i]
            if tile == i + 1 or tile == 0:
                continue
            else:
                raw_target = (tile - 1) // 4
                column_target = (tile - 1) % 4
                raw = i // 4
                column = i % 4
                h += abs(raw - raw_target) + abs(column - column_target)
        
        # Linear Conflict
        for row in range(4):
            row_tiles = []
            for col in range(4):
                tile = table[row * 4 + col]
                if tile != 0 and (tile - 1) // 4 == row:
                    row_tiles.append(tile)
            
            for j in range(len(row_tiles)):
                for k in range(j + 1, len(row_tiles)):
                    if row_tiles[j] > row_tiles[k]:
                        h += 2

        for col in range(4):
            col_tiles = []
            for row in range(4):
                tile = table[row * 4 + col]
                if tile != 0 and (tile - 1) % 4 == col:
                    col_tiles.append(tile)
            
            for j in range(len(col_tiles)):
                for k in range(j + 1, len(col_tiles)):
                    if col_tiles[j] > col_tiles[k]:
                        h += 2

        return h

# Traverse node pointers and record the zero position for each state leading to the solution of the fifteen puzzle
def traceNodes(final_node):
    nodesZeroList = []
    nodesCounter = 0
    node = final_node
    while node:
        nodesZeroList.append(node.zeroPos)
        node = node.parent
        nodesCounter += 1
    return nodesZeroList, nodesCounter

# Main function to find a (near-optimal) solution
def Solve(table, w): # (table, weight)
    manhattanHeuristic = manhattan_LC(table)
    nodeQueue = PriorityQueue() 
    node = Node(table.copy(), None, table.index(0), manhattanHeuristic, 0)
    visited = set()
    visited.add(tuple(table))

    while node.h != 0:
        for dir in movesForZero[node.zeroPos]:
            prevZeroPos = node.zeroPos
            new_table = node.table.copy()
            
            new_table[dir], new_table[prevZeroPos] = new_table[prevZeroPos], new_table[dir]
            hashable_table = tuple(new_table)

            if hashable_table in visited:
                continue    

            new_limit = manhattan_LC(new_table)
            new_moves = node.moves + 1

            nodeQueue.enqueue((Node(new_table, node, dir, new_limit, new_moves), new_moves + w*new_limit))
            visited.add(hashable_table)
        node = nodeQueue.dequeue()[0]
    return node

# ======== GLOBALS ======== 
movesForZero = (
(1, 4),            
(0, 2, 5),         
(1, 3, 6),         
(2, 7),            

(0, 5, 8),         
(1, 4, 6, 9),      
(2, 5, 7, 10),     
(3, 6, 11),        

(4, 9, 12),        
(5, 8, 10, 13),    
(6, 9, 11, 14),    
(7, 10, 15),       

(8, 13),           
(9, 12, 14),       
(10, 13, 15),      
(11, 14)           
)

tablica = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
key_word = None
file_count = 0
projektDir = os.path.dirname(os.path.abspath(__file__))
folderInPath = os.path.join(projektDir, "In")
folderOutPath = os.path.join(projektDir, "Out")
n = int(sys.argv[1])
w = float(sys.argv[2])

# =========================

# Remove existing files from the 'In' and 'Out' directories
if n != 0:
    for filename in os.listdir(folderInPath):
        filePath = os.path.join(folderInPath, filename)
        
        if os.path.isfile(filePath):
            os.remove(filePath) 

    for filename in os.listdir(folderOutPath):
        filePath = os.path.join(folderOutPath, filename)
        
        if os.path.isfile(filePath):
            os.remove(filePath)

    # Generate boards and save them to the 'In' directory
    for i in range(n):
        t_random = shuffle(tablica)
        with open(f"{folderInPath}/table{i}.txt", "w") as f:
            t_random_list = [str(i) for i in t_random]
            f.write(", ".join(t_random_list))
    


# Solve boards from the 'In' directory and save the result to the 'Out' directory
with os.scandir(folderInPath) as entries:
    for entry in entries:
        if entry.is_file():
            with open(entry.path, 'r') as f:
                t = [int(i) for i in f.readline().split(', ')]
                if isSolvable(t):
                    start = perf_counter()
                    solution = Solve(t, w)
                    end = perf_counter()
                    nodesStats = traceNodes(solution)
                    nodesZeroList = nodesStats[0]
                    nodesCounter = nodesStats[1]
                    raw1 = f"Blank element moves: {'->'.join([str(i) for i in nodesZeroList[::-1]])}\n"
                    raw2 = f"Number of moves: {nodesCounter - 1}\n"
                    raw3 = f"Solution search time: {end-start:.5f}\n"
                    with open(f"{folderOutPath}/{entry.name[:-4]}_out.txt", "w", encoding="utf-8") as f:
                        f.writelines([raw1, raw2, raw3])
            
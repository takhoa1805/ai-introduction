# State: list of (n+1) elements. Where the empty space's value = 0
# - n+1: number of elements in the board
# - sqrt(n+1) * sqrt(n+1): the board's size
# Initial state: Randomly located n+1 elements in a 2D list
# Goal state: n+1 elements are sorted in ascending order
# Legal move: Swap the empty space with one of its neighbors
# - The empty space can move up, down, left, or right as long as it is not out of the board
# - Swap (A[i],A[j]) so that:
#     => A[i] == 0 
#     => j = i + 1 OR 
#        j = i - 1 OR 
#        j = i + sqrt(n+1) OR 
#        j = i - sqrt(n+1)
# Cost: 1 for each move

from copy import deepcopy
import math
import sys
from board_generator import generate_unique_random_numbers

# print(sys.getrecursionlimit())
sys.setrecursionlimit(10000000)


BOARD_SIZE = 16
# ADD MAXIMUM DEPTH TO REDUCE RECURSION DEPTH
MAX_DEPTH = 50


# GENERATE INITIAL STATES
init_state = generate_unique_random_numbers(BOARD_SIZE)

# GENERATE GOAL STATES
goal_state_1 = [0]
goal_state_2 = []

for i in range (1,BOARD_SIZE):
    goal_state_1.append(i)
    goal_state_2.append(i)

goal_state_2.append(0)



print ("Initial state:", init_state)
print ("Goal state 1:", goal_state_1)
print ("Goal state 2:", goal_state_2)


class State:

    # up,down,left,right = ['travelled','untravelled','unavailable']
    def __init__(self, board, up='untravelled', down='untravelled', left='untravelled', right='untravelled', parent=None, depth=0):
        self.board = board
        self.parent = parent
        self.depth = depth
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.empty = self.find_empty()
        self.is_goal = self.goal_check()


    def find_empty(self):
        # print("self.board",self.board)
        for i in range(len(self.board)):
            if self.board[i] == 0:
                # print("empty space:",i)
                return i


    def swap(self,board, x, y):
        new_state = board.copy()
        new_state[x], new_state[y] = new_state[y], new_state[x]

        return new_state

    def goal_check(self):
        return self.board == goal_state_1 or self.board == goal_state_2

    def move_up(self):
        move = self.empty - math.sqrt(len(self.board))
        move = int(move)
        if move in range(len(self.board)):
            new_board = self.swap(self.board, self.empty, move)
            return new_board
        else:
            self.up = 'unavailable'
            return 'unavailable'


    def move_down(self):
        move = self.empty + math.sqrt(len(self.board))
        move = int(move)


        if move in range(len(self.board)):
            new_board = self.swap(self.board, self.empty, move)
            return new_board

        else:
            self.down = 'unavailable'
            return 'unavailable'


    def move_left(self):
        move = self.empty - 1
        move = int(move)
        at_left_border = self.empty % (math.sqrt(len(self.board))) == 0

        if move in range(len(self.board)) and not at_left_border:
            new_board = self.swap(self.board, self.empty, move)
            return new_board

        else:
            self.left = 'unavailable'
            return 'unavailable'


    def move_right(self):
        move = self.empty + 1
        move = int(move)
        at_right_border = (self.empty) % (math.sqrt(len(self.board))) == (math.sqrt(len(self.board)) - 1)

        if move in range(len(self.board)) and not at_right_border:
            new_board = self.swap(self.board, self.empty, move)
            return new_board

        else:
            self.right = 'unavailable'
            return 'unavailable'


    def search(self,visited):
        self.print_state()
        if (self.is_goal):
            print ("GOAL STATE FOUND!")
            self.print_state()
            return True
        
        if (self.depth > MAX_DEPTH):
            return False

        visited.add(tuple(self.board))

        # Search up
        up_board = self.move_up()
        if (up_board != 'unavailable' and self.up == 'untravelled' and tuple(up_board) not in visited):
            print("moving up")
            up_state = State(up_board,parent=self,down="travelled",depth=self.depth+1)
            self.up = "travelled"
            if (up_state.search(visited) == True):
                return True
        
        # Search down
        down_board = self.move_down()
        if (down_board != 'unavailable' and self.down == 'untravelled' and tuple(down_board) not in visited):
            print("moving down")
            down_state = State(down_board,parent=self,up="travelled",depth=self.depth+1)
            self.down = "travelled"
            if (down_state.search(visited) == True):
                return True
            


        # Search left
        left_board = self.move_left()
        if (left_board != 'unavailable' and self.left == 'untravelled' and tuple(left_board) not in visited):
            print("moving left")
            left_state = State(left_board,parent=self,right="travelled",depth=self.depth+1)
            self.left = "travelled"
            if (left_state.search(visited) == True):
                return True
        
        # Search right
        right_board = self.move_right()
        if (right_board != 'unavailable' and self.right == 'untravelled' and tuple(right_board) not in visited):
            print("moving right")
            right_state = State(right_board,parent=self,left="travelled",depth=self.depth+1)
            self.right = "travelled"
            if (right_state.search(visited) == True):
                return True
        
        return False

    def print_state(self):
        print('Visit state status:')
        print('Depth:', self.depth)
        print('Up: ',self.up)
        print('Down: ',self.down)
        print('Left: ',self.left)
        print('Right: ',self.right)
        print('Empty space:',self.empty)
        print('Is goal:',self.is_goal)
        
        # Check if array length is a perfect square
        length = len(self.board)
        sqrt_length = int(math.sqrt(length))
        if sqrt_length * sqrt_length != length:
            print("Array length is not a perfect square.")
            return

        # Print the matrix in sqrt_length x sqrt_length format
        for i in range(sqrt_length):
            row = self.board[i * sqrt_length: (i + 1) * sqrt_length]
            print(" ".join(map(str, row)))
        print ('\n')
        

# Check if the initial state is solvable
def is_solvable(init_state):
    size = len(init_state)
    width = int(math.sqrt(size))

    inversions = 0
    for i in range(size):
        for j in range(i + 1, size):
            if init_state[i] != 0 and init_state[j] != 0 and init_state[i] > init_state[j]:
                inversions += 1

    empty_index = init_state.index(0)
    empty_row_from_bottom = width - (empty_index // width)

    if width % 2 == 1:
        return inversions % 2 == 0
    else:
        return (inversions % 2 == 0 and empty_row_from_bottom % 2 == 1) or \
               (inversions % 2 == 1 and empty_row_from_bottom % 2 == 0)


if (not is_solvable(init_state)):
    print("")
    print ("THE INITIAL STATE IS NOT SOLVABLE")
    print("")

    exit()
else:
    state = State(init_state)
    visited_states = set()
    state.search(visited_states)









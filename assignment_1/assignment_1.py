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


# Initial state of 8-Puzzle
init_state =[0,1,5,7,2,8,4,3,6]

# Goal state of 8-Puzzle
goal_state = [0,1,2,3,4,5,6,7,8]

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
        # new_state = deepcopy(board)
        # new_state[x], new_state[y] = new_state[y], new_state[x]


        # print("swapped from ",x,"to",y)
        # print("type of new_state",type(new_state))

        return new_state

    def goal_check(self):
        return self.board == goal_state

    def move_up(self):
        move = self.empty - math.sqrt(len(self.board))
        move = int(move)
        # print("move up in range",move in range(len(self.board)))
        if move in range(len(self.board)):
            self.up = 'travelled'
            new_board = self.swap(self.board, self.empty, move)
            # new_state = State(new_board, parent=self, depth=self.depth+1)
            return new_board
        else:
            self.up = 'unavailable'
            return 'unavailable'


    def move_down(self):
        move = self.empty + math.sqrt(len(self.board))
        move = int(move)

        # print("move down in range",move in range(len(self.board)))

        if move in range(len(self.board)):
            self.down = 'travelled'
            new_board = self.swap(self.board, self.empty, move)
            # new_state = State(new_board, parent=self, depth=self.depth+1)
            return new_board

        else:
            self.down = 'unavailable'
            return 'unavailable'


    def move_left(self):
        move = self.empty - 1
        move = int(move)

        # print("move left in range", move in range(len(self.board)))

        if move in range(len(self.board)):
            self.left = 'travelled'
            new_board = self.swap(self.board, self.empty, move)
            # new_state = State(new_board, parent=self, depth=self.depth+1)
            return new_board

        else:
            self.left = 'unavailable'
            return 'unavailable'


    def move_right(self):
        move = self.empty + 1
        move = int(move)

        # print("move right in range",move in range(len(self.board)))

        if move in range(len(self.board)):
            self.right = 'travelled'
            new_board = self.swap(self.board, self.empty, move)
            # new_state = State(new_board, parent=self, depth=self.depth+1)
            return new_board

        else:
            self.right = 'unavailable'
            return 'unavailable'


    def search(self):
        self.print_state()
        if (self.is_goal):
            print ("GOAL STATE FOUND!")
            self.print_state()
            return True
        
        # Search up
        up_board = self.move_up()
        # print("up_board",up_board)
        if (up_board != 'unavailable' and self.up == 'untravelled'):
            up_state = State(up_board,parent=self,down="travelled",depth=self.depth+1)
            if (up_state.search() == True):
                return True
        
        # Search down
        down_board = self.move_down()
        # print("down_board",down_board)
        if (down_board != 'unavailable' and self.down == 'untravelled'):
            down_state = State(down_board,parent=self,up="travelled",depth=self.depth+1)

            if (down_state.search() == True):
                return True

        # Search left
        left_board = self.move_left()
        # print("left_board",left_board)
        if (left_board != 'unavailable' and self.left == 'untravelled'):
            left_state = State(left_board,parent=self,right="travelled",depth=self.depth+1)
            if (left_state.search() == True):
                return True
        
        # Search right
        right_board = self.move_right()
        # print("right_board",right_board)
        if (right_board != 'unavailable' and self.right == 'untravelled'):
            right_state = State(right_board,parent=self,left="travelled",depth=self.depth+1)
            if (right_state.search() == True):
                return True
        

    def print_state(self):
        print('Visited at depth:', self.depth)
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
        

state = State(init_state)
state.search()







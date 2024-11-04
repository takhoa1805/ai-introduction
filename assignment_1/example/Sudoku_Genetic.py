import random

class Sudoku:
    def __init__(self, grid):
        self.grid = grid

    def is_valid(self, row, col, num):
        for x in range(9):
            if self.grid[row][x] == num or self.grid[x][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.grid[i + start_row][j + start_col] == num:
                    return False
        return True

    def solve(self):
        empty = self.find_empty()
        if not empty:
            return True
        row, col = empty
        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.grid[row][col] = num
                if self.solve():
                    return True
                self.grid[row][col] = 0
        return False

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None

def genetic_algorithm(sudoku):
    population = [sudoku.grid]
    for _ in range(1000):
        new_population = []
        for individual in population:
            if Sudoku(individual).solve():
                return individual
            new_population.append(mutate(individual))
        population = new_population
    return None

def mutate(individual):
    row = random.randint(0, 8)
    col1, col2 = random.sample(range(9), 2)
    individual[row][col1], individual[row][col2] = individual[row][col2], individual[row][col1]
    return individual

# Example Sudoku grid (0 represents empty cells)
sudoku_grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

sudoku = Sudoku(sudoku_grid)
solution = genetic_algorithm(sudoku)
print(solution)

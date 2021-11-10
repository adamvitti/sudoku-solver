import sys
from itertools import combinations
from z3 import *

#Paste sudoku board here:
sudokuInput = [ [6, 0, 0, 0, 8, 0, 0, 0, 1] , [0, 3, 0, 7, 0, 0, 6, 0, 0] , [0, 0, 0, 0, 1, 0, 0, 0, 7] , [0, 5, 0, 0, 3, 8, 4, 0, 0] , [3, 0, 0, 0, 4, 0, 0, 0, 0] , [0, 0, 4, 0, 0, 0, 0, 5, 3] , [0, 1, 0, 0, 0, 3, 0, 6, 0] , [0, 0, 3, 9, 0, 0, 0, 8, 5] , [9, 2, 8, 1, 0, 0, 3, 0, 0] ]

#Checks that the input of the sudoku board is formatted properly with correct values 1-9
if (len(sudokuInput) != 9):
    print('Invalid Sudoku input')
    sys.exit()
for row in sudokuInput:
    if(len(row) != 9):
        print('Invalid Sudoku input')
        sys.exit()
    for value in row:
        if(value < 0 or value > 9):
            print('Value in sudoku board is not within integer range 1-9!')
            sys.exit()


# Creates z3 solver and holder with variables for Z3 to solve (solves all the 0 zero spaces on board)
mySolver = Solver()

z3Variables = [[] for i in range(9)]
for i in range(9):
    z3Variables[i] = Ints("X%s%s" % (i,j) for j in range(9))



# Initializes the z3 variables to either the board value, or sets the solver constraint for the unkown variable from 1-9
for i in range(len(sudokuInput)):
    for j in range(len(sudokuInput[i])):

        # Values of 0 represent unkown value, whereas anything else is already known
        if sudokuInput[i][j] != 0:
            mySolver.add(z3Variables[i][j] == sudokuInput[i][j])
        else:
            mySolver.add(z3Variables[i][j] >= 1)
            mySolver.add(z3Variables[i][j] <= 9)

# Defines the rows within our board and adds constraints to Z3 solver:
for row in z3Variables:
    #Checks uniqueness of values in each row (makes sure 1-9 is only used once per row)
    for vals in combinations(row, 2):
        x, y = list(vals)
        mySolver.add(x != y)

    #Adds Z3 solver constraint that states the sum of row values should add to 45 (1+2+3+ ... + 9 = 45)
    mySolver.add(sum(row) == 45)

# Defines the columns within our board and adds constraints to the Z3 solver: 
for j in range(9):
    columnValues = []
    for i in range(9):
        columnValues.append(z3Variables[i][j])

    for vals in combinations(columnValues, 2):
        x, y = list(vals)
        mySolver.add(x != y)

    #Adds Z3 solver constraint that states the sum of row values should add to 45 (1+2+3+ ... + 9 = 45)
    mySolver.add(sum(columnValues) == 45)

# Defines the 3x3 grids within our 9x9 board and adds constraints to Z3 solver:
for i in range(0, 9, 3): 
    for j in range(0, 9, 3):
        gridValues = []

        for x in range(i, i + 3):
            for y in range(j, j + 3):
                gridValues.append(z3Variables[x][y])

    #Checks uniqueness of values in grid (makes sure 1-9 is only used once per grid)
    for vals in combinations(gridValues, 2):
        x, y = list(vals)
        mySolver.add(x != y)

    #Adds Z3 solver constraint that states the sum of grid values should add to 45 (1+2+3+ ... + 9 = 45)
    mySolver.add(sum(gridValues) == 45)

result = mySolver.check()
if result == sat:
    model = mySolver.model()
    solvedSudoku = sudokuInput
    print("Solved Sudoku:")
    for i in range(9):
        for j in range(9):
            if solvedSudoku[i][j] == 0:
                solvedSudoku[i][j] = model[z3Variables[i][j]]

    for row in solvedSudoku:
        print(row)

else:
    print('Cannot solve this Sudoku Puzzle!')



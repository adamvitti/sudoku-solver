import sys
import random
import copy
import time

# Class Cell from sudoku.py file provided by https://github.com/JoeKarlsson/Python-Sudoku-Generator-Solver
class cell():
    """ Initilalizes cell object. A cell is a single box of a sudoku puzzle. 81 cells make up the body of a
        sudoku puzzle. Initializes puzzle with all possible answers available, solved to false, and position of cell within the
        sudoku puzzle"""
    def __init__(self, position):
        self.possibleAnswers = [1,2,3,4,5,6,7,8,9]
        self.answer = None
        self.position = position
        self.solved = False
        
    def remove(self, num):
        """Removes num from list of possible anwers in cell object."""
        if num in self.possibleAnswers and self.solved == False:
            self.possibleAnswers.remove(num)
            if len(self.possibleAnswers) == 1:
                self.answer = self.possibleAnswers[0]
                self.solved = True
        if num in self.possibleAnswers and self.solved == True:
            self.answer = 0

    def solvedMethod(self):
        """ Returns whether or not a cell has been solved"""
        return self.solved

    def checkPosition(self):
        """ Returns the position of a cell within a sudoku puzzle. x = row; y = col; z = box number"""
        return self.position

    def returnPossible(self):
        """ Returns a list of possible answers that a cell can still use"""
        return self.possibleAnswers

    def lenOfPossible(self):
        """ Returns an integer of the length of the possible answers list"""
        return len(self.possibleAnswers)

    def returnSolved(self):
        """ Returns whether or not a cell has been solved"""
        if self.solved == True:
            return self.possibleAnswers[0]
        else:
            return 0
        
    def setAnswer(self, num):
        """ Sets an answer of a puzzle and sets a cell's solved method to true. This
            method also eliminates all other possible numbers"""
        if num in [1,2,3,4,5,6,7,8,9]:
            self.solved = True
            self.answer = num
            self.possibleAnswers = [num]
        else:
            print('Invalid entry.')
       
    def reset(self):
        """ Resets all attributes of a cell to the original conditions""" 
        self.possibleAnswers = [1,2,3,4,5,6,7,8,9]
        self.answer = None
        self.solved = False

def emptySudoku():
    # Creates a 9x9 game board with (row, col, box) coordinate system
    set = []
    for row in range(1,10):
        if row in [1, 2, 3]:
            z = 1
        if row in [4, 5, 6]:
            z = 4
        if row in [7, 8, 9]:
            z = 7
        for col in range(1,10):
            if col in [1, 2, 3]:
                box = z + 0
            if col in [4, 5, 6]:
                box = z + 1
            if col in [7, 8, 9]:
                box = z + 2
            c = cell((row, col, box))
            set.append(c)
    return set

# printSudoku from sudoku.py file provided by https://github.com/JoeKarlsson/Python-Sudoku-Generator-Solver
def printSudokuBoard(sudoku):
    '''Prints out a sudoku in a format for the solver! '''
    row1 = []
    row2 = []
    row3 = []
    row4 = []
    row5 = []
    row6 = []
    row7 = []
    row8 = []
    row9 = []
    for i in range(81):
        if i in range(0,9):
            row1.append(sudoku[i].returnSolved())
        if i in range(9,18):
            row2.append(sudoku[i].returnSolved())
        if i in range(18,27):
            row3.append(sudoku[i].returnSolved())
        if i in range(27,36):
            row4.append(sudoku[i].returnSolved())
        if i in range(36,45):
            row5.append(sudoku[i].returnSolved())
        if i in range(45,54):
            row6.append(sudoku[i].returnSolved())
        if i in range(54,63):
            row7.append(sudoku[i].returnSolved())
        if i in range(63,72):
            row8.append(sudoku[i].returnSolved())
        if i in range(72,81):
            row9.append(sudoku[i].returnSolved())
    print(row1[0:3],row1[3:6],row1[6:10])
    print(row2[0:3],row2[3:6],row2[6:10])
    print(row3[0:3],row3[3:6],row3[6:10])
    print('')
    print(row4[0:3],row4[3:6],row4[6:10])
    print(row5[0:3],row5[3:6],row5[6:10])
    print(row6[0:3],row6[3:6],row6[6:10])
    print('')
    print(row7[0:3],row7[3:6],row7[6:10])
    print(row8[0:3],row8[3:6],row8[6:10])
    print(row9[0:3],row9[3:6],row9[6:10])



def generator():
    Cells = [i for i in range(81)] # Cells refers to unset positions on the board
    Game = emptySudoku()
    while len(Cells) != 0: # While loop will end once all positions on the board have been given an answer
        Least = []
        Lowest = []
        for i in Cells:
            Least.append(Game[i].lenOfPossible()) #Finds the number of possible answers for each remaining cell
        Minimum = min(Least) #Finds the cell with the least number of possible answers
        for i in Cells:
            if Game[i].lenOfPossible() == Minimum:
                Lowest.append(Game[i])
        choice = random.choice(Lowest)
        possible = choice.returnPossible()
        index = Game.index(choice)
        Cells.remove(index)
        final = random.choice(possible)
        P1 = choice.checkPosition()
        choice.setAnswer(final)
        if ruleCheck(Game):
            for n in range(len(Game)):
                P2 = Game[n].checkPosition()
                if P1[0] == P2[0] or P1[1] == P2[1] or P1[2] == P2[2]:
                    Game[n].remove(final)
    return Game

def ruleCheck(game):
    # Checks whether or not the game follows sudoku rules. One integer 1 - 9 in each row, column, and box
    for x in range(len(game)):
        for y in range(len(game)):
            P1 = game[x].checkPosition()
            P2 = game[y].checkPosition()
            if x != y:
                if P1[0] == P2[0] or P1[1] == P2[1] or P1[2] == P2[2]:
                    Val1 = game[x].returnSolved()
                    Val2 = game[y].returnSolved()
                    if Val1 == Val2:
                        return False
            return True

def solver(game):
    # Iterates through the cells to check if game is solvable without guessing, if a guess is required
    # the function returns False, if it is solvable without guessing it returns True
    cells = [y for y in range(81)]
    duplicate = copy.deepcopy(game)
    cnt = 0
    while len(cells) != 0:
        for y in cells:
            if duplicate[y].solved or duplicate[y].lenOfPossible == 1:
                ans = duplicate[y].returnPossible()
                duplicate[y].setAnswer(ans[0])
                P1 = duplicate[y].checkPosition()
                for i in range(len(duplicate)):
                    if y != i:
                        P2 = duplicate[i].checkPosition()
                        if P1[0] == P2[0] or P1[1] == P2[1] or P1[2] == P2[2]:
                            val = duplicate[y].returnSolved()
                            duplicate[i].remove(val)
                            #index = game.index(game[y])
                            #cells.remove(game[y])
                            cnt = 0
            else:
                cnt += 1
                if cnt > (len(cells) + 3):
                    return False
        break
    return True

def show(game):
    # Randomly selects a spot on the board and removes the value, which will then check to see if the board
    # is still solvable
    cells = [] # the cells that still contain a shown value
    board = game
    i = 81
    while i != 0:
        for x in range(81):
            cells.append(board[x])
        if solver(board):
            choice = random.choice(cells)
            value = choice.returnSolved()
            choice.reset()
            if solver(board):
                #index = game.index(choice)
                #cells.remove(index)
                i -= 1
            else:
                choice.setAnswer(value)
                #index = game.index(choice)
                #cells.remove(index)
                i -= 1

    return board
            
        

def checkValid(base,game):
    # Checks values against each other
    for x in range(0,81):
        if base[x].possibleAnswers != game[x].possibleAnswers:
            return 1
        else:
            return 0

def printSudokuOutput(sudoku):
    row1 = []
    row2 = []
    row3 = []
    row4 = []
    row5 = []
    row6 = []
    row7 = []
    row8 = []
    row9 = []
    for i in range(81):
        if i in range(0,9):
            row1.append(sudoku[i].returnSolved())
        if i in range(9,18):
            row2.append(sudoku[i].returnSolved())
        if i in range(18,27):
            row3.append(sudoku[i].returnSolved())
        if i in range(27,36):
            row4.append(sudoku[i].returnSolved())
        if i in range(36,45):
            row5.append(sudoku[i].returnSolved())
        if i in range(45,54):
            row6.append(sudoku[i].returnSolved())
        if i in range(54,63):
            row7.append(sudoku[i].returnSolved())
        if i in range(63,72):
            row8.append(sudoku[i].returnSolved())
        if i in range(72,81):
            row9.append(sudoku[i].returnSolved())
    print('[',row1,',',row2,',',row3,',',row4,',',row5,',',row6,',',row7,',',row8,',',row9,']')


base = generator()
game = show(base)

print('Here is the Sudoku board:')
printSudokuBoard(game)

print('\nCopy this output format for our Z3 Solver:\n')
printSudokuOutput(game)
print('')


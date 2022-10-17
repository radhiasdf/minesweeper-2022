import random
import pygame

mineratio = 5 # There's a mine in every [] squares
num_rows, num_cols = 8,8

num_mines = int(round((num_rows*num_cols)/mineratio))
print("mines: " + str(num_mines))

field = [[0 for i in range(num_rows)] for j in range(num_cols)]

minecount = num_mines
mine = -1

# adding mines
while minecount > 0:
    row, col = random.randint(0, num_rows-1), random.randint(0, num_rows-1)
    print(row, col)
    if field[row][col] != mine:
        field[row][col] = mine
        minecount = minecount - 1


for row in field: print(row)

fielddisplay = [["" for i in range(num_rows)] for j in range(num_cols)]
#for row in fielddisplay: print(row)

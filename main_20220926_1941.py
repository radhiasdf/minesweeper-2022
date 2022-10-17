import random
import pygame

mineratio = 5  # There's a mine in every [] squares, 5 is hard, 8 is easy
num_rows, num_cols = 8, 6
num_mines = int(round((num_rows * num_cols) / mineratio))
print("mines: " + str(num_mines))

field = [[0 for _ in range(num_cols)] for _ in range(num_rows)]

minecount = num_mines
mine = 'X'

# adding mines
while minecount > 0:
    row, col = random.randint(0, num_rows - 1), random.randint(0, num_cols - 1)
    print(row, col)
    if field[row][col] != mine:
        field[row][col] = mine
        minecount -= 1

# adding number indicators for every non-bomb cell, with checking if out of range
for row in range(num_rows):
    for col in range(num_cols):
        count = 0
        if field[row][col] != mine:
            if col > 0:
                if field[row][col - 1] == mine: count += 1  # left
            if col < num_cols - 1:
                if field[row][col + 1] == mine: count += 1  # right
            if row > 0:
                if field[row - 1][col] == mine: count += 1  # up
            if row < num_rows - 1:
                if field[row + 1][col] == mine: count += 1  # down

            if row > 0 and col > 0:
                if field[row - 1][col - 1] == mine: count += 1  # top left
            if row > 0 and col < num_cols - 1:
                if field[row - 1][col + 1] == mine: count += 1  # top right
            if row < num_rows - 1 and col > 0:
                if field[row + 1][col - 1] == mine: count += 1  # bottom left
            if row < num_rows - 1 and col < num_cols - 1:
                if field[row + 1][col + 1] == mine: count += 1  # bottom right
            field[row][col] = count

for row in field: print(row)

fielddisplay = [["" for i in range(num_rows)] for j in range(num_cols)]
# for row in fielddisplay: print(row)

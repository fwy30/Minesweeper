import random
# The docstring and comments are the same as
# these functions in Minesweeper.py file


def randomgrid(xl, yl, thres):
    grid = [[0 for i in range(xl)] for j in range(yl)]
    for i in range(yl):
        for j in range(xl):
            if random.random() > 1 - thres:
                grid[i][j] = 9
            else:
                grid[i][j] = 0

    for m in range(yl):
        for n in range(xl):
            if grid[m][n] == 0:
                num = findnieghbor(grid, n, m)
                grid[m][n] = num
    return grid


def findnieghbor(grid, x, y):
    neighboor = []
    num = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if pos_chk(x + i, y + j):
                neighboor.append([x + i, y + j])
    neighboor.remove([x, y])
    for block in neighboor:
        a, b = block
        if grid[b][a] == 9:
            num = num + 1
    return num


def pos_chk(x, y):
    xl = 9
    yl = 8
    # print(xl, yl)
    if x >= 0 and x < xl and y >= 0 and y < yl:
        return True
    else:
        return False


print(randomgrid(9, 8, 0.1))

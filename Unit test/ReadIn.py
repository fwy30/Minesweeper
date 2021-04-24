def read_grid(file_name):
    grid = []
    file = open(file_name, "r")
    lines = file.readlines()
    # grid is stored in the lines between GRID START AND GRID STOP
    grid_start = lines.index('GRID START\n')
    grid_end = lines.index('GRID STOP\n')
    y_length = grid_end - grid_start - 1
    # number in grid is separated by space
    first_line = lines[grid_start + 1].replace(' ', '')
    x_length = int((len(first_line) - 1))
    # print(lines)

    grid = [[0 for i in range(x_length)] for j in range(y_length)]

    # In the grid, 9 means mines position (all position in the grid
    # will have at most 8 neighboors, so number is will never be used),
    # and other numbers mean the number of mines in their neighbourhood
    for k in range(y_length):
        each_line = lines[grid_start + 1 + k].replace(' ', '')
        for q, p in enumerate(each_line):
            if p != '\n':
                grid[k][q] = int(p)
    return grid

print(read_grid("grid81.txt"))
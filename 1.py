import tkinter as tk
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import messagebox


def read_grid(file_name):
    '''
    Reads in a bff file and breaks down the file
    into different blocks which are represented by
    A, B, C, X, and O. After the data is processed
    the code will return the grid, type and number of blocks available,
    initial lazor position and direction, and list of target points.

    **Parameters**

        file_name: *str*
            The bff file from the Lazor game

    **Returns**
        grid: *list*
            List of list to represent available points and occupied
            points.

        block: *list*
            List of blocks that fall into A, B or C category. A meaning
            reflect block, B meaning opaque block, C meaning refract block.

        lazorposition: *list*
            List of integers representing the position and direction
            inside of the grid the lazor is.

        point: *list*
            List of integers representing the target points
            inside of the grid.
    '''
    grid = []
    file = open(file_name, "r")
    lines = file.readlines()
    grid_start = lines.index('GRID START\n')
    grid_end = lines.index('GRID STOP\n')
    y_length = grid_end - grid_start - 1
    first_line = lines[grid_start + 1].replace(' ', '')
    x_length = int((len(first_line) - 1))
    print(lines)

    grid = [[0 for i in range(x_length)] for j in range(y_length)]

    for k in range(y_length):
        each_line = lines[grid_start + 1 + k].replace(' ', '')
        for q, p in enumerate(each_line):
            if p != '\n':
                grid[k][q] = int(p)
    return grid


class Minesweeper:
    def __init__(self, tk, grid):
        self.tk = tk
        self.grid = grid
        self.x_length = len(grid[0])
        self.y_length = len(grid)

        num_mine = 0
        for i in range(self.y_length):
            for j in range(self.x_length):
                number = self.grid[i][j]
                if number == 9:
                    num_mine = num_mine + 1
        self.num_mine = num_mine

        mine = Image.open("bomb.jpg")
        mine = mine.resize((20, 20), Image.ANTIALIAS)
        self.mine = ImageTk.PhotoImage(mine)

        grass = Image.open("grass.jpeg")
        grass = grass.resize((20, 20), Image.ANTIALIAS)
        self.grass = ImageTk.PhotoImage(grass)

        self.safe = PhotoImage(file="flag.gif")

        zero = PhotoImage(file="clicked.gif")
        number = [zero]
        for i in range(1, 9):
            number.append(PhotoImage(file=str(i) + ".gif"))
        self.number = number

        self.frame = Frame(self.tk)
        self.frame.pack()
        self.info = [[0 for i in range(self.x_length)]
                     for j in range(self.y_length)]
        self.create_grid()
        return

    def create_grid(self):
        for i in range(self.y_length):
            for j in range(self.x_length):
                grass = self.grass
                number = self.grid[i][j]
                num_mine = 0
                state = False
                if number == 9:
                    state = True
                    num_mine = num_mine + 1
                info = {"posi": [i, j],
                        "button": Button(self.frame, image=grass),
                        "state": state,
                        "click": 0,
                        "num_mine": num_mine,
                        "number": number}

                info["button"] = Button(self.frame, image=grass)
                info["button"].bind('<Button-1>', self.left_event(i, j))
                info["button"].bind('<Button-3>', self.right_event(i, j))
                info["button"].grid(row=i, column=j)
                self.info[i][j] = info
        return

    # Create a wrapper for left click event, will call left_click
    # function to take response
    def left_event(self, i, j):
        return lambda x: self.left_click(self.info[i][j])

    def left_click(self, info):
        if info["state"]:
            info["button"].config(image=self.mine)
            info["button"].unbind('<Button-3>')
            self.goodgame()
            return
        if info['click'] == 0:
            info['click'] = 1
            # print(info)
            number = int(info["number"])
            info["button"].config(image=self.number[number])
            info["button"].unbind('<Button-3>')
        if self.check_step():
            self.wellplay()
            # print('1')
            return
        else:
            # print("2")
            return

    def right_event(self, i, j):
        return lambda x: self.right_click(self.info[i][j])

    def right_click(self, info):
        info["button"].config(image=self.safe)
        info["button"].unbind('<Button-1>')
        if info["state"]:
            self.num_mine = self.num_mine - 1
            print(self.num_mine)
        else:
            print("y")
        return

    def goodgame(self):
        retry = messagebox.askretrycancel(
            "Minesweeper", "You Lose! Try again?")
        # print(retry)
        if retry:
            self.create_grid()
        else:
            self.tk.quit()

    def wellplay(self):
        retry = messagebox.askyesno(
            "Minesweeper", "You Win! Try again?")
        # print(retry)
        if retry:
            self.create_grid()
        else:
            self.tk.quit()
        return

    def check_step(self):
        step = 0
        for i in range(self.y_length):
            for j in range(self.x_length):
                if not self.info[i][j]['state']:
                    if self.info[i][j]['click'] == 0:
                        step = step + 1
        print(step)
        if step == 0:
            return True
        else:
            return False


if __name__ == "__main__":
    g = read_grid('grid24.txt')
    print(g)
    # The Tk class is instantiated without arguments,
    # this create a main window of the minesweeper
    minesweeper = tk.Tk()
    # Create the class minesweeper object
    ms = Minesweeper(minesweeper, g)
    minesweeper.mainloop()

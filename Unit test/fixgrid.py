import tkinter as tk
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import messagebox
import copy


def read_grid(file_name):
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
    def __init__(self, tk, grider):
        self.tk = tk
        grid = grider
        self.grid = grider
        self.x_length = len(grid[0])
        self.y_length = len(grid)

        num_mine = 0
        num_flag = 0
        for i in range(self.y_length):
            for j in range(self.x_length):
                number = self.grid[i][j]
                if number == 9:
                    num_mine = num_mine + 1
                    num_flag = num_flag + 1
        self.num_mine = num_mine
        self.num_flag = copy.deepcopy(num_mine)

        mine = Image.open("bomb.jpg")
        mine = mine.resize((20, 20), Image.ANTIALIAS)
        self.mine = ImageTk.PhotoImage(mine)

        grass = Image.open("grass.jpeg")
        grass = grass.resize((20, 20), Image.ANTIALIAS)
        self.grass = ImageTk.PhotoImage(grass)

        self.safe = PhotoImage(file="flag.gif")
        self.plain = PhotoImage(file="0.gif")

        self.frame = Frame(self.tk)
        self.frame.pack()
        self.labels = {"mines": Label(self.frame, text="Mines: 0"),
                       "flags": Label(self.frame, text="Flags: 0")}

        self.labels["mines"].grid(
            row=0, column=0, columnspan=int(self.y_length / 2 - 1))
        self.labels["flags"].grid(row=0, column=int(
            self.y_length / 2) - 1, columnspan=int(self.y_length / 2 - 1))

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
        num_mine = 0
        for i in range(self.y_length):
            for j in range(self.x_length):
                number = self.grid[i][j]
                if number == 9:
                    num_mine = num_mine + 1
        self.num_mine = num_mine

        for i in range(self.y_length):
            for j in range(self.x_length):
                grass = self.grass
                number = self.grid[i][j]
                state = False
                if number == 9:
                    state = True
                info = {"posi": [i, j],
                        "button": Button(self.frame, image=grass),
                        "state": state,
                        "click": 0,
                        "number": number}
                # print(info)
                info["button"] = Button(self.frame, image=grass)
                info["button"].bind('<Button-1>', self.left_event(i, j))
                info["button"].bind('<Button-3>', self.right_event(i, j))
                info["button"].grid(row=i, column=j)
                self.info[i][j] = info
        self.labels["flags"].config(text="Flags: " + str(self.num_flag))
        self.labels["mines"].config(text="Mines: " + str(self.num_mine))
        return

    # Create a wrapper for left click event, will call left_click
    # function to take response
    def left_event(self, i, j):
        return lambda x: self.left_click(self.info[i][j])

    def left_click(self, info):
        y, x = info['posi']
        neighboor = []
        if info['number'] != 0:
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
        else:
            # print(x, y)
            neighboor = self.neighboor(x, y)
            number = int(info["number"])
            info["button"].config(image=self.plain)
            info["button"].unbind('<Button-3>')
            info['click'] = 1
            # print(neighboor)
            full_list = self.find_zero_neighboor(neighboor, x, y)
            for block in full_list:
                a, b = block
                print(a, b)
                if self.info[b][a]['number'] == 0:
                    self.info[b][a]["button"].config(image=self.plain)
                    self.info[b][a]["button"].unbind('<Button-3>')
                    self.info[b][a]['click'] = 1
                else:
                    number = self.info[b][a]['number']
                    self.info[b][a]["button"].config(image=self.number[number])
                    self.info[b][a]["button"].unbind('<Button-3>')
                    self.info[b][a]['click'] = 1

        if self.check_step():
            self.wellplay(True)
            # print('1')
            return
        else:
            # print("2")
            return

    def right_event(self, i, j):
        return lambda x: self.right_click(self.info[i][j])

    def right_click(self, info):
        i, j = info['posi']
        # if right click the unclicked button
        if info['click'] == 0:
            print(info)
            self.num_mine = self.num_mine - 1
            print(self.num_mine)
            if self.num_mine < 0:
                self.num_mine = 0
                messagebox.showinfo(
                    "Minesweeper", "You do not have more flags!")
                return
            else:
                info["button"].config(image=self.safe)
                info["button"].unbind('<Button-1>')
                info["click"] = 2
                self.num_flag = self.num_flag - 1
                self.labels["flags"].config(text="Flags: " + str(self.num_flag))

        # if right click the flagged button again
        elif info['click'] == 2:
            info["button"].config(image=self.grass)
            # info["button"].unbind('<Button-1>')
            info["click"] = 0
            self.num_mine = self.num_mine + 1
            info["button"].bind('<Button-1>', self.left_event(i, j))
            print(self.num_mine)
            self.num_flag = self.num_flag + 1
            self.labels["flags"].config(text="Flags: " + str(self.num_flag))
            return

    def goodgame(self):
        retry = messagebox.askretrycancel(
            "Minesweeper", "You Lose! Try again?")
        # print(retry)
        if retry:
            self.create_grid()
        else:
            self.tk.quit()

    def wellplay(self, TF):
        if TF:
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

    def find_zero_neighboor(self, neighboor, a, b):
        neighboor = neighboor
        full_list = [bl for bl in neighboor]
        zero = []
        new = []
        print(neighboor)
        state = False
        while not state:
            state = True
            for block in neighboor:
                x, y = block
                if self.info[y][x]['number'] == 0:
                    zero.append(block)
                    new = self.neighboor(x, y)
                    print('new', new)
                    for newblock in new:
                        p, q = newblock
                        print(p, q)
                        if self.info[q][p]['number'] == 0:
                            print("ss", p, q)
                            if newblock not in zero:
                                state = False
                                # zero.append(newblock)
                            if newblock not in full_list:
                                full_list.append(newblock)
                        else:
                            if newblock not in full_list:
                                full_list.append(newblock)

            neighboor = full_list
            # print(state)
        # print('f', full_list)
        # print(len(full_list))
        return full_list

    def neighboor(self, x, y):
        neighboor = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.pos_chk(x + i, y + j, self.grid):
                    neighboor.append([x + i, y + j])
        neighboor.remove([x, y])
        return neighboor

    def pos_chk(self, x, y, grid):
        xl = len(grid[0])
        yl = len(grid)
        # print(xl, yl)
        if x >= 0 and x < xl and y >= 0 and y < yl:
            return True
        else:
            return False


if __name__ == "__main__":
    g = read_grid('grid24.txt')

    # The Tk class is instantiated without arguments,
    # this create a main window of the minesweeper
    minesweeper = tk.Tk()
    # Create the class minesweeper object
    ms = Minesweeper(minesweeper, g)
    minesweeper.mainloop()
    # print(ms.pos_chk(0, 0))

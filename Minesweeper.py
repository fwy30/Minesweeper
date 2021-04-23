import tkinter as tk
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import messagebox
import random
import copy


def read_grid(file_name):
    '''
    Reads in a test file and converts it into a list of list. After that
    the code will return the default grid, and the default grid are required
    for the processing of the minesweeper game, however, you can choose to
    play random generated grid at three different difficult levels, but a
    default grid is also need in this case. Default grid can be customized
    by followed the instruction in any existing grid file.

    **Parameters**

        file_name: *str*
            The text file contains configuration of the minesweeper. Can be
            downloaded from the github website or custumized.

    **Returns**
        grid: *list*
            List of list to represent configuration of the grid.
    '''
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


class Minesweeper:
    '''
    Minesweeper class object contains functions to create frame and windows
    for game; function and wrapper of left and right click events; win and
    loss functions; functions to generate random grid, and functions to
    create a customize messagebox to ask for difficulty level.
    '''

    def __init__(self, tk, grider):
        '''
        class Minesweeper is initialized with a tk instance and a default
        grid you can choose to play random grid later but a default grid is
        required to start the game

        **Parameters**
            tk: *tkinter class*
                A tkinter instance
            grider: *list*
                List of list represent the confuguration of the default grid

        **Returns**
            None
        '''

        self.tk = tk
        # call the customize function to see if the player want to play
        # the defaulted grid, customized grid, or random grid (easy
        # middle, hard mode)
        if self.customize():
            # if the user want to play default grid, load the grid with
            # with the grider (default grid when initialized)
            grid = grider
        else:
            # if the user want to play random grid, call the difficulty
            # function to ask for difficulty (easy, middle, hard) the
            # user want to play
            self.difficulty()
            if v == 0:
                grid = self.randomgrid(9, 9, 0.10)
            elif v == 1:
                grid = self.randomgrid(16, 16, 0.15)
            else:
                grid = self.randomgrid(30, 16, 0.20)

        self.grid = grid
        self.x_length = len(grid[0])
        self.y_length = len(grid)

        # count the number of the mines and flags, the number of mines
        # is equal to the number of the flags
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

        # load the picture of the bomb, grass, flag, and numbers,
        # the source of these pictures are cited in readme file
        # in github
        mine = Image.open("bomb.jpg")
        mine = mine.resize((20, 20), Image.ANTIALIAS)
        self.mine = ImageTk.PhotoImage(mine)

        grass = Image.open("grass.jpeg")
        grass = grass.resize((20, 20), Image.ANTIALIAS)
        self.grass = ImageTk.PhotoImage(grass)

        self.safe = PhotoImage(file="flag.gif")
        self.plain = PhotoImage(file="0.gif")

        # create and pack the frame of the indicator of the mines and
        # flags
        self.frame = Frame(self.tk)
        self.frame.pack()
        self.labels = {"mines": Label(self.frame, text="Mines: 0"),
                       "flags": Label(self.frame, text="Flags: 0")}

        # make the indicator on the top the windows, and place mines
        # indicator in the left half and flags indicator in the right
        # half
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
        # info is the dictionary store the position, button,
        # mine state, click state and number on it
        self.info = [[0 for i in range(self.x_length)]
                     for j in range(self.y_length)]

        # call the create_grid function to create the grid
        self.create_grid()
        self.tk.mainloop()
        return

    def create_grid(self):
        '''
        creat_grid function is used to store the infomation of
        each position into self.info and create the windows of
        the game

        **Parameters**
            self: *object*

        **Returns**
            None
        '''

        # count the number of the mines
        num_mine = 0
        for i in range(self.y_length):
            for j in range(self.x_length):
                number = self.grid[i][j]
                if number == 9:
                    num_mine = num_mine + 1
        self.num_mine = num_mine

        # update the info dictionary for each block
        for i in range(self.y_length):
            for j in range(self.x_length):
                # when first started, all the button are grass pictures
                grass = self.grass
                number = self.grid[i][j]
                state = False
                # the state for mine is True
                if number == 9:
                    state = True

                # posi store the position of the block, the button store
                # response to left and right click, the state tells if
                # this block is a mine, and the number indicates the number
                # of mines in the neighbor of this block
                info = {"posi": [i, j],
                        "button": Button(self.frame, image=grass),
                        "state": state,
                        "click": 0,
                        "number": number}
                # print(info)
                # bind the left and right click event to the button and
                # display them in the window
                info["button"] = Button(self.frame, image=grass)
                info["button"].bind('<Button-1>', self.left_event(i, j))
                info["button"].bind('<Button-3>', self.right_event(i, j))
                info["button"].grid(row=i, column=j)
                self.info[i][j] = info

        # get the initial number of the flags and mines and disply them
        # on top of the frame
        self.labels["flags"].config(text="Flags: " + str(self.num_flag))
        self.labels["mines"].config(text="Mines: " + str(self.num_mine))
        return

    def left_event(self, i, j):
        '''
        left_event is a wrapper function for left click event, which will
        call left_click function to take response

        **Parameters**
            self: *object*
            i: *int*
                The row number of the block
            j: *int*
                The column number of the block

        **Returns**
            left_click function
        '''
        return lambda x: self.left_click(self.info[i][j])

    def left_click(self, info):
        '''
        left_click is a function for left click event, which will
        response to different situations based on the number of
        the button

        **Parameters**
            self: *object*
            info: *dictionary*
                info dictionary of this block

        **Returns**
            none
        '''

        # In posi, coordinate are stored in the way to represent
        # a position in the grid, for example, point in grid[3][5]
        # has x cordinate of 5 and y cordinate of 3, so to get y and
        # x value here need to swap y and x in sequence
        y, x = info['posi']
        neighboor = []
        # if the number is not 0
        if info['number'] != 0:
            # if it is a mine
            if info["state"]:
                # display the mine and loss message
                info["button"].config(image=self.mine)
                info["button"].unbind('<Button-3>')
                self.goodgame()
                return
            # if it is not a mine and not clicked (0)
            if info['click'] == 0:
                # change the click state to clicked (1)
                info['click'] = 1
                # print(info)
                # get the number of this block and update the
                # the picture on the block to its number picture
                number = int(info["number"])
                info["button"].config(image=self.number[number])
                info["button"].unbind('<Button-3>')

        # if the number is 0, display all the neighbors to boundary of
        # non zero number
        else:
            # print(x, y)
            # call the neighboor function to get the neighboor of this block,
            # change the block to plain picture and unbind the right click,
            # set the click state to clicked (1)
            neighboor = self.neighboor(x, y)
            number = int(info["number"])
            info["button"].config(image=self.plain)
            info["button"].unbind('<Button-3>')
            info['click'] = 1
            # print(neighboor)
            # get the full list of all the blocks cleared out by this click
            full_list = self.find_zero_neighboor(neighboor, x, y)

            # left click the blocks in the full list
            for block in full_list:
                a, b = block
                # print(a, b)
                # if this block is 0, display plain picture
                if self.info[b][a]['number'] == 0:
                    self.info[b][a]["button"].config(image=self.plain)
                    self.info[b][a]["button"].unbind('<Button-3>')
                    self.info[b][a]['click'] = 1
                # else if this block is number 1-8, display corresponding
                # number picture
                else:
                    number = self.info[b][a]['number']
                    self.info[b][a]["button"].config(image=self.number[number])
                    self.info[b][a]["button"].unbind('<Button-3>')
                    self.info[b][a]['click'] = 1

        # check if the player left clicked all the non mine block,
        # if yes, the player win
        if self.check_step():
            # if ture, display the win message
            self.wellplay(True)
            # print('1')
            return
        else:
            # print("2")
            return

    def right_event(self, i, j):
        '''
        right_event is a wrapper function for right click event, which will
        call right_click function to take response

        **Parameters**
            self: *object*
            i: *int*
                The row number of the block
            j: *int*
                The column number of the block

        **Returns**
            right_click function
        '''
        return lambda x: self.right_click(self.info[i][j])

    def right_click(self, info):
        '''
        right_click is a function for right click event, which will
        response to different situations based on the number of
        the button and the clicked state of the block

        **Parameters**
            self: *object*
            info: *dictionary*
                info dictionary in the block

        **Returns**
            none
        '''

        i, j = info['posi']
        # if right click the unclicked button
        if info['click'] == 0:
            # print(info)
            # reduce number of flag by 1
            self.num_flag = self.num_flag - 1
            # if there is no flag to use
            if self.num_flag < 0:
                self.num_flag = 0
                # show messagebox to warn no flags to use anymore
                messagebox.showinfo(
                    "Minesweeper", "You do not have more flags!")
                return
            # if there is remaining flags
            else:
                # change the picture to safe, and unbind the left click
                # event, and set the click states to flaged (2)
                info["button"].config(image=self.safe)
                info["button"].unbind('<Button-1>')
                info["click"] = 2
                # change the flag indicator in the top
                self.labels["flags"].config(
                    text="Flags: " + str(self.num_flag))

        # if right click the flagged button again
        elif info['click'] == 2:
            # change the picture back to grass
            info["button"].config(image=self.grass)
            # change the click state to not clicked
            info["click"] = 0
            # rebind the left click event after remove the flag
            info["button"].bind('<Button-1>', self.left_event(i, j))
            # print(self.num_mine)
            # add the number of flags by 1
            self.num_flag = self.num_flag + 1
            # change the flag indicator in the top
            self.labels["flags"].config(text="Flags: " + str(self.num_flag))
            return

    def goodgame(self):
        '''
        goodgame is function display the lose message, it will ask
        play if want to retry, if retry then reload the grid and restart,
        if cancel then quit the windows

        **Parameters**
            self: *object*

        **Returns**
            none
        '''

        retry = messagebox.askretrycancel(
            "Minesweeper", "You Lose! Try again?")
        # print(retry)
        if retry:
            # if retry restart the game
            self.create_grid()
        else:
            # if cancel quit the window
            self.tk.quit()

    def wellplay(self, TF):
        '''
        wellplay is function display the win message, it will ask
        play if want to retry, if retry then reload the grid and restart,
        if cancel then quit the windows

        **Parameters**
            self: *object*

        **Returns**
            none
        '''

        if TF:
            retry = messagebox.askyesno(
                "Minesweeper", "You Win! Try again?")
            # print(retry)
            if retry:
                # if retry restart the game
                self.create_grid()
            else:
                # if cancel quit the window
                self.tk.quit()
        return

    def check_step(self):
        '''
        check_step is function check if player wins, if the number of
        clicked block is equal to the non mine block number, the player
        wins and return True, otherwise return false

        **Parameters**
            self: *object*

        **Returns**
            boolean: True or False
        '''

        step = 0
        for i in range(self.y_length):
            for j in range(self.x_length):
                # for the Flase state block (not mine)
                if not self.info[i][j]['state']:
                    # count the number of the unclicked block and flagged block
                    if self.info[i][j]['click'] == 0 or self.info[i][j]['click'] == 2:
                        step = step + 1
        # print(step)
        # if step is 0, which means all non mine block are left clicked
        if step == 0:
            return True
        else:
            return False

    def find_zero_neighboor(self, neighboor, a, b):
        '''
        find_zero_neighboor is function check if player wins, if the number of
        clicked block is equal to the non mine block number, the player
        wins and return True, otherwise return false

        **Parameters**
            self: *object*
            neighboor: *list*
                the initial neighboor list of this number 0 point
            a: *int*
                the x position of this number 0 point
            b: *int*
                the y position of this number 0 point


        **Returns**
            full_list: *list*
                list of coordinates of all the related blocks with respect
                to this number 0 block, which will be left clicked (appear)
                at the same time
        '''

        # the neighboor is initially the neighboor of this number 0 point,
        # and it will become the full_list after each while loop to append
        # new number zero points
        neighboor = neighboor
        # append the full list with inital neighboors
        full_list = [bl for bl in neighboor]
        # the zero list store all the number 0 points coordinates
        zero = []
        # new list store the new neighboors of new number 0 point
        new = []
        # print(neighboor)
        # default state is False, which will become true inside the loop,
        # and if there is new number 0 block, it will turn False, if there
        # is no new number 0 block, it will keep True and quit the while loop
        state = False
        while not state:
            state = True
            for block in neighboor:
                x, y = block
                # if this neighboor is 0
                if self.info[y][x]['number'] == 0:
                    # append this neighboor into zero list
                    zero.append(block)
                    # find the new neighboor for this zero block
                    new = self.neighboor(x, y)
                    # print('new', new)
                    for newblock in new:
                        # get the new x, y position of the new neighboor
                        p, q = newblock
                        # print(p, q)
                        # if there is number 0 block in the neighboor
                        if self.info[q][p]['number'] == 0:
                            # print("ss", p, q)
                            # check if it is a new zero block
                            if newblock not in zero:
                                # if yes, change the state to False, and
                                # run the while loop again until no new
                                # zero block appended
                                state = False
                            # append the new zero block into full list if
                            # it is now in full list
                            if newblock not in full_list:
                                full_list.append(newblock)

                        # if the new neighboor is not 0
                        else:
                            # append the new neighboor into full list
                            # if it is not in full list
                            if newblock not in full_list:
                                full_list.append(newblock)
            # change the neighboor to full list to get new neighboors of
            # all zero blocks
            neighboor = full_list
            # print(state)
        # print('f', full_list)
        # print(len(full_list))
        return full_list

    def neighboor(self, x, y):
        '''
        neighboor is function find the neighboor of a specific point

        **Parameters**
            self: *object*
            x: *int*
                x position of this point
            y: *int*
                y position of this point

        **Returns**
            neighboor: List of position which are neighboor of this point
        '''

        neighboor = []
        # get the 9 blocks from (x-1, y-1) to (x+1, y+1)
        for i in range(-1, 2):
            for j in range(-1, 2):
                # check if this neighboor point is an availble point in grid
                if self.pos_chk(x + i, y + j, self.grid):
                    neighboor.append([x + i, y + j])
        # drop this point from the list, (x, y) is not neighboor of (x, y)
        neighboor.remove([x, y])
        return neighboor

    def pos_chk(self, x, y, grid):
        '''
        pos_chk is the function check the position of a specific point,
        and it will return True if this point is valid inside the grid,
        and return False if this point is not valid

        **Parameters**
            self: *object*
            x: *int*
                x position of this point
            y: *int*
                y position of this point
            grid: *list*
                list of list represent the configuration of the grid

        **Returns**
            boolean: True or False
        '''
        xl = len(grid[0])
        yl = len(grid)
        # print(xl, yl)
        # the criteria is x and y larger or equal to 0 and smaller than
        # their dimension
        if x >= 0 and x < xl and y >= 0 and y < yl:
            return True
        else:
            return False

    def customize(self):
        '''
        cusomize is the function check if the player want to play the default
        grid or random grid generated. A messagebox will appear and ask "Do
        you want to use default grid?" It will return True if player select
        yes, and return False if player select no

        **Parameters**
            self: *object*

        **Returns**
            boolean: True or False
        '''

        # create a message box ask question, and C is Ture if select yes
        # and C is False if select no
        C = messagebox.askyesno(
            "Minesweeper", "Do you want to use default grid?")
        if C:
            messagebox.showinfo(
                "Minesweeper", "You can change default grid in main block.")
            return True
        else:
            # print("You are playing random grid.")
            return False

    def randomgrid(self, xl, yl, thres):
        '''
        randomgrid is the function creates the random grid based on the
        x dimension, y dimension, and threshold (which is the probability
        of a block to be a mine)

        **Parameters**
            self: *object*
            xl: *int*
                x dimension of the grid
            yl: *int*
                y dimension of the grid
            thres: 'float'
                probability of a block to be mine

        **Returns**
            grid: *list*
                List of list represents the configuration of the grid
        '''

        grid = [[0 for i in range(xl)] for j in range(yl)]
        for i in range(yl):
            for j in range(xl):
                # random.random generate a float number between 0 and 1,
                # if this number is larger than 1-thres, it will be mine
                if random.random() > 1 - thres:
                    grid[i][j] = 9
                # if this number is smaller than 1-thres, it will be stored
                # as 0, and get its number later
                else:
                    grid[i][j] = 0

        for m in range(yl):
            for n in range(xl):
                # for all the non mine block, use the findneighbor to get
                # the number of the mine within its neighbor
                if grid[m][n] == 0:
                    num = self.findnieghbor(grid, n, m)
                    grid[m][n] = num
        return grid

    def findnieghbor(self, grid, x, y):
        '''
        findnieghbor is the function which find the number of mines within
        the neighbor of a specifc point

        **Parameters**
            self: *object*
            gird: *list*
                List of list represents the configuration of the grid
            x: *int*
                x dimension of the grid
            y: *int*
                y dimension of the grid

        **Returns**
            num: *int*
                The number of mines within the neighbor of a specifc point
        '''

        neighboor = []
        num = 0
        # get all the nine neighboors from (x-1, y-1) to (x+1, y+1)
        for i in range(-1, 2):
            for j in range(-1, 2):
                # if this is a valid point, append this neighboor
                if self.pos_chk(x + i, y + j, grid):
                    neighboor.append([x + i, y + j])
        # drop the point itself (x, y)
        neighboor.remove([x, y])
        for block in neighboor:
            a, b = block
            # count the number of mines in its neighbors
            if grid[b][a] == 9:
                num = num + 1
        return num

    def difficulty(self):
        '''
        difficulty is the function which create a customized message box
        and ask player which difficulty level of the random generated grid
        the player want to play. Three levels are available, easy (grid size
        9 * 9 with 10% of the mines), middle (grid size 16 * 16 with 15% of
        the mines), hard (grid size 30 * 16 with 20% of the mines)

        **Parameters**
            self: *object*

        **Returns**
            none
        '''

        # create a tkinter windows, display the message, and create 3 buttons
        # each button is call select function to give values to a global
        # variable V to indicate which difficulty level the user choose
        t = tk.Tk()
        label = Label(
            t, text="Please choose your difficulty level", justify=LEFT)
        label.pack(padx=20, pady=15)
        easy = Button(t, text="Easy", width=8,
                      command=lambda: self.select(t, 0))
        easy.pack(padx=5, pady=10, side=LEFT)
        middle = Button(t, text="Middle", width=8,
                        command=lambda: self.select(t, 1))
        middle.pack(padx=20, side=LEFT)
        hard = Button(t, text="Hard", width=8,
                      command=lambda: self.select(t, 2))
        hard.pack(pady=10, side=RIGHT)
        t.mainloop()
        return

    def select(self, t, val):
        '''
        select is the function which gives value to a global variable v
        and pass it to initial function to start create random grid of
        specific size

        **Parameters**
            self: *object*
            t: *tkinter object*
                used to displace the message windows
            val:
                value used to pass to the global variables

        **Returns**
            none
        '''

        global v
        v = val
        # destroy the windows and quit the t tkinter object
        t.withdraw()
        t.destroy()
        t.quit()
        return


if __name__ == "__main__":
    # read in a default grid, can be customized based on the
    # instruction in readme file
    g = read_grid('grid24.txt')
    # The Tk class is instantiated without arguments,
    # this create a main window of the minesweeper
    minesweeper = tk.Tk()
    # Create the class minesweeper object
    ms = Minesweeper(minesweeper, g)
    # minesweeper.mainloop()

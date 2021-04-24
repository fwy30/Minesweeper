# Minesweeper


## Background and Introduction
Minesweeper was originated from a classic puzzle video game in 1960s, and it has been written for computer platforms in 1990s. In the game, player need to left click to explore each button in the grid and use right click to put flags to sweep the buttons with mines. The player wins if all the buttons without mines are left clicked, and the player loses if button with mine are left clicked.


## Project scope
1. A read in function to read in the customized minesweeper grid.
2. A Minesweeper class with initial function.
3. A create grid function to generate a platform to display the minesweeper grid and bind the left and right click events to each button.
4. Functions and wrapper function for left and right click events.
5. Functions to show win and lose message boxes.
6. Function to check if win criteria is met. 
7. Function to calculate and combine neighbors and left click them when clicking on a button with number 0.
8. Function to add counters for flags and mines.
9. Functions to generate random grid, calculate the number of each non mines blocks.
10. Functions to generate a window and ask if player want to play default grid or random grid, and offer 3 different difficulty levels with different grid size and different mine percentages.
11. Some default grids that user can play around (grid24, grid24-2, grid81, grid81-2).
12. Some unit test files for function or functions (fixgrid is unit test for fix grid withour asking and generating random grid, RandomGrid is unit test for generate a list of list which represents the configuration of the grid of desired grid size and percent mine, CustomMessagebox is the unit test for displaying a windows asks for difficulty and give values to a global variable v).
13. A readme file explains the game (this file).
14. Some snapshots of the game.

## Instruction:
Download the Minesweeper.py file, or download the Minesweeper.zip file and unzip the folder. Put all the picture files (.gif, .jpg, .jpeg file) and the default grid (ect. grid24.txt) together with Minesweeper.py file. Change the path inside the code if needed (change path of the default grid file in main block, and change the path of the picture in the initial function of the Minesweeper object). 

You will need a default grid to start the game, however, there will be a window before game starts asking you if you want to play default grid, you can play random grid if you choose no, and you will then pick a difficulty level (easy: 9 * 9 grid with 10% of mines, middle: 16 * 16 grid with 15% of mines, hard: 30 * 16 with 20% of mines). 

When the game starts, there will be a counter on the top indicates the number of mines and number of the flags, the number of the flags is equal to the number of the mines in the begining of the game. The number of mines is constant when the grid is generated, and it will not change no matter if you flag a mines or flag a non mine block (or you can just flag all the blocks to see which blocks change the number of mines). The number of flags will decrease by 1 when you right click a unclicked block and increase by 1 when you unflag a block already with flag on it. Different from the Minesweeper game in Windows operating system (where you can make more flags than mines, and the flag counter will be negative if you put more flags than mines), there will be a warning message telling you that you do not have enough flags when the number of flag you put exceed the number of mines. You can not flag a block which is already left clicked, and you also cannot left click a block with flag on it (you have to deflag this block first). Note that you are not required to flag all the mines to win, if you find (left-click) all the non mine blocks, you will win; and you will lose if you left click any mines. 

## Customize grid
There are four default grids (grid24, grid24-2, grid81, grid81-2), in the grid, each block is represented by a number which indicate the number of mines in its neighboors. Since a block will have at most 8 neighboors, the maximum number of the number will be 8, and number 9 is not used. Therefore, number 9 is used to represent the mines position. To customize your own grid, open a text file and start a line with "GRID START", then start new lines with the blocks. In each lines, number of each blocks is separated by space, and the length of the numbers in each line represents the length of the x axis of the grid. The number of the lines represents length of the y axis, and each row will start at a new line. After constructing your grid, start a new lines with "GRID STOP", and also start another new line with blank. 

Also notice there is unit test file named RandomGrid.py, you can also generate random grid with your favorite dimension and mines number in that file and copy and paste them into a text file and modified them into correct format.


### Grid example:
GRID START

1 9 1 1 9 2 9 1 0

2 2 1 1 1 2 2 2 1

9 1 1 1 2 1 2 9 1

3 3 2 9 2 9 2 1 1

9 9 3 2 3 2 2 1 0

2 2 2 9 2 2 9 1 0

0 0 1 2 9 2 1 1 0

0 0 0 1 1 1 0 0 0

0 0 0 0 0 0 0 0 0

GRID STOP


(notice to leave a blank line after GRID STOP)


## Citation:

### grass: https://www.pexels.com/search/grass/

### mine: https://www.amymittelman.com/subscription-bomb/

### flag and number: https://commons.wikimedia.org/wiki/Main_Page

### some tkinter syntax is learnt from: 
### https://docs.python.org/3/library/tkinter.html
### https://www.geeksforgeeks.org/python-gui-tkinter/

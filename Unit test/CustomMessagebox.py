from tkinter import *
# The docstring and comments are the same as
# these functions in Minesweeper.py file
root = Tk()
root.title("Main Window")


def select(val):
    global v
    v = val
    root.withdraw()
    root.destroy()
    return


def new():
    label = Label(
        root, text="Please choose your difficulty level", justify=LEFT)
    label.pack(padx=20, pady=15)
    easy = Button(root, text="Easy", width=8, command=lambda: select(0))
    easy.pack(padx=5, pady=10, side=LEFT)
    middle = Button(root, text="Middle", width=8, command=lambda: select(1))
    middle.pack(padx=20, side=LEFT)
    hard = Button(root, text="Hard", width=8, command=lambda: select(2))
    hard.pack(pady=10, side=RIGHT)


new()
root.mainloop()
print(v)

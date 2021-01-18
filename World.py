#from tkinter import *
import tkinter as tk
master = tk.Tk()

master.title("Maze Assistant")
master.geometry("200x150")
master.configure(bg="red")
Width = 50
(x,y)=(5,5)
board=tk.Canvas(master, width=x*Width, height=y*Width)


def render_grid():
    global specials, walls, Width, x, y, player
    for i in range(x):
        for j in range(y):
            board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="white", width=1)
            temp = {}
            
    for (i, j, c, w) in specials:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill=c, width=1)
    for (i, j) in walls:
        board.create_rectangle(i * Width, j * Width, (i + 1) * Width, (j + 1) * Width, fill="black", width=1)

render_grid()

master.mainloop()


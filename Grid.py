from tkinter import *
from tkinter.ttk import *

#Color values
RED = '#f05454'
BLUE = '#0e49b5'
AQUA = '#8bcdcd'
GREEN = '#83a95c'
BLACK = '#000000'
WHITE = '#ffffff'
GREY = '#555555'

#Main window setup
root = Tk()
root.title("Path finding")
root.geometry("510x550")
root.resizable(0, 0)

WIDTH = 500
HEIGHT = 500
SIZE = 20
INFINTE = 10000 #Any big number with respect to grid size

start = None
target = None
obstacle = []


class Node():
    def __init__(self, pos):
        self.pos = pos
        self.h = INFINTE
        self.g = INFINTE
        self.parent = None
    
    def f(self):
        return self.h + self.g

    def __eq__(self, other):
        return self.pos == other.pos

    def __ne__(self, other):
        return self.pos != other.pos

    #For debug purpose
    def __str__(self):
        return "["+str(self.pos[0])+", "+str(self.pos[1])+"]"


#Main canvas class
class mCanvas(Canvas):
    def __init__(self, root, width, height, gridSize):
        super().__init__(root, width=width, height=height,background="white")
        self.bind("<Button-1>", self.setMode)
        self.bind("<B1-Motion>", self.draw)
        self.bind("<Button-3>", self.erase)
        self.bind("<B3-Motion>", self.erase)
        self.width = width
        self.height = height
        self.gridSize = gridSize
        self.drawGrid(gridSize)
        self.mode = 0

    def erase(self, event):
        x = (event.x//self.gridSize)*self.gridSize + self.gridSize/2
        y = (event.y//self.gridSize)*self.gridSize + self.gridSize/2
        a, b = int((x-SIZE/2)/SIZE)-1, int((y-SIZE/2)/SIZE)-1

        if [a,b] in obstacle:
                self.mark(x,y,WHITE)
                obstacle.remove([a,b])

    def draw(self, event):
        if self.mode > 1:
            self.setO(event)

    def setMode(self, event):
        if self.mode == 0:
            self.setS(event)
            info.config(text="*Set target position*",foreground=RED)
            self.mode += 1
        elif self.mode == 1:
            info.config(text="Draw the obstacle",foreground=BLACK)
            self.setT(event)
            self.mode += 1
        else:
            self.setO(event)
    
    #Set obstacle
    def setO(self, event):
        x = (event.x//self.gridSize)*self.gridSize + self.gridSize/2
        y = (event.y//self.gridSize)*self.gridSize + self.gridSize/2
        a, b = int((x-SIZE/2)/SIZE)-1, int((y-SIZE/2)/SIZE)-1

        if [a,b] != start and [a,b] != target:
            if [a,b] not in obstacle:
                self.mark(x,y,BLACK)
                obstacle.append([a,b])

    #Set starting position
    def setS(self, event):
        #Position of click on the canvas
        x = (event.x//self.gridSize)*self.gridSize + self.gridSize/2
        y = (event.y//self.gridSize)*self.gridSize + self.gridSize/2

        #Index of the clicked block
        a, b = int((x-SIZE/2)/SIZE)-1, int((y-SIZE/2)/SIZE)-1
        if [a,b] not in obstacle and [a,b] != target:
            global start 
            if start != None:
                if start != [a,b]:
                    self.mark(start[0], start[1],WHITE)
                    start = [a,b]
                self.mark(x,y,BLUE)
            else:
                start = [a,b]
                self.mark(x,y,BLUE)

    #Set target position
    def setT(self, event):
        #Position of click on the canvas
        x = (event.x//self.gridSize)*self.gridSize + self.gridSize/2
        y = (event.y//self.gridSize)*self.gridSize + self.gridSize/2

        #Index of the clicked block
        a, b = int((x-SIZE/2)/SIZE)-1, int((y-SIZE/2)/SIZE)-1
        if [a,b] not in obstacle and [a,b] != start:
            global target 
            if target != None:
                if target != [a,b]:
                    self.mark(target[0], target[1],WHITE)
                    target = [a,b]
                self.mark(x,y,RED)
            else:
                target = [a,b]
                self.mark(x,y,RED)

    #Mark position x,y on the grid with color 'color'
    def mark(self, x, y, color):
        x1 = (x//self.gridSize)*self.gridSize
        x2 = ((x//self.gridSize) + 1)*self.gridSize
        y1 = (y//self.gridSize)*self.gridSize
        y2 = ((y//self.gridSize) + 1)*self.gridSize
        self.create_rectangle(x1,y1,x2,y2,fill=color , outline=GREY, width=1)

    #Draw the grid at start
    def drawGrid(self, size):
        for i in range(0,self.width,size):
            for j in range(0,self.height,size):
                if i == 0 or i == self.width - size:
                    self.mark(i,j,BLACK)
                    #obstacle.append([i,j])
                elif j == 0 or j == self.height-size:
                    self.mark(i,j,BLACK)
                    #obstacle.append([i,j])
                else:
                    self.mark(i,j,WHITE)

grid = [[Node([i-1,j-1]) for j in range(1,int(WIDTH/SIZE)-1)] for i in range(1,int(HEIGHT/SIZE)-1)]

#Returns the neighbouring points 
def getNeighbours(node):
    a,b = node.pos
    neighbours = []
    for i in range(-1,2):
        for j in range(-1,2):
            if i == 0 and j == 0:
                continue
            if i == j:
                continue
            x, y = a + i, b + j
            if x >= 0 and x < len(grid) and y >= 0 and y < len(grid):
                neighbours.append(grid[x][y])
    return neighbours

def getDistance(start, end):
    return abs(start.pos[0]-end.pos[0]) + abs(start.pos[1]-end.pos[1])

def tracePath(start, end):
    path = []
    cNode = end
    while cNode != start:
        path.append(cNode)
        cNode = cNode.parent
        if cNode != start:
            x,y = cNode.pos
            canvas.mark((x+1)*SIZE+int(SIZE/2),(y+1)*SIZE+int(SIZE/2),AQUA)
    return path.reverse()

def popup():
    popup = Tk()
    popup.geometry("200x75")
    popup.title("Oops!")
    label = Label(popup, text="Path not found!")
    button = Button(popup, text="Close", command = popup.destroy)
    label.pack(pady=10)
    button.pack()
    popup.mainloop()

#Start path finding with A* Algorithm
def startPF():
    openSet = []
    closedSet = []
    sNode = grid[start[0]][start[1]]
    tNode = grid[target[0]][target[1]]
    openSet.append(sNode)
    while len(openSet) > 0:
        cNode = openSet[0]

        for i in range(len(openSet)):
            if openSet[i].f() < cNode.f() or openSet[i].f() == cNode.f() and openSet[i].h < cNode.h:
                cNode = openSet[i]

        openSet.remove(cNode)
        closedSet.append(cNode)
        if cNode != sNode and cNode != tNode:
            canvas.mark((cNode.pos[0]+1)*SIZE+int(SIZE/2),(cNode.pos[1]+1)*SIZE+int(SIZE/2),GREEN)

        if cNode == tNode:
            tracePath(sNode,tNode)
            return

        for n in getNeighbours(cNode):
            if n.pos in obstacle or n in closedSet:
                continue
            g = cNode.g + getDistance(cNode, n)
            if g < n.g or n not in openSet:
                n.g = g
                n.h = getDistance(n, tNode)
                n.parent = cNode

                if n not in openSet:
                    openSet.append(n)
                    if n != tNode and n != sNode:
                        canvas.mark((n.pos[0]+1)*SIZE+int(SIZE/2),(n.pos[1]+1)*SIZE+int(SIZE/2),GREEN)

    popup()

        
canvas = mCanvas(root, WIDTH, HEIGHT, SIZE)
start_btn = Button(root,text="Start", command=startPF)
info = Label(text="*Set starting position*", foreground=BLUE)


start_btn.pack()
info.pack()
canvas.pack()
root.mainloop()
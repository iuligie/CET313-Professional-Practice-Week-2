import tkinter as tk


Width =30
triangle_size = 0.1
(x,y)=(20,16)
player = (0, 7)
actions = ["up", "down", "left", "right"]
#board=tk.Canvas(master, width=x*Width, height=y*Width)
border=[]
walls = [
(1,15),
(2, 2),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8),(2,10),(2,12),(2,13),(2,15),(2,17),(2,18),
(3, 2),(3,6),(3,10),(3,13),
(4,2),(4,4),(4,6),(4,8),(4,9),(4,10),(4,11),(4,12),(4,13),(4,14),(4,15),(4,16),(4,17),
(5,4),(5,6),(5,17),
(6,1),(6,2),(6,3),(6,4),(6,6),(6,7),(6,8),(6,9),(6,10),(6,11),(6,12),(6,13),(6,14),(6,15),(6,17),
(7,2),(7,10),(7,17),
(8,2),(8,3),(8,4),(8,5),(8,6),(8,7),(8,8),(8,10),(8,11),(8,13),(8,15),(8,16),(8,17),
(9,2),(9,8),(9,10),(9,11),(9,12),(9,13),(9,15),(9,17),
(10,4),(10,5),(10,6),(10,8),(10,13),(10,15),
(11,1),(11,2),(11,3),(11,4),(11,6),(11,8),(11,9),(11,10),(11,11),(11,12),(11,13),(11,15),(11,6),(11,17),
(12,6),(12,11),(12,17),
(13,2),(13,3),(13,4),(13,5),(13,6),(13,7),(13,8),(13,11),(13,12),(13,13),(13,14),(13,15),(13,17),
(14,17),
(15,1),(15,2),(15,3),(15,4),(15,5),(15,6),(15,7),(15,8),(15,9),(15,10),(15,11),(15,12),(15,13),(15,14),(15,15),(15,16),(15,17),(15,18)
]
specials = [(16, 3, "red", -1), (0, 7, "yellow", 1),(13, 19, "yellow", 1),(19, 13, "green", 1)]
cell_scores = {}
start=[]

class Game(tk.Tk):
    
    def __init__(self):
        tk.Tk.__init__(self)
        self.can = tk.Canvas(self, width=x*Width, height=y*Width)
        self.can.pack(fill="both", expand=True)
        self.render_grid()
        self.player = self.can.create_rectangle(player[0]*Width+Width*2/10, player[1]*Width+Width*2/10,
                            player[0]*Width+Width*8/10, player[1]*Width+Width*8/10, fill="red", width=1)
        self.x=0
        self.y=7
        self.bind("<Key>", self.move_player)
        

    def render_grid(self):
        global specials, walls, Width, x, y, player
        for i in range(x):
            for j in range(y):
                self.can.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="white", width=1)
                if((i==0  or j == 0) or i==19):
                        walls.append((i,j))
                        self.can.create_rectangle(i * Width, j * Width, (i + 1) * Width, (j + 1) * Width, fill="black", width=1)
        for (j, i) in walls:
            self.can.create_rectangle(i * Width, j * Width, (i + 1) * Width, (j + 1) * Width, fill="black", width=1)
        for (i, j, c, w) in specials:
            self.can.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill=c, width=1)

    def move_player(self, event):
        key = event.keysym
        if key == "Left":
            self.x= self.x - 1
            print("(To The Left)is valid? -> " + str(self.isValidMove()))
            if(self.isValidMove()):
                self.can.move(self.player, -30, 0)    
                print((self.x,self.y))
            else: self.x=self.x + 1       
        elif key == "Right":
            self.x= self.x + 1
            print("(To The Right)is valid? -> " + str(self.isValidMove()))
            if(self.isValidMove()):
                self.can.move(self.player, 30, 0)    
                print((self.x,self.y))
            else: self.x=self.x-1  
        elif key == "Up":
            self.y= self.y - 1
            print("(To The Sky)is valid? -> " + str(self.isValidMove()))
            if(self.isValidMove()):
                self.can.move(self.player, 0, -30)    
                print((self.x,self.y))
            else: self.y=self.y + 1      
        elif key == "Down":
            self.y= self.y + 1
            print("(To The Floor)is valid? -> " + str(self.isValidMove()))
            if(self.isValidMove()):
                self.can.move(self.player, 0, 30)    
                print((self.x,self.y))
            else: self.y=self.y-1  
    
    def isValidMove(self):
        if (self.y, self.x) in walls:
            print(self.x,self.y)
            return False
        print(self.x,self.y)
        return True


if __name__ == '__main__':
    game = Game()
    game.mainloop()
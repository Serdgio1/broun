import tkinter
from tkinter import *
from random import  randint

lis = []

W, H = 600 ,500
tk = Tk()
canvas = Canvas(tk, width=W,height=H)
canvas.pack()
value = tkinter.IntVar()
horizontal = Scale(tk, length=W/2*1.5  ,from_=0,to=100,orient=HORIZONTAL,command=lambda val: print(value.get()),variable=value)
horizontal.pack()

class Ball:
    def __init__(self, size, color, speedx, speedy):
        n = randint(0,W-size)

        if n and n-size and n+size not in lis:
            self.ball = canvas.create_oval(n,n,n+size,n+size,fill=color)
            lis.append(n)
        self.speedx = speedx
        self.speedy = speedy
        self.movement()

    def check(self):
        if self.speedx > 0:
            self.speedx = 0
            self.speedx += value.get()
        else:
            self.speedx = 0
            self.speedx -= value.get()

        if self.speedy > 0:
            self.speedy = 0
            self.speedy += value.get()
        else:
            self.speedy = 0
            self.speedy -= value.get()


    def all_move(self, pos):
        if pos[2] >= W or pos[0] <= 0:
            self.speedx *= -1

        if pos[3] >= H or pos[1] <= 0:
            self.speedy *= -1

        if pos[0] >= W or pos[1] >= H:
            pos[0] = randint(0,W-40)

    def not_move(self,pos):

        if pos[2] >= pos[2] + 40 or pos[0] <= pos[0] -40:
            self.speedx *= -1

        if pos[3] >= pos[3] + 40 or pos[1] <= pos[1] - 40:
            self.speedy *= -1


    def movement(self):
        canvas.move(self.ball,self.speedx,self.speedy)
        pos = canvas.coords(self.ball)

        #if value.get() >= 50:
        self.all_move(pos)
       #else:
        #    self.not_move(pos)
        self.check()


        tk.after(40,self.movement)




ball = Ball(40, 'green',0,0)
ball1 = Ball(40, 'yellow',0,0)
ball2 = Ball(40, 'yellow',0,0)
tk.mainloop()

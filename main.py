import tkinter
from tkinter import *
from random import  *

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
        y = randint(0,H-size)

        self.create = [True, True, True, True, True]
        self.pos_s = []
        self.speedx = speedx
        self.speedy = speedy
        self.size = size
        self.color = color
        self.create_ball()

        self.movement()

    def create_ball(self):
        while True:
            n = randint(0, W - self.size)
            y = randint(0, H - self.size)
            self.ball = canvas.create_oval(n, y, n + self.size, y + self.size, fill=self.color)
            if not self.check_overlap():
                break
            canvas.delete(self.ball)

    def check_overlap(self):
        x1, y1, x2, y2 = canvas.coords(self.ball)
        for item in canvas.find_overlapping(x1, y1, x2, y2):
            if item != self.ball:
                return True
        return False

    def check(self):
        if self.speedx > 0:
            self.speedx = 0
            self.speedx += randint(value.get()-2,value.get()+2)
        else:
            self.speedx = 0
            self.speedx -= randint(value.get()-2,value.get()+2)

        if self.speedy > 0:
            self.speedy = 0
            self.speedy += randint(value.get()-2,value.get()+2)
        else:
            self.speedy = 0
            self.speedy -= randint(value.get()-2,value.get()+2)


    def all_move(self, pos):
        if pos[2] >= W or pos[0] <= 0:
            self.speedx *= -1

        if pos[3] >= H or pos[1] <= 0:
            self.speedy *= -1

        if pos[0] >= W or pos[1] >= H:
            pos[0] = randint(0,W-40)

    def not_move(self,pos_s, pos):

        if pos[2] >= pos_s[2] or pos[0] <= pos_s[0] or pos[2] >= W or pos[0] <= 0:
            self.speedx *= -1

        if pos[3] >= pos_s[3] or pos[1] <= pos_s[1] or pos[3] >= H or pos[1] <= 0:
            self.speedy *= -1


    def movement(self):
        canvas.move(self.ball,self.speedx,self.speedy)
        pos = canvas.coords(self.ball)


        if value.get() >= 50:
            for i in range(len(self.create)):
                self.create[i] = True
            self.all_move(pos)
            self.check()
            canvas.delete('square0','square1', 'square2', 'square3', 'square4')

        elif value.get() >= 40:

            canvas.delete('square0', 'square1', 'square2', 'square3')
            self.create[3] = True
            if self.create[4]:

                square = canvas.create_rectangle(pos[0]-200, pos[1]-200, pos[2]+200, pos[3]+200,outline='',tags='square4')
                self.pos_s = canvas.coords(square)
                self.create[4] = False
            self.not_move(self.pos_s, pos)
            self.check()

        elif value.get() >= 30:
            canvas.delete('square0', 'square1', 'square2', 'square4')
            self.create[4] = True
            self.create[2] = True
            if self.create[3]:
                square = canvas.create_rectangle(pos[0]-90,pos[1]-90,pos[2]+90,pos[3]+90,outline='', tags='square3')
                self.pos_s = canvas.coords(square)
                self.create[3] = False
            self.not_move(self.pos_s, pos)
            self.check()

        elif value.get() >= 20:
            canvas.delete('square0', 'square1', 'square3', 'square4')
            self.create[3] = True
            self.create[1] = True
            if self.create[2]:
                canvas.config(borderwidth=0)
                square = canvas.create_rectangle(pos[0]-50,pos[1]-50,pos[2]+50,pos[3]+50, outline='',tags='square2')
                self.pos_s = canvas.coords(square)
                self.create[2] = False
            self.not_move(self.pos_s, pos)
            self.check()

        elif value.get() >= 10:
            canvas.delete('square0', 'square2', 'square3', 'square4')
            self.create[2] = True
            self.create[0] = True
            if self.create[1]:
                canvas.config(borderwidth=0)
                square = canvas.create_rectangle(pos[0]-20,pos[1]-20,pos[2]+20,pos[3]+20, outline='',tags='square1')
                self.pos_s = canvas.coords(square)
                self.create[1] = False
            self.not_move(self.pos_s, pos)
            self.check()

        elif value.get() > 0:
            canvas.delete('square1', 'square2', 'square3', 'square4')
            self.create[1] = True
            if self.create[0]:
                canvas.config(borderwidth=0)
                square = canvas.create_rectangle(pos[0]-1,pos[1]-1,pos[2]+1,pos[3]+1, outline='',tags='square0')
                self.pos_s = canvas.coords(square)
                self.create[0] = False
            self.not_move(self.pos_s, pos)
            self.check()
        else:
            self.speedx = 0
            self.speedy = 0

        tk.after(40,self.movement)


objs = list()
for i in range(38):
    objs.append(Ball(40, 'yellow', 0, 0))





tk.mainloop()
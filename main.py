import tkinter
from tkinter import *

W, H = 600 ,500
tk = Tk()
canvas = Canvas(tk, width=W,height=H)
canvas.pack()
value = tkinter.IntVar()
horizontal = Scale(tk, length=W/2*1.5  ,from_=0,to=200,orient=HORIZONTAL,command=lambda val: print(value.get()),variable=value)
horizontal.pack()

class Ball:
    def __init__(self, size, color, speedx, speedy):
        self.ball = canvas.create_oval(0,0,size,size,fill=color)
        self.speedx = speedx
        self.speedy = speedy
        self.movement()

    def movement(self):
        canvas.move(self.ball,self.speedx,self.speedy)
        pos = canvas.coords(self.ball)
        if pos[2] >= W or pos[0] <= 0:
            print(self.speedx)
            self.speedx = -1 * value.get()

        if pos[3] >= H or pos[1] < 0:
            self.speedy = -1 * value.get()

        tk.after(40,self.movement)




ball = Ball(40, 'green',value.get(),value.get())
tk.mainloop()

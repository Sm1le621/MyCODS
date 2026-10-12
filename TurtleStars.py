import turtle 
import random
import time

woun = turtle.Screen()
woun.setup(700, 900)
turtle.bgcolor("#055350")

p = turtle.Pen()

def paint(n):
    if n % 2 != 0:
            p.begin_fill()
            for x in range(n):
                p.forward(200)
                p.left(n // 2 * 360/n)
            p.end_fill()
for i in range(5, 12):
    p.penup()
    x = random.randint(-420, 420)
    y = random.randint(-320, 320)
    p.setpos(x, y)
    p.speed(10)
    p.color("yellow")
    p.pendown()
    paint(i)

    time.sleep(2)

woun.mainloop()

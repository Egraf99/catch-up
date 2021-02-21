from tkinter import *
from random import randint, uniform, choice
from math import *

# size window and circles
WIDTH_WINDOW = 800
HEIGHT_WINDOW = 800
BALL_SIZE = 10

# size and speed dino
WIDTH_DINO = 20
HEIGHT_DINO = 80
SPEED_X_DINO = 10
SPEED_Y_DINO = 5

# root after, ms
ROOT = 30

# list of create balls and available colours
balls = []
COLOURS = ('black', 'white', 'green', 'yellow', 'red', 'blue', 'purple')


class App:
    def __init__(self):
        global root, c, line

        # made window
        root = Tk()
        root.title('Дино-игра')
        c = Canvas(root, width=WIDTH_WINDOW, height=HEIGHT_WINDOW)
        c.grid()
        c.focus_set()

        # the line below which the ball cannot be placed
        line = c.create_line(0, HEIGHT_WINDOW / 10, WIDTH_WINDOW, HEIGHT_WINDOW / 10, dash=(4, 2))

        # player\dino
        dino = Dino()

        # processing events
        c.bind('<Button-1>', make_ball)
        c.bind('<KeyPress>', dino.move)

        root.mainloop()


class Circle:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

        self.item = c.create_oval(x - BALL_SIZE * self.size, y - BALL_SIZE * self.size,
                                  x + BALL_SIZE * self.size, y + BALL_SIZE * self.size,
                                  fill=choice(COLOURS))

        self.movement = False
        self.speed = 0
        self.aff = uniform(0.5, 1)  # acceleration of free fall
        self.elasticity = randint(1, 4)

    def move(self):
        """ check coords ball and move him"""
        # check coord ball
        if c.coords(self.item)[3] > HEIGHT_WINDOW:
            c.coords(self.item, self.x - BALL_SIZE, HEIGHT_WINDOW - BALL_SIZE * 2, self.x + BALL_SIZE, HEIGHT_WINDOW)
            self.speed = -self.speed + self.speed/self.elasticity

        # change speed ball and move ball
        if c.coords(self.item)[3] > HEIGHT_WINDOW - 5 and fabs(self.speed) < 2:
            c.coords(self.item, self.x - BALL_SIZE, HEIGHT_WINDOW - BALL_SIZE * 2, self.x + BALL_SIZE, HEIGHT_WINDOW)
            self.speed = 0
            self.movement = False
            root.after(5000, self.delete)
        else:
            self.speed += self.aff

        c.move(self.item, 0, self.speed)

        if self.movement:
            root.after(ROOT, self.move)

    def delete(self):
        c.delete(self.item)


def make_ball(event):
    """checking mouse coord, made and move ball"""
    if event.y < c.coords(line)[3]:
        ball = Circle(event.x, event.y, 1)
        ball.movement = True
        ball.move()
        balls.append(ball)


class Dino:
    def __init__(self):
        self.item = c.create_rectangle(WIDTH_WINDOW/2 - WIDTH_DINO/2, HEIGHT_WINDOW - HEIGHT_DINO,
                                       WIDTH_WINDOW/2 + WIDTH_DINO/2, HEIGHT_WINDOW,
                                       fill="gray")
        self.speed_x = 0
        self.speed_y = 0

    def move(self, event=None):
        """ move dino"""
        if event:
            key = event.keysym
        else:
            key = None

        if key == "Left" and c.coords(self.item)[0] > 0:
            self.speed_x = -SPEED_X_DINO
        elif key == "Right" and c.coords(self.item)[2] < WIDTH_WINDOW:
            self.speed_x = SPEED_X_DINO

        if not key:
            self.speed_x = 0

        c.move(self.item, self.speed_x, self.speed_y)

        root.after(ROOT, self.move)


if __name__ == '__main__':
    App()

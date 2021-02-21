from tkinter import *
from random import randint, uniform, choice
from math import *

# size window and circles
WIDTH = 800
HEIGHT = 800
BALL_SIZE = 10

# list of create balls and available colours
balls = []
COLOURS = ('black', 'white', 'green', 'yellow', 'red', 'blue', 'purple')


class App:
    def __init__(self):
        global root, c, line

        # made window
        root = Tk()
        root.title('Дино-игра')
        c = Canvas(root, width=WIDTH, height=HEIGHT)
        c.grid()
        c.focus_set()

        # the line below which the ball cannot be placed
        line = c.create_line(0, HEIGHT / 10, WIDTH, HEIGHT / 10, dash=(4, 2))

        # processing mouse events
        c.bind('<Button-1>', make_ball)

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
        # check coord ball
        if c.coords(self.item)[3] > HEIGHT:
            c.coords(self.item, self.x - BALL_SIZE, HEIGHT - BALL_SIZE * 2, self.x + BALL_SIZE, HEIGHT)
            self.speed = -self.speed + self.speed/self.elasticity

        # change speed ball and move ball
        if c.coords(self.item)[3] > HEIGHT - 5 and fabs(self.speed) < 2:
            c.coords(self.item, self.x - BALL_SIZE, HEIGHT - BALL_SIZE * 2, self.x + BALL_SIZE, HEIGHT)
            self.speed = 0
            self.movement = False
            root.after(5000, self.delete)
        else:
            self.speed += self.aff

        c.move(self.item, 0, self.speed)

        if self.movement:
            root.after(30, self.move)

    def delete(self):
        c.delete(self.item)


def make_ball(event):
    # checking mouse coord, made and move ball
    if event.y < c.coords(line)[3]:
        ball = Circle(event.x, event.y, 1)
        ball.movement = True
        ball.move()
        balls.append(ball)


# def start_balls(event):
#     # start all balls in the window
#     for b in balls:
#         if not b.movement:
#             b.movement = True
#             b.move()


if __name__ == '__main__':
    App()

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
SPEED_Y_DINO = 20

# root after, ms
ROOT = 30

# list of create balls
balls = []
balls_quantity = []
max_ball = 3


class App:
    def __init__(self):
        global root, c, line, WIDTH_WINDOW, HEIGHT_WINDOW

        # made window
        root = Tk()
        root.title('Дино-игра')
        WIDTH_WINDOW = root.winfo_screenwidth()
        HEIGHT_WINDOW = root.winfo_screenheight()
        root.attributes('-fullscreen', True)
        c = Canvas(root, width=WIDTH_WINDOW, height=HEIGHT_WINDOW)
        c.place(x=0, y=0)
        c.focus_set()

        # the line below which the ball cannot be placed
        line = c.create_line(0, HEIGHT_WINDOW / 10, WIDTH_WINDOW, HEIGHT_WINDOW / 10, dash=(4, 2))

        # player\dino
        dino = Dino()

        # processing events
        c.bind('<Button-1>', make_ball)
        c.bind('<KeyPress>', dino.start_move)
        c.bind('<KeyRelease>', dino.stop_move)
        root.bind('<Key>', close_window)

        root.mainloop()


class Circle:
    id_ball = 0

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

        self.item = c.create_oval(x - BALL_SIZE * self.size, y - BALL_SIZE * self.size,
                                  x + BALL_SIZE * self.size, y + BALL_SIZE * self.size,
                                  fill=random_color())

        self.movement = False
        self.speed = 0
        self.aff = uniform(0.5, 1)  # acceleration of free fall
        self.elasticity = uniform(1, 4)

        self.id = self.id_ball
        balls_quantity.append(self.id)
        Circle.id_ball += 1

    def move(self):
        # check coord ball
        if c.coords(self.item)[3] > HEIGHT_WINDOW:
            c.coords(self.item, self.x - BALL_SIZE, HEIGHT_WINDOW - BALL_SIZE * 2, self.x + BALL_SIZE, HEIGHT_WINDOW)
            self.speed = -self.speed + self.speed / self.elasticity

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
        balls_quantity.remove(self.id)


class Dino:
    def __init__(self):
        self.item = c.create_rectangle(WIDTH_WINDOW / 2 - WIDTH_DINO / 2, HEIGHT_WINDOW - HEIGHT_DINO,
                                       WIDTH_WINDOW / 2 + WIDTH_DINO / 2, HEIGHT_WINDOW,
                                       fill="orange")
        self.speed_x = 0
        self.speed_y = 0

        self.movement = False
        self.jumping = False
        self.move()
        self.collision()

    def start_move(self, event):
        # sets the speed
        key = None
        if event:
            key = event.keysym

        if key == "Up" and not self.jumping:
            self.jumping = True
            self.speed_y = -SPEED_Y_DINO
            self.jump()
        if key == "Left":
            self.speed_x = -SPEED_X_DINO
        elif key == "Right":
            self.speed_x = SPEED_X_DINO

    def stop_move(self, event):
        # speed = 0
        if event.keysym in ['Left', 'Right']:
            self.speed_x = 0

    def jump(self):
        if self.jumping:
            self.speed_y += SPEED_Y_DINO/10

        if c.coords(self.item)[3] > HEIGHT_WINDOW:
            x_left, x_right = c.coords(self.item)[0], c.coords(self.item)[2]
            c.coords(self.item, x_left, HEIGHT_WINDOW - HEIGHT_DINO, x_right, HEIGHT_WINDOW)
            self.jumping = False
            self.speed_y = 0

        if self.jumping:
            root.after(ROOT, self.jump)

    def move(self):
        # move dino
        y_up, y_down = c.coords(self.item)[1], c.coords(self.item)[3]

        if c.coords(self.item)[0] < 0:
            c.coords(self.item, 0, y_up, WIDTH_DINO, y_down)
        if c.coords(self.item)[2] > WIDTH_WINDOW:
            c.coords(self.item, WIDTH_WINDOW - WIDTH_DINO, y_up, WIDTH_WINDOW, y_down)

        c.move(self.item, self.speed_x, self.speed_y)

        root.after(ROOT, self.move)

    def collision(self):
        for ball in balls:
            if ball.movement:
                if \
                        (c.coords(ball.item)[0] <= c.coords(self.item)[0] <= c.coords(ball.item)[2] or
                         c.coords(ball.item)[0] <= c.coords(self.item)[2] <= c.coords(ball.item)[2]) and \
                        (c.coords(ball.item)[1] <= c.coords(self.item)[1] <= c.coords(ball.item)[3] or
                         c.coords(ball.item)[1] <= c.coords(self.item)[3] <= c.coords(ball.item)[3]):
                    c.create_text(WIDTH_WINDOW / 2, HEIGHT_WINDOW / 2, anchor=CENTER,
                                  font='Times 30', text='Игра окончена!')

        root.after(1, self.collision)


def make_ball(event):
    # checking mouse coord, made and move ball
    if event.y < c.coords(line)[3] and len(balls_quantity) < max_ball:
        ball = Circle(event.x, event.y, 1)
        ball.movement = True
        ball.move()
        balls.append(ball)


def random_color():
    # generate random HEX color. Example: #AA11FF
    color = '#'
    colors = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    for i in range(6):
        color += f'{choice(colors)}'
    return color


def close_window(event):
    if event.keysym == 'Escape':
        root.destroy()


if __name__ == '__main__':
    App()

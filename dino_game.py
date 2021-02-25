from tkinter import *
from random import uniform, choice
from math import *

# root after, ms
ROOT = 30


def set_size_window(*args, fullscreen=False):
    global WINDOW_WIDTH, WINDOW_HEIGHT, DIN0_WIDTH, DIN0_HEIGHT, DIN0_SPEED_X, DIN0_SPEED_Y, BALL_SIZE

    # set size window
    if len(args) == 2:
        win_w, win_h = args
        WINDOW_WIDTH = win_w
        WINDOW_HEIGHT = win_h
        root.geometry(f'{win_w}x{win_h}')
    elif fullscreen:
        WINDOW_WIDTH = root.winfo_screenwidth()
        WINDOW_HEIGHT = root.winfo_screenheight()
        root.attributes('-fullscreen', True)
    else:
        raise IndexError

    # set specifications dino and balls
    DIN0_WIDTH = WINDOW_WIDTH / 40
    DIN0_HEIGHT = WINDOW_HEIGHT / 10

    DIN0_SPEED_X = WINDOW_WIDTH / 80
    DIN0_SPEED_Y = WINDOW_HEIGHT / 20

    BALL_SIZE = WINDOW_WIDTH / 100


class App:
    def __init__(self):
        global root, dino, c, playing, line, WINDOW_WIDTH, WINDOW_HEIGHT

        playing = True

        # the line below which the ball cannot be placed
        line = c.create_line(0, WINDOW_HEIGHT / 10, WINDOW_WIDTH, WINDOW_HEIGHT / 10, dash=(4, 2))

        # player\dino
        dino = Dino()

        # processing events
        c.bind('<Button-1>', make_ball)
        c.bind('<KeyPress>', dino.start_move)
        c.bind('<KeyRelease>', dino.stop_move)
        root.bind('<Key>', handling_keyboard_events)

        root.mainloop()


class Circle:
    # list of create balls
    id_ball = 0
    balls = []
    balls_quantity = []
    max_ball = 20

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

        self.item = c.create_oval(x - BALL_SIZE * self.size, y - BALL_SIZE * self.size,
                                  x + BALL_SIZE * self.size, y + BALL_SIZE * self.size,
                                  fill=random_color())

        self.movement = False
        self.speed_x = 0
        self.speed_y = 0
        self.aff = uniform(0.5, 1)  # acceleration of free fall
        self.elasticity = uniform(1, 4)

        self.id = self.id_ball
        self.balls_quantity.append(self.id)
        Circle.id_ball += 1

    def move(self):
        if playing:
            try:
                # check coord ball
                if c.coords(self.item)[3] > WINDOW_HEIGHT:
                    c.coords(self.item, self.x - BALL_SIZE, WINDOW_HEIGHT - BALL_SIZE * 2, self.x + BALL_SIZE,
                             WINDOW_HEIGHT)
                    self.speed_y = -self.speed_y + self.speed_y / self.elasticity

                # change speed ball and move ball
                if c.coords(self.item)[3] > WINDOW_HEIGHT - 5 and fabs(self.speed_y) < 2:
                    c.coords(self.item, self.x - BALL_SIZE, WINDOW_HEIGHT - BALL_SIZE * 2, self.x + BALL_SIZE,
                             WINDOW_HEIGHT)
                    self.speed_y = 0
                    self.movement = False
                    root.after(5000, self.delete)
                else:
                    self.speed_y += self.aff

                c.move(self.item, 0, self.speed_y)

                if self.movement:
                    root.after(ROOT, self.move)
            except TclError: pass
            except IndexError: pass

    def delete(self):
        try:
            c.delete(self.item)
            self.balls_quantity.remove(self.id)
        except ValueError:
            pass

    def change_speed(self, x, y):
        self.speed_x = x
        self.speed_y = y


class Dino:
    def __init__(self):
        self.item = c.create_rectangle(WINDOW_WIDTH / 2 - DIN0_WIDTH / 2, WINDOW_HEIGHT - DIN0_HEIGHT,
                                       WINDOW_WIDTH / 2 + DIN0_WIDTH / 2, WINDOW_HEIGHT,
                                       fill="orange")

        self.speed_x = 0
        self.speed_y = 0

        self.movement = False
        self.jumping = False
        self.move()
        self.collision()

    def start_move(self, event):
        if playing:
            # check event and move dino in the specified direction
            key = None
            if event:
                key = event.keysym

            if key == "Up" and not self.jumping:
                self.jumping = True
                self.speed_y = -DIN0_SPEED_Y
                self.jump()
            if key == "Left":
                self.speed_x = -DIN0_SPEED_X
            elif key == "Right":
                self.speed_x = DIN0_SPEED_X

    def stop_move(self, event):
        if playing:
            # speed = 0
            if event.keysym in ['Left', 'Right']:
                self.speed_x = 0

    def speed(self, x, y):
        self.speed_x = x
        self.speed_y = y

    def jump(self):
        if playing:
            if self.jumping:
                self.speed_y += DIN0_SPEED_Y / 10

            if c.coords(self.item)[3] > WINDOW_HEIGHT:
                x_left, x_right = c.coords(self.item)[0], c.coords(self.item)[2]
                c.coords(self.item, x_left, WINDOW_HEIGHT - DIN0_HEIGHT, x_right, WINDOW_HEIGHT)
                self.jumping = False
                self.speed_y = 0

            if self.jumping:
                root.after(ROOT, self.jump)

    def move(self):
        if playing:
            try:
                # move dino
                y_up, y_down = c.coords(self.item)[1], c.coords(self.item)[3]

                if c.coords(self.item)[0] < 0:
                    c.coords(self.item, 0, y_up, DIN0_WIDTH, y_down)
                if c.coords(self.item)[2] > WINDOW_WIDTH:
                    c.coords(self.item, WINDOW_WIDTH - DIN0_WIDTH, y_up, WINDOW_WIDTH, y_down)

                c.move(self.item, self.speed_x, self.speed_y)

                root.after(ROOT, self.move)
            except TclError: pass
            except IndexError: pass

    def collision(self):
        if playing:
            for ball in Circle.balls:
                if ball.movement:
                    try:
                        if \
                                (c.coords(ball.item)[0] <= c.coords(self.item)[0] <= c.coords(ball.item)[2] or
                                 c.coords(ball.item)[0] <= c.coords(self.item)[2] <= c.coords(ball.item)[2]) and \
                                        (c.coords(ball.item)[1] <= c.coords(self.item)[1] <= c.coords(ball.item)[3] or
                                         c.coords(ball.item)[1] <= c.coords(self.item)[3] <= c.coords(ball.item)[3]):
                            game_over()

                    except TclError:
                        pass
                    except IndexError:
                        pass

            root.after(1, self.collision)

    def delete(self):
        try:
            c.delete(self.item)
        except ValueError:
            pass


def make_ball(event):
    if playing:
        # checking mouse coord, made and move ball
        if event.y < c.coords(line)[3] and len(Circle.balls_quantity) < Circle.max_ball:
            ball = Circle(event.x, event.y, 1)
            ball.movement = True
            ball.move()
            Circle.balls.append(ball)


def random_color():
    # generate random HEX color. Example: #AA11FF
    color = '#'
    colors = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    for i in range(6):
        color += f'{choice(colors)}'
    return color


def handling_keyboard_events(event):
    # print(f'{event.keysym} и {event.type}') - for learn event
    if event.keysym == 'Escape':
        root.destroy()
    if event.keysym == 'space':
        retry()
        pass


def init_game():
    global c

    # set size objects
    set_size_window(fullscreen=True)

    # made window
    root.title('Дино-игра')
    c = Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    c.place(x=0, y=0)
    c.focus_set()


def game_over():
    global playing

    playing = False

    # speed all objects = 0
    dino.speed(0, 0)
    for ball in Circle.balls:
        ball.change_speed(0, 0)

    # text
    size_text = WINDOW_WIDTH // 25
    font_text = 'Times ' + str(size_text)

    c.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, anchor=CENTER,
                  font=font_text, text='Игра окончена!')

    # button of retry
    Button(root, bg='gray', text='Новая игра', font=font_text, command=retry, anchor=CENTER)\
        .place(x=WINDOW_WIDTH / 2, y=WINDOW_HEIGHT / 1.2)


def retry():
    global app

    # delete all objects
    list_destroy = root.place_slaves()
    for obj in list_destroy:
        obj.destroy()

    # start new game
    init_game()
    app = App()


if __name__ == '__main__':
    root = Tk()
    init_game()
    app = App()

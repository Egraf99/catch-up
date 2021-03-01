from tkinter import *
from random import uniform, choice
from math import *

# root after, ms
ROOT = 30


def init_game():
    global c

    # set size objects
    set_size_window(800, 800)

    # made window
    root.title('Дино-игра')
    c = Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    c.place(x=0, y=0)
    c.focus_set()


def set_size_window(*args, fullscreen=False):
    global full, WINDOW_WIDTH, WINDOW_HEIGHT, DIN0_WIDTH, DIN0_HEIGHT, DIN0_SPEED_X, DIN0_SPEED_Y, BALL_SIZE, FIGURE

    # set size window
    if len(args) == 2:
        win_w, win_h = args
        WINDOW_WIDTH = win_w
        WINDOW_HEIGHT = win_h
        root.geometry(f'{win_w}x{win_h}')
    elif fullscreen:
        full = True
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

    FIGURE = 'square'


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
    Button(root, bg='gray', text='Новая игра', font=font_text, command=retry) \
        .place(x=WINDOW_WIDTH / 3, y=WINDOW_HEIGHT / 5, width=WINDOW_WIDTH / 3)


def retry():
    global app

    # clear lists
    Circle.balls_quantity = []
    Circle.balls = []
    Circle.id_ball = 0

    Figure.figures = []

    # delete all objects
    list_destroy = root.place_slaves()
    for obj in list_destroy:
        obj.destroy()

    # start new game
    init_game()
    app = App()


class App:
    def __init__(self):
        global root, dino, c, playing, line, WINDOW_WIDTH, WINDOW_HEIGHT

        playing = True

        # the line below which the ball cannot be placed
        line = c.create_line(0, WINDOW_HEIGHT / 10, WINDOW_WIDTH, WINDOW_HEIGHT / 10, dash=(4, 2))

        # player\dino
        dino = Dino()

        # processing events
        c.bind('<ButtonPress-1>', make_ball)
        c.bind('<ButtonPress-3>', start_make_figure)
        c.bind('<B3-Motion>', show_figure)
        c.bind('<ButtonRelease-3>', make_figure)
        c.bind('<Shift-ButtonPress-1>', del_figure)
        c.bind('<KeyPress>', dino.start_move)
        c.bind('<KeyRelease>', dino.stop_move)

        root.bind('<Key>', handling_keyboard_events)

        root.mainloop()


class Figure:
    # list of figures
    figures = []
    figures_quantity = []
    id_figure = 0

    def __init__(self, figure='square'):
        self.item = None

        self.figure = figure

        self.speed_y = 0
        self.aff = 1.5

        self.id = self.id_figure
        self.figures_quantity.append(self.id)
        Figure.id_figure += 1

    def create(self, color=None):
        if playing:
            if color:
                col = color
            else:
                col = random_color()

            if self.figure == 'square':
                self.item = c.create_rectangle(self.x_left, self.y_up, self.x_right, self.y_down, fill=col)

            elif self.figure == 'triangle':
                middle_width = self.take_middle()
                self.item = c.create_polygon(self.x_left, self.y_down, middle_width, self.y_up,
                                             self.x_right, self.y_down, outline='black', fill=col)

    def move(self):
        if playing:
            self.speed_y += self.aff

            c.move(self.item, 0, self.speed_y)

            if self.figure == 'square':
                if c.coords(self.item)[3] < WINDOW_HEIGHT:
                    root.after(ROOT, self.move)
                else:
                    self.speed_y = 0
                    c.coords(self.item,
                             self.x_left, WINDOW_HEIGHT - (fabs(self.y_down - self.y_up)),
                             self.x_right, WINDOW_HEIGHT)

            elif self.figure == 'triangle':
                if c.coords(self.item)[1] < WINDOW_HEIGHT and c.coords(self.item)[3] < WINDOW_HEIGHT:
                    root.after(ROOT, self.move)
                else:
                    self.speed_y = 0
                    if self.y_down > self.y_up:
                        c.coords(self.item,
                                 self.x_left, WINDOW_HEIGHT, self.take_middle(),
                                 WINDOW_HEIGHT - self.take_height(),
                                 self.x_right, WINDOW_HEIGHT)
                    else:
                        c.coords(self.item,
                                 self.x_left, WINDOW_HEIGHT - self.take_height(),
                                 self.take_middle(), WINDOW_HEIGHT,
                                 self.x_right, WINDOW_HEIGHT - self.take_height())

    def take_middle(self):
        if self.x_right > self.x_left:
            middle_x = (self.x_right - self.x_left) / 2 + self.x_left
        else:
            middle_x = (self.x_left - self.x_right) / 2 + self.x_right

        return middle_x

    def take_height(self):
        return fabs(self.y_down - self.y_up)

    def delete(self):
        try:
            c.delete(self.item)
            self.figures_quantity.remove(self.id)
        except ValueError:
            pass


def start_make_figure(event):
    global fig, pressed
    pressed = True
    fig = Figure(FIGURE)
    fig.x_left, fig.y_up = event.x, event.y


def make_figure(event):
    global fig, pressed

    fig.delete()
    fig.x_right, fig.y_down = event.x, event.y
    fig.create(color=None)
    Figure.figures.append(fig)
    fig.move()
    pressed = False


def show_figure(event):
    global fig

    fig.delete()
    if pressed:
        fig.x_right, fig.y_down = event.x, event.y
        fig.create(color='white')


def del_figure(event):
    x, y = event.x, event.y
    items = c.find_overlapping(x, y, x, y)
    for item in filter(lambda i: i is not dino.item, items):
        for fig in Figure.figures:
            if fig.item is item:
                fig.delete()


class Circle:
    # list of create balls
    id_ball = 0
    balls = []
    balls_quantity = []
    max_ball = 30

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

        self.collision_dino()

    def move(self):
        if playing:
            try:
                # check ball collision figure
                if self.collision_fig() == 'stop':
                    self.speed_y = 0.1

                elif self.collision_fig() == 'bounce':
                    self.speed_y = -self.speed_y + self.speed_y / self.elasticity

                # check coord ball
                elif c.coords(self.item)[3] > WINDOW_HEIGHT:
                    c.coords(self.item, self.x - BALL_SIZE, WINDOW_HEIGHT - BALL_SIZE * 2, self.x + BALL_SIZE,
                             WINDOW_HEIGHT)
                    self.speed_y = -self.speed_y + self.speed_y / self.elasticity

                # change speed ball and move ball
                elif c.coords(self.item)[3] > WINDOW_HEIGHT - 5 and fabs(self.speed_y) < 2:
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

            except Exception:
                pass

    def collision_dino(self):
        if playing:
            if self.movement:
                try:
                    dino_x1, dino_y1, dino_x2, dino_y2 = c.coords(dino.item)
                    ball_x1, ball_y1, ball_x2, ball_y2 = c.coords(self.item)

                    if (dino_x1 <= ball_x1 <= dino_x2 or dino_x1 <= ball_x2 <= dino_x2) and \
                            (ball_y1 <= dino_y1 <= ball_y2 or ball_y1 <= dino_y2 <= ball_y2):
                        game_over()

                except Exception:
                    pass

            root.after(1, self.collision_dino)

    def collision_fig(self):
        try:
            ball_x1, ball_y1, ball_x2, ball_y2 = c.coords(self.item)

            for fig in Figure.figures:
                try:

                    if fig.figure == 'square':
                        fig_x1, fig_y1, fig_x2, fig_y2 = c.coords(fig.item)

                        if (fig_x1 <= ball_x1 <= fig_x2 or fig_x1 <= ball_x2 <= fig_x2) and ball_y2 >= fig_y1:
                            c.coords(self.item, ball_x1, fig_y1 - BALL_SIZE * 2, ball_x2, fig_y1)
                            return 'bounce'

                        elif (fig_x1 <= ball_x1 <= fig_x2 or fig_x1 <= ball_x2 <= fig_x2) and \
                                ball_y2 > fig_y1 - 5 and fabs(self.speed_y) < 2:
                            c.coords(self.item, ball_x1, fig_y1 - BALL_SIZE * 2, ball_x2, fig_y1)
                            return 'stop'

                    elif fig.figure == 'triangle':
                        fig_x1, fig._y1, fig_x2, fig_y2, fig_x3, fig_y3 = c.coords(fig.item)
                        pass

                except Exception:
                    continue

        except Exception:
            pass

    def delete(self):
        try:
            c.delete(self.item)
            self.balls_quantity.remove(self.id)
        except ValueError:
            pass

    def change_speed(self, x, y):
        self.speed_x = x
        self.speed_y = y


def make_ball(event):
    if playing:
        # checking mouse coord, made and move ball
        if event.y < c.coords(line)[3] and len(Circle.balls_quantity) < Circle.max_ball:
            ball = Circle(event.x, event.y, 1)
            ball.movement = True
            ball.move()
            Circle.balls.append(ball)


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
        self.collision_balls()

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

            except Exception:
                pass

    def collision_balls(self):
        if playing:
            for ball in Circle.balls:
                if ball.movement:
                    dino_x1, dino_y1, dino_x2, dino_y2 = c.coords(self.item)
                    ball_x1, ball_y1, ball_x2, ball_y2 = c.coords(ball.item)

                    try:
                        if (dino_x1 <= ball_x1 <= dino_x2 or dino_x1 <= ball_x2 <= dino_x2) and \
                                (ball_y1 <= dino_y1 <= ball_y2 or ball_y1 <= dino_y2 <= ball_y2):
                            game_over()

                    except Exception:
                        pass

            root.after(1, self.collision_balls)

    def delete(self):
        try:
            c.delete(self.item)
        except ValueError:
            pass


def random_color():
    # generate random HEX color. Example: #AA11FF
    color = '#'
    colors = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    for i in range(6):
        color += f'{choice(colors)}'
    return color


def handling_keyboard_events(event):
    global FIGURE
    #print(f'{event.keysym} и {event.char}') #- for learn event
    if event.keysym == 'Escape':
        root.destroy()
    if event.keysym == 'space':
        retry()
    if event.char == 'q' or event.char == 'й':
        if FIGURE == 'square':
            FIGURE = 'triangle'
            txt = c.create_text(0, WINDOW_HEIGHT, anchor=SW, font=f'Times {WINDOW_WIDTH // 50}',
                                text='Фигура: Треугольник')
            root.after(1000, lambda: c.delete(txt))
        elif FIGURE == 'triangle':
            FIGURE = 'square'
            txt = c.create_text(0, WINDOW_HEIGHT, anchor=SW, font=f'Times {WINDOW_WIDTH // 50}',
                                text='Фигура: Прямоугольник')
            root.after(1000, lambda: c.delete(txt))


if __name__ == '__main__':
    root = Tk()
    init_game()
    app = App()

from tkinter import *
from math import *

WIDTH = 800
HEIGHT = 800
CIRCLE_SIZE = 10
figures = []
max_figures = 25


class App:
    def __init__(self):
        global root, c, line
        root = Tk()
        root.title('пробы')
        c = Canvas(root, width=WIDTH, height=HEIGHT)
        c.grid()
        c.focus_set()
        c.bind('<Button-3>', find_coord)
        c.bind('<Button-1>', go_all)
        check_figure()
        root.mainloop()


class Circle:

    def __init__(self, x, y, size, speed_x, speed_y):
        self.size = size
        self.x_finish = self.y_finish = 0
        self.kx = speed_x
        self.ky = speed_y
        self.go = False
        self.health = True
        self.item = c.create_oval(x - CIRCLE_SIZE * self.size, y - CIRCLE_SIZE * self.size,
                                  x + CIRCLE_SIZE * self.size, y + CIRCLE_SIZE * self.size,
                                  fill='green')

    def _find_coefficient(self):
        x0, y0, x1, y1 = c.coords(self.item)
        x = (x0 + x1)/2
        y = (y0 + y1)/2
        abs_x = x - self.x_finish
        abs_y = y - self.y_finish
        hyp = sqrt(abs_x ** 2 + abs_y ** 2)

        if abs_x != 0:
            kx = hyp / abs_x
        else:
            kx = 0
        if abs_y != 0:
            ky = hyp / abs_y
        else:
            ky = 0

        if (abs_x < 0 and abs_y < 0) or (abs_x > 0 and abs_y > 0):
            kx = -kx
            ky = -ky
        return kx, ky

    def check_move(self, event):
        if not self.go:
            self.go = True
            self.move(event)

    def move(self, event=None):

        if event:
            self.x_finish, self.y_finish = event.x, event.y
            self.kx, self.ky, = self._find_coefficient()

        if c.coords(self.item)[3] > HEIGHT or c.coords(self.item)[1] < 0:
            self.kx = -self.kx
        if c.coords(self.item)[0] < 0 or c.coords(self.item)[2] > WIDTH:
            self.ky = -self.ky

        c.move(self.item, self.ky, self.kx)

        root.after(60, self.move)

    def change_size(self, x, y):
        self.size += 1
        self.item = c.create_oval(x - CIRCLE_SIZE * self.size, y - CIRCLE_SIZE * self.size,
                                  x + CIRCLE_SIZE * self.size, y + CIRCLE_SIZE * self.size,
                                  fill='green')


def find_coord(event):
    made_figure(event.x, event.y)


def made_figure(x, y, size=1, speed_x=None, speed_y=None):
    if len(figures) <= max_figures:
        figure = Circle(x, y, size, speed_x, speed_y)
        figures.append(figure)


def go_all(event):
    check_figure()
    for f in figures:
        f.move(event)


def check_figure():
    for f in figures:
        x0, y0, x1, y1 = c.coords(f.item)
        items = c.find_overlapping(x0, y0, x1, y1)
        for j in filter(lambda i: i is not f.item, items):
            print(items)
            c.delete(f.item)
            figures.remove(f)
            print(items)
            x0a, y0a, x1a, y1a = c.coords(figures[j-1].item)
            print([x0a, y0a, x1a, y1a])
            figures[j - 1].change_size((x1a + x0a)/2, (y1a + y0a)/2)
    root.after(1, check_figure)


if __name__ == '__main__':
    App()

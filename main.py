from tkinter import *
from math import *

WIDTH = 800
HEIGHT = 800
CIRCLE_SIZE = 10



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
        root.mainloop()


class Circle:
    figures = []
    max_figures = 25

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
        self.check_collision()

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

        try:
            if c.coords(self.item)[3] > HEIGHT or c.coords(self.item)[1] < 0:
                self.kx = -self.kx
            if c.coords(self.item)[0] < 0 or c.coords(self.item)[2] > WIDTH:
                self.ky = -self.ky

            c.move(self.item, self.ky, self.kx)
        except Exception:
            pass

        root.after(60, self.move)

    def change_size(self, x, y):
        self.size += 1
        c.delete(self.item)
        self.item = c.create_oval(x - CIRCLE_SIZE * self.size, y - CIRCLE_SIZE * self.size,
                                  x + CIRCLE_SIZE * self.size, y + CIRCLE_SIZE * self.size,
                                  fill='green')

    def delete(self):
        try:
            c.delete(self.item)
            self.figures.remove(self)
        except ValueError:
            pass

    def check_collision(self):
        try:
            x0, y0, x1, y1 = c.coords(self.item)
            items = c.find_overlapping(x0, y0, x1, y1)
            for item in filter(lambda i: i is not self.item, items):
                for fig in Circle.figures:
                    if fig.item == item:
                        fig.delete()
                        self.change_size(x0, y0)
            root.after(1, self.check_collision)
        except Exception:
            pass


def find_coord(event):
    made_figure(event.x, event.y)


def made_figure(x, y, size=1, speed_x=None, speed_y=None):
    if len(Circle.figures) <= Circle.max_figures:
        figure = Circle(x, y, size, speed_x, speed_y)
        Circle.figures.append(figure)


def go_all(event):
    for f in Circle.figures:
        f.move(event)


if __name__ == '__main__':
    App()

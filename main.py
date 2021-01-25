from tkinter import *
from math import *

WIDTH = 900
HEIGHT = 800
CIRCLE_SIZE = 10
figures = []


def main():
    global root, c, line
    root = Tk()
    root.title('пробы')
    c = Canvas(root, width=WIDTH, height=HEIGHT)
    c.grid()
    c.focus_set()
    c.bind('<Button-3>', made_figure)
    c.bind('<Button-1>', go_all)
    root.mainloop()


class Circle:

    def __init__(self, x, y):
        self.coord = c.create_oval(x - CIRCLE_SIZE, y - CIRCLE_SIZE, x + CIRCLE_SIZE, y + CIRCLE_SIZE, fill='green')
        self.x = x
        self.y = y
        self.x_finish = self.y_finish = 0
        self.kx = self.ky = None
        self.go = False

    def _find_coefficient(self):
        abs_x = self.x - self.x_finish
        abs_y = self.y - self.y_finish
        hyp = sqrt(abs_x ** 2 + abs_y ** 2)
        kx = hyp / abs_x
        ky = hyp / abs_y
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
            self.kx, self.ky = self._find_coefficient()

        if c.coords(self.coord)[3] > HEIGHT or c.coords(self.coord)[1] < 0:
            self.kx = -self.kx
        if c.coords(self.coord)[0] < 0 or c.coords(self.coord)[2] > WIDTH:
            self.ky = -self.ky

        self.x += self.kx
        self.y += self.ky
        c.move(self.coord, self.ky, self.kx)

        root.after(60, self.move)


def made_figure(event):
    figure = Circle(event.x, event.y)
    figures.append(figure)


def go_all(event):
    for f in figures:
        f.check_move(event)


if __name__ == '__main__':
    main()

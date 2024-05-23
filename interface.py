from tkinter import Tk, BOTH, Canvas
import time, random

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title = "Maze solver"
        self.__canvas = Canvas(self.__root, bg="white", width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__window_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def __str__(self):
        return f"{self.__root}, {self.__root.title}, {self.canvas}, {self.window_running}"

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__window_running = True
        while self.__window_running == True:
            self.redraw()

    def close(self):
        self.__window_running = False

    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x}, {self.y}"

class Line:
    def __init__(self, point_1, point_2):
        self.point_1 = point_1
        self.point_2 = point_2

    def __str__(self):
        return f"{self.point_1}, {self.point_2}"

    def draw(self, canvas, fill_color="black"):
        canvas.create_line(self.point_1.x, self.point_1.y, self.point_2.x, self.point_2.y, fill=fill_color, width=2)

class Cell:
    def __init__(self, window=None):
        self._win = window
        self._x1, self._y1 = None, None
        self._x2, self._y2 = None, None
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        if self.has_left_wall:
            self._win.draw_line(Line(Point(x1, y1), Point(x1, y2)))
        else:
            self._win.draw_line(Line(Point(x1, y1), Point(x1, y2)), "white")
        if self.has_top_wall:
            self._win.draw_line(Line(Point(x1, y1), Point(x2, y1)))
        else:
             self._win.draw_line(Line(Point(x1, y1), Point(x2, y1)), "white")
        if self.has_right_wall:
            self._win.draw_line(Line(Point(x2, y1), Point(x2, y2)))
        else:
            self._win.draw_line(Line(Point(x2, y1), Point(x2, y2)), "white")
        if self.has_bottom_wall:
            self._win.draw_line(Line(Point(x1, y2), Point(x2, y2)))
        else:
            self._win.draw_line(Line(Point(x1, y2), Point(x2, y2)), "white")

    def draw_move(self, to_cell, undo=False):
        if undo == False:
            self._win.draw_line(Line(Point((self._x1 + self._x2) / 2, (self._y1 +self._y2) / 2), Point((to_cell._x1 + to_cell._x2) / 2, (to_cell._y1 + to_cell._y2) / 2)), "red")
        else:
            self._win.draw_line(Line(Point((self._x1 + self._x2) / 2, (self._y1 +self._y2) / 2), Point((to_cell._x1 + to_cell._x2) / 2, (to_cell._y1 + to_cell._y2) / 2)), "gray")

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self._x1, self._y1 = x1, y1
        self.num_rows, self.num_cols = num_rows, num_cols
        self.cell_size_x, self.cell_size_y = cell_size_x, cell_size_y
        self.win = win
        if seed != None:
            self.seed = random.seed(seed)

        self._create_cells()

    def _create_cells(self):
        self._cells = []
        for column in range(self.num_cols):
            self._cells.append([])
            for row in range(self.num_rows):
                self._cells[column].append(Cell(self.win))

        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)
        self._break_entrance_and_exit()

    def _draw_cell(self, i, j):
        if self.win is None:
            return
        x = self._x1 + i * self.cell_size_x
        y = self._y1 + j * self.cell_size_y
        self._cells[i][j].draw(x, y, x + self.cell_size_x, y + self.cell_size_y)
        self._animate()


    def _animate(self):
        if self.win is None:
            return
        self.win.redraw()
        time.sleep(0.01)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall = False
        self._draw_cell(0, 0)
        self._draw_cell(self.num_cols - 1, self.num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            to_visit = []
            #check which adjacent cells are valid
            #left
            if i > 0 and self._cells[i - 1][j].visited == False:
                to_visit.append((i - 1, j))
            #right
            if i < self.num_cols - 1 and self._cells[i + 1][j].visited == False:
                to_visit.append((i + 1, j))
            #top
            if j > 0 and self._cells[i][j - 1].visited == False:
                to_visit.append((i, j -1))
            #bottom
            if j < self.num_rows - 1 and self._cells[i][j + 1].visited == False:
                to_visit.append((i, j + 1))
            if len(to_visit) > 0:
                next_cell = random.choice(to_visit)
                if next_cell[0] < i:
                    self._cells[i][j].has_left_wall = False
                    self._cells[next_cell[0]][next_cell[1]].has_right_wall = False
                elif next_cell[0] > i:
                    self._cells[i][j].has_right_wall = False
                    self._cells[next_cell[0]][next_cell[1]].has_left_wall = False
                elif next_cell[1] < j:
                    self._cells[i][j].has_top_wall = False
                    self._cells[next_cell[0]][next_cell[1]].has_bottom_wall = False
                elif next_cell[1] > j:
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[next_cell[0]][next_cell[1]].has_top_wall = False
                self._break_walls_r(next_cell[0], next_cell[1])
            else:
                self._draw_cell(i, j)
                time.sleep(0.01)
                return

    def _reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate
        self._cells[i][j].visited = True
        if self._cells[i][j] is self._cells[self.num_cols - 1][self.num_rows - 1]:
            return True
        #left
        if i > 0 and self._cells[i - 1][j].visited == False and self._cells[i][j].has_left_wall == False:
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            self._cells[i][j].draw_move(self._cells[i - 1][j], undo=True)
        #right
        if i < self.num_cols - 1 and self._cells[i + 1][j].visited == False and self._cells[i][j].has_right_wall == False:
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            self._cells[i][j].draw_move(self._cells[i + 1][j], undo=True)
        #top
        if j > 0 and self._cells[i][j - 1].visited == False and self._cells[i][j].has_top_wall == False:
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            self._cells[i][j].draw_move(self._cells[i][j - 1], undo=True)
        #bottom
        if j < self.num_rows - 1 and self._cells[i][j + 1].visited == False and self._cells[i][j].has_bottom_wall == False:
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            self._cells[i][j].draw_move(self._cells[i][j + 1], undo=True)
        return False

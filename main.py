from tkinter import *
import random
import os

root = Tk()
root.title("A* path finding")

# 2 main frames in gui
global grid_frame
global add_object_frame

grid_frame = LabelFrame(root)
grid_frame.grid(row=0, column=0)

start_button_state = 0
end_button_state = 0
wall_button_state = 0


class AStar:
    def __init__(self, start, end, walls):
        self.start = start
        self.end = end
        self.walls = walls

        self.g_cost = {}  # cost according to distance from starting point
        self.h_cost = {}  # cost according to distance from finish point
        self.f_cost = {}  # sum cost of g and h cost

        self.parent = {}

        self.final_path = []

        self.visited = []
        self.seen_not_visited = []
        self.new = []
        self.null = [str(x) + ',' + str(y) for x in range(board.column) for y in range(board.row) if
                     str(x) + ',' + str(y) != self.start and str(x) + ',' + str(y) not in self.walls]
        self.run(self.start)

    def run(self, coords):
        try:
            while coords != self.end:
                x_y = coords.split(",")
                x = int(x_y[0])
                y = int(x_y[1])
                self.new = []
                self.next_possible_moves(x, y)

                coords = self.next_move()

                board.color_green(self.new)
                board.color_red(coords)

                self.seen_not_visited.remove(coords)
                self.visited.append(coords)

            val = self.end
            self.final_path.append(self.end)
            while val in self.parent.keys():
                val = self.parent[val]
                self.final_path.append(val)
            board.color_blue(self.final_path)

        except:
            print("No path found.")
            root.quit()

    def next_possible_moves(self, x, y):
        parent_li = self.parent.keys()
        if str(x + 1) + ',' + str(y) not in self.walls and (
                str(x + 1) + ',' + str(y) in self.null or str(x + 1) + ',' + str(y) in self.seen_not_visited):
            temp_g = self.find_g(x + 1, y, x, y)
            temp_h = self.find_h(x + 1, y)
            temp_f = temp_g + temp_h
            if str(x + 1) + ',' + str(y) not in parent_li:
                self.parent[str(x + 1) + ',' + str(y)] = str(x) + "," + str(y)
                self.g_cost[str(x + 1) + "," + str(y)] = temp_g
                self.h_cost[str(x + 1) + "," + str(y)] = temp_h
                self.f_cost[str(x + 1) + "," + str(y)] = temp_f
                self.seen_not_visited.append(str(x + 1) + ',' + str(y))
                self.new.append(str(x + 1) + ',' + str(y))
                self.null.remove(str(x + 1) + ',' + str(y))
            elif str(x + 1) + ',' + str(y) in parent_li:
                if temp_g < self.g_cost[str(x + 1) + ',' + str(y)]:
                    self.g_cost[str(x + 1) + ',' + str(y)] = temp_g
                    self.parent[str(x + 1) + ',' + str(y)] = str(x) + "," + str(y)
                    self.h_cost[str(x + 1) + "," + str(y)] = temp_h
                    self.f_cost[str(x + 1) + "," + str(y)] = temp_f

        if str(x) + ',' + str(y + 1) not in self.walls and (
                str(x) + ',' + str(y + 1) in self.null or str(x) + ',' + str(y + 1) in self.seen_not_visited):
            temp_g = self.find_g(x, y + 1, x, y)
            temp_h = self.find_h(x, y + 1)
            temp_f = temp_g + temp_h
            if str(x) + ',' + str(y + 1) not in parent_li:
                self.parent[str(x) + ',' + str(y + 1)] = str(x) + "," + str(y)
                self.g_cost[str(x) + "," + str(y + 1)] = temp_g
                self.h_cost[str(x) + "," + str(y + 1)] = temp_h
                self.f_cost[str(x) + "," + str(y + 1)] = temp_f
                self.seen_not_visited.append(str(x) + ',' + str(y + 1))
                self.null.remove(str(x) + ',' + str(y + 1))
                self.new.append(str(x) + ',' + str(y + 1))
            elif str(x) + ',' + str(y + 1) in parent_li:
                if temp_g < self.g_cost[str(x) + ',' + str(y + 1)]:
                    self.g_cost[str(x) + ',' + str(y + 1)] = temp_g
                    self.parent[str(x) + ',' + str(y + 1)] = str(x) + "," + str(y)
                    self.h_cost[str(x) + "," + str(y + 1)] = temp_h
                    self.f_cost[str(x) + "," + str(y + 1)] = temp_f

        if str(x - 1) + ',' + str(y) not in self.walls and (
                str(x - 1) + ',' + str(y) in self.null or str(x - 1) + ',' + str(y) in self.seen_not_visited):
            temp_g = self.find_g(x - 1, y, x, y)
            temp_h = self.find_h(x - 1, y)
            temp_f = temp_g + temp_h
            if str(x - 1) + ',' + str(y) not in parent_li:
                self.parent[str(x - 1) + ',' + str(y)] = str(x) + "," + str(y)
                self.g_cost[str(x - 1) + "," + str(y)] = temp_g
                self.h_cost[str(x - 1) + "," + str(y)] = temp_h
                self.f_cost[str(x - 1) + "," + str(y)] = temp_f
                self.seen_not_visited.append(str(x - 1) + ',' + str(y))
                self.null.remove(str(x - 1) + ',' + str(y))
                self.new.append(str(x - 1) + ',' + str(y))
            elif str(x - 1) + ',' + str(y) in parent_li:
                if temp_g < self.g_cost[str(x - 1) + ',' + str(y)]:
                    self.g_cost[str(x - 1) + ',' + str(y)] = temp_g
                    self.parent[str(x - 1) + ',' + str(y)] = str(x) + "," + str(y)
                    self.h_cost[str(x - 1) + "," + str(y)] = temp_h
                    self.f_cost[str(x - 1) + "," + str(y)] = temp_f

        if str(x) + ',' + str(y - 1) not in self.walls and (
                str(x) + ',' + str(y - 1) in self.null or str(x) + ',' + str(y - 1) in self.seen_not_visited):
            temp_g = self.find_g(x, y - 1, x, y)
            temp_h = self.find_h(x, y - 1)
            temp_f = temp_g + temp_h
            if str(x) + ',' + str(y - 1) not in parent_li:
                self.parent[str(x) + ',' + str(y - 1)] = str(x) + "," + str(y)
                self.g_cost[str(x) + "," + str(y - 1)] = temp_g
                self.h_cost[str(x) + "," + str(y - 1)] = temp_h
                self.f_cost[str(x) + "," + str(y - 1)] = temp_f
                self.seen_not_visited.append(str(x) + ',' + str(y - 1))
                self.null.remove(str(x) + ',' + str(y - 1))
                self.new.append(str(x) + ',' + str(y - 1))
            elif str(x) + ',' + str(y - 1) in parent_li:
                if temp_g < self.g_cost[str(x) + ',' + str(y - 1)]:
                    self.g_cost[str(x) + ',' + str(y - 1)] = temp_g
                    self.parent[str(x) + ',' + str(y - 1)] = str(x) + "," + str(y)
                    self.h_cost[str(x) + "," + str(y - 1)] = temp_h
                    self.f_cost[str(x) + "," + str(y - 1)] = temp_f

        if str(x + 1) + ',' + str(y + 1) not in self.walls and (
                str(x + 1) + ',' + str(y + 1) in self.null or str(x + 1) + ',' + str(y + 1) in self.seen_not_visited):
            temp_g = self.find_g(x + 1, y + 1, x, y)
            temp_h = self.find_h(x + 1, y + 1)
            temp_f = temp_g + temp_h
            if str(x + 1) + ',' + str(y + 1) not in parent_li:
                self.parent[str(x + 1) + ',' + str(y + 1)] = str(x) + "," + str(y)
                self.g_cost[str(x + 1) + "," + str(y + 1)] = temp_g
                self.h_cost[str(x + 1) + "," + str(y + 1)] = temp_h
                self.f_cost[str(x + 1) + "," + str(y + 1)] = temp_f
                self.seen_not_visited.append(str(x + 1) + ',' + str(y + 1))
                self.null.remove(str(x + 1) + ',' + str(y + 1))
                self.new.append(str(x + 1) + ',' + str(y + 1))
            elif str(x + 1) + ',' + str(y + 1) in parent_li:
                if temp_g < self.g_cost[str(x + 1) + ',' + str(y + 1)]:
                    self.g_cost[str(x + 1) + ',' + str(y + 1)] = temp_g
                    self.parent[str(x + 1) + ',' + str(y + 1)] = str(x) + "," + str(y)
                    self.h_cost[str(x + 1) + "," + str(y + 1)] = temp_h
                    self.f_cost[str(x + 1) + "," + str(y + 1)] = temp_f

        if str(x - 1) + ',' + str(y + 1) not in self.walls and (
                str(x - 1) + ',' + str(y + 1) in self.null or str(x - 1) + ',' + str(y + 1) in self.seen_not_visited):
            temp_g = self.find_g(x - 1, y + 1, x, y)
            temp_h = self.find_h(x - 1, y + 1)
            temp_f = temp_g + temp_h
            if str(x - 1) + ',' + str(y + 1) not in parent_li:
                self.parent[str(x - 1) + ',' + str(y + 1)] = str(x) + "," + str(y)
                self.g_cost[str(x - 1) + "," + str(y + 1)] = temp_g
                self.h_cost[str(x - 1) + "," + str(y + 1)] = temp_h
                self.f_cost[str(x - 1) + "," + str(y + 1)] = temp_f
                self.seen_not_visited.append(str(x - 1) + ',' + str(y + 1))
                self.null.remove(str(x - 1) + ',' + str(y + 1))
                self.new.append(str(x - 1) + ',' + str(y + 1))
            elif str(x - 1) + ',' + str(y + 1) in parent_li:
                if temp_g < self.g_cost[str(x - 1) + ',' + str(y + 1)]:
                    self.g_cost[str(x - 1) + ',' + str(y + 1)] = temp_g
                    self.parent[str(x - 1) + ',' + str(y + 1)] = str(x) + "," + str(y)
                    self.h_cost[str(x - 1) + "," + str(y + 1)] = temp_h
                    self.f_cost[str(x - 1) + "," + str(y + 1)] = temp_f

        if str(x - 1) + ',' + str(y - 1) not in self.walls and (
                str(x - 1) + ',' + str(y - 1) in self.null or str(x - 1) + ',' + str(y - 1) in self.seen_not_visited):
            temp_g = self.find_g(x - 1, y - 1, x, y)
            temp_h = self.find_h(x - 1, y - 1)
            temp_f = temp_g + temp_h
            if str(x - 1) + ',' + str(y - 1) not in parent_li:
                self.parent[str(x - 1) + ',' + str(y - 1)] = str(x) + "," + str(y)
                self.g_cost[str(x - 1) + "," + str(y - 1)] = temp_g
                self.h_cost[str(x - 1) + "," + str(y - 1)] = temp_h
                self.f_cost[str(x - 1) + "," + str(y - 1)] = temp_f
                self.seen_not_visited.append(str(x - 1) + ',' + str(y - 1))
                self.null.remove(str(x - 1) + ',' + str(y - 1))
                self.new.append(str(x - 1) + ',' + str(y - 1))
            elif str(x - 1) + ',' + str(y - 1) in parent_li:
                if temp_g < self.g_cost[str(x - 1) + ',' + str(y - 1)]:
                    self.g_cost[str(x - 1) + ',' + str(y - 1)] = temp_g
                    self.parent[str(x - 1) + ',' + str(y - 1)] = str(x) + "," + str(y)
                    self.h_cost[str(x - 1) + "," + str(y - 1)] = temp_h
                    self.f_cost[str(x - 1) + "," + str(y - 1)] = temp_f

        if str(x + 1) + ',' + str(y - 1) not in self.walls and (
                str(x + 1) + ',' + str(y - 1) in self.null or str(x + 1) + ',' + str(y - 1) in self.seen_not_visited):
            temp_g = self.find_g(x + 1, y - 1, x, y)
            temp_h = self.find_h(x + 1, y - 1)
            temp_f = temp_g + temp_h
            if str(x + 1) + ',' + str(y - 1) not in parent_li:
                self.parent[str(x + 1) + ',' + str(y - 1)] = str(x) + "," + str(y)
                self.g_cost[str(x + 1) + "," + str(y - 1)] = temp_g
                self.h_cost[str(x + 1) + "," + str(y - 1)] = temp_h
                self.f_cost[str(x + 1) + "," + str(y - 1)] = temp_f
                self.seen_not_visited.append(str(x + 1) + ',' + str(y - 1))
                self.null.remove(str(x + 1) + ',' + str(y - 1))
                self.new.append(str(x + 1) + ',' + str(y - 1))
            elif str(x + 1) + ',' + str(y - 1) in parent_li:
                if temp_g < self.g_cost[str(x + 1) + ',' + str(y - 1)]:
                    self.g_cost[str(x + 1) + ',' + str(y - 1)] = temp_g
                    self.parent[str(x + 1) + ',' + str(y - 1)] = str(x) + "," + str(y)
                    self.h_cost[str(x + 1) + "," + str(y - 1)] = temp_h
                    self.f_cost[str(x + 1) + "," + str(y - 1)] = temp_f

    def next_move(self):
        f_cost_li = [y for x, y in self.f_cost.items() if x not in self.visited]
        h_cost_li = []
        min_f_cost = min(f_cost_li)
        same_min_f = []
        same_min_h = []
        total_same_min_f = 0
        total_same_min_h = 0

        for x, y in self.f_cost.items():
            if min_f_cost == y and x not in self.visited:
                total_same_min_f += 1
                same_min_f.append(x)

        if total_same_min_f == 1:
            return same_min_f[0]

        for x in same_min_f:
            h_cost_li.append(self.h_cost[x])

        min_h_cost = min(h_cost_li)

        for x in same_min_f:
            if min_h_cost == self.h_cost[x]:
                total_same_min_h += 1
                same_min_h.append(x)

        if total_same_min_h == 1:
            return same_min_h[0]

        else:
            return random.choice(same_min_h)

    def find_h(self, coord_x, coord_y):
        ver_hor = self.end_vert_hori()
        end_x_y = self.end.split(",")
        end_x = int(end_x_y[0])
        end_y = int(end_x_y[1])

        h_point = 0

        if coord_x == end_x and coord_y == end_y:
            return h_point

        while str(coord_x) + "," + str(coord_y) not in ver_hor:
            if coord_x == end_x and coord_y == end_y:
                return h_point
            if end_x > coord_x and end_y > coord_y:
                coord_x += 1
                coord_y += 1
                h_point += 14
            elif end_x < coord_x and end_y > coord_y:
                coord_x -= 1
                coord_y += 1
                h_point += 14
            elif end_x < coord_x and end_y < coord_y:
                coord_x -= 1
                coord_y -= 1
                h_point += 14
            elif end_x > coord_x and end_y < coord_y:
                coord_x += 1
                coord_y -= 1
                h_point += 14

        while 1:
            if (coord_x == end_x and coord_y == end_y):
                return h_point
            if end_x == coord_x and end_y > coord_y:
                coord_y += 1
                h_point += 10
            elif end_x > coord_x and end_y == coord_y:
                coord_x += 1
                h_point += 10
            elif end_x < coord_x and end_y == coord_y:
                coord_x -= 1
                h_point += 10
            elif end_x == coord_x and end_y < coord_y:
                coord_y -= 1
                h_point += 10

    def find_g(self, coord_x, coord_y, par_x, par_y):
        g_point = 0

        par = str(par_x) + "," + str(par_y)

        if par not in self.parent.keys():
            if (par_x + 1 == coord_x and par_y == coord_y) or (par_x - 1 == coord_x and par_y == coord_y) or (
                    par_x == coord_x and par_y - 1 == coord_y) or (par_x == coord_x and par_y + 1 == coord_y):
                g_point += 10
            else:
                g_point += 14
            return g_point

        else:
            if (par_x + 1 == coord_x and par_y == coord_y) or (par_x - 1 == coord_x and par_y == coord_y) or (
                    par_x == coord_x and par_y - 1 == coord_y) or (par_x == coord_x and par_y + 1 == coord_y):
                g_point = self.g_cost[par] + 10
            else:
                g_point = self.g_cost[par] + 14
            return g_point

    def end_vert_hori(self):
        li = []

        end_x_y = self.end.split(",")
        end_x = int(end_x_y[0])
        end_y = int(end_x_y[1])

        for x in range(board.row):
            li.append(str(end_x) + ',' + str(x))
        for x in range(board.column):
            li.append(str(x) + ',' + str(end_y))

        return li


class Grid:
    def __init__(self, row, column):
        self.row = row
        self.column = column

        self.start_x_y = []
        self.end_x_y = []
        self.walls_x_y = []

        self.buttons = [[''] * self.column] * self.row

        for x in range(self.row):
            for y in range(self.column):
                coord_obj = []
                self.buttons[x][y] = Button(grid_frame, height=1, width=3, bg="white")
                coord_obj.append(str(y) + "," + str(x))
                coord_obj.append(self.buttons[x][y])
                self.buttons[x][y].configure(command=lambda button_vals=coord_obj: self.color(button_vals))
                self.buttons[x][y].grid(row=x, column=y)

    def color(self, coord_obj):
        if start_button_state == 1:
            self.start(coord_obj)
            if coord_obj not in self.end_x_y and coord_obj not in self.walls_x_y and coord_obj in self.start_x_y:
                coord_obj[1].configure(bg="green")

        elif end_button_state == 1:
            self.end(coord_obj)
            if coord_obj not in self.start_x_y and coord_obj not in self.walls_x_y and coord_obj in self.end_x_y:
                coord_obj[1].configure(bg="red")

        elif wall_button_state == 1:
            self.wall(coord_obj)
            if coord_obj not in self.start_x_y and coord_obj not in self.end_x_y and coord_obj in self.walls_x_y:
                coord_obj[1].configure(bg="gray")

    def start(self, coord_obj):

        if not self.start_x_y and coord_obj not in self.end_x_y and coord_obj not in self.walls_x_y:
            self.start_x_y.append(coord_obj)

        elif coord_obj not in self.start_x_y and coord_obj not in self.end_x_y and coord_obj not in self.walls_x_y:
            self.start_x_y[0][1].configure(bg="white")
            self.start_x_y.append(coord_obj)
            del self.start_x_y[0]

    def end(self, coord_obj):

        if not self.end_x_y and coord_obj not in self.walls_x_y and coord_obj not in self.start_x_y:
            self.end_x_y.append(coord_obj)

        elif coord_obj not in self.start_x_y and coord_obj not in self.end_x_y and coord_obj not in self.walls_x_y:
            self.end_x_y[0][1].configure(bg="white")
            self.end_x_y.append(coord_obj)
            del self.end_x_y[0]

    def wall(self, coord_obj):

        if coord_obj in self.walls_x_y:
            coord_obj[1].configure(bg="white")
            self.walls_x_y.remove(coord_obj)

        elif coord_obj not in self.start_x_y and coord_obj not in self.end_x_y and coord_obj not in self.walls_x_y:
            self.walls_x_y.append(coord_obj)

    def color_green(self, x_y):
        for coords in x_y:
            coord = coords.split(",")
            x = int(coord[1])
            y = int(coord[0])
            self.buttons[x][y] = Button(grid_frame, height=1, width=3, bg="#90EE90")
            self.buttons[x][y].grid(row=x, column=y)
            self.buttons[x][y].update()

    def color_red(self, x_y):
        coord = x_y.split(",")
        x = int(coord[1])
        y = int(coord[0])
        self.buttons[x][y] = Button(grid_frame, height=1, width=3, bg="#ffcccb")
        self.buttons[x][y].grid(row=x, column=y)
        self.buttons[x][y].update()

    def color_blue(self, x_y):
        for coords in x_y[::-1]:
            coord = coords.split(",")
            x = int(coord[1])
            y = int(coord[0])
            self.buttons[x][y] = Button(grid_frame, height=1, width=3, bg="blue")
            self.buttons[x][y].grid(row=x, column=y)
            self.buttons[x][y].update()


board = Grid(25, 44)


def start_button():
    global start_button_state
    global end_button_state
    global wall_button_state

    if start_button_state == 0:
        end_button_state = 0
        wall_button_state = 0
        start_button_state = 1

    else:
        end_button_state = 0
        wall_button_state = 0
        start_button_state = 0


def end_button():
    global start_button_state
    global end_button_state
    global wall_button_state

    if end_button_state == 0:
        end_button_state = 1
        wall_button_state = 0
        start_button_state = 0

    else:
        end_button_state = 0
        wall_button_state = 0
        start_button_state = 0


def wall_button():
    global start_button_state
    global end_button_state
    global wall_button_state

    if wall_button_state == 0:
        end_button_state = 0
        wall_button_state = 1
        start_button_state = 0

    else:
        end_button_state = 0
        wall_button_state = 0
        start_button_state = 0


def find(start,end,wall):
    try:
        global start_button_state
        global end_button_state
        global wall_button_state

        end_button_state = 0
        wall_button_state = 0
        start_button_state = 0

        only_coord_start = board.start_x_y[0][0]
        only_coord_end = board.end_x_y[0][0]
        only_coord_walls = [li[0] for li in board.walls_x_y]

        start["state"]="disabled"
        end["state"] = "disabled"
        wall["state"] = "disabled"

        AStar(only_coord_start, only_coord_end, only_coord_walls)

    except:
        return


def clear():
    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)


add_object_frame = LabelFrame(root, width=400)
add_object_frame.grid(row=1, column=0)

add_start = Button(add_object_frame, text="Start Point", padx=5, pady=5, command=start_button)
add_start.grid(row=0, column=1, padx=100, pady=10)

add_end = Button(add_object_frame, text="End Point", padx=5, pady=5, command=end_button)
add_end.grid(row=0, column=2, padx=100, pady=10)

add_wall = Button(add_object_frame, text="Walls", padx=5, pady=5, command=wall_button)
add_wall.grid(row=0, column=3, padx=100, pady=10)

find_path = Button(add_object_frame, text="Find path", padx=5, pady=5,command=lambda: find(add_start,add_end,add_wall))
find_path.grid(row=0, column=4, padx=100, pady=10)

refresh = Button(add_object_frame, text="Clear all", padx=5, pady=5, command=clear)
refresh.grid(row=0, column=5, padx=100, pady=10)

root.mainloop()

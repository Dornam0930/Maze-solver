from interface import Window, Maze

def main():
    margin_x = 50
    margin_y = 50
    num_colums = 10
    num_rows = 10
    cell_size_x = 50
    cell_size_y = 50
    seed = None
    win = Window(800, 600)
    maze = Maze(margin_x, margin_y, num_colums, num_rows, cell_size_x, cell_size_y, win=win, seed=seed)
    maze._break_walls_r(0, 0)
    maze._reset_cells_visited()
    is_solved = maze.solve()
    if is_solved:
        print("maze solved")
    else:
        print("maze is not solvable")
    win.wait_for_close()

main()
import unittest
from interface import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1._cells), num_cols)
        self.assertEqual(len(m1._cells[0]), num_rows)

    def test_start_end_break(self):
        num_cols = 10
        num_rows = 10
        m2 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(m2._cells[0][0].has_top_wall, False)
        self.assertEqual(m2._cells[-1][-1].has_bottom_wall, False)

    def test_reset_cell_visited(self):
        maze = Maze(50, 50, 10, 10, 50, 50)
        maze._break_walls_r(0, 0)
        maze._reset_cells_visited()
        for column in maze._cells:
            for row in column:
                self.assertEqual(row.visited, False)


if __name__ == "__main__":
    unittest.main()
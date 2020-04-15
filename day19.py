import unittest
from day15 import Computer
import numpy as np
from matplotlib import pyplot as plt


def find_halfway(sample_1, sample_2):
    x1, y1 = sample_1
    x2, y2 = sample_2
    x = (x1 + x2)//2
    y = (y1 + y2)//2
    return x, y


class Tractor:
    def __init__(self, program, shape):
        self.program = program
        self.shape = shape
        if shape:
            self.area = np.full(shape, fill_value=np.nan)

    def show_plot(self):
        plt.imshow(self.area.transpose())
        plt.show()

    def count_affected_points(self): # 0.453 s
        self.find_tractor_beam()
        return np.nansum(self.area)

    def find_tractor_beam(self):
        point_in = 8, 6
        point_out = 8, 0
        border = self.find_border_between(point_in, point_out)
        self.follow_border(*border)
        point_out = 8, 20
        border = self.find_border_between(point_in, point_out)
        self.follow_border(*border)
        self.fill_top_left(10)
        self.fill_empty()
        self.show_plot()

    def find_border_between(self, point_in, point_out):
        halfway = find_halfway(point_in, point_out)
        if halfway == point_in:
            return halfway, point_out
        if halfway == point_out:
            return point_in, halfway
        half_val = self.in_tractor_beam(*halfway)
        if half_val == 1:
            border = self.find_border_between(halfway, point_out)
        else:
            border = self.find_border_between(point_in, halfway)
        return border

    def in_tractor_beam(self, i, j):
        computer = Computer(self.program)
        computer.set_input([i, j])
        prog = computer.run_program()
        result = next(prog)
        if hasattr(self, 'area'):
            self.area[i, j] = result
        return result

    def follow_border(self, point_in, point_out):
        i_in, j_in = point_in
        i_out, j_out = point_out
        points_in = [point_in]
        points_out = [point_out]
        i = i_in
        j = j_in
        while i < self.shape[0] - 1:
            i = i + 1
            if j_out > j_in:
                add = 1
            else:
                add = -1
            found_in = False
            found_out = False
            while not(found_in and found_out) and j > 0 and j < self.shape[1]:
                if self.in_tractor_beam(i, j):
                    points_in.append((i, j))
                    j = j + add
                    found_in = True
                else:
                    points_out.append((i, j))
                    j = j - add
                    found_out = True
        return points_in, points_out

    def fill_top_left(self, num):
        for i in range(num):
            for j in range(num):
                self.area[i, j] = self.in_tractor_beam(i, j)

    def fill_empty(self):
        for row_num, row in enumerate(self.area):
            in_tractor = np.argwhere(row == 1)
            if in_tractor.size > 0:
                min_in = in_tractor.min()
                max_in = in_tractor.max()
                self.area[row_num, min_in:max_in] = 1

    def find_left_border(self, row_num):
        step_size = int(80/np.sqrt(600) * np.sqrt(row_num))
        sample_out = (row_num, 0)
        col_num = step_size
        while True:
            if self.in_tractor_beam(row_num, col_num):
                sample_in = row_num, col_num
                break
            col_num = col_num + step_size
        border, _ = self.find_border_between(sample_in, sample_out)
        return border[1]

    def fits(self, square_size, row):
        col = self.find_left_border(row)
        return (self.in_tractor_beam(row - square_size + 1,
                                     col + square_size - 1) == 1)

    def binary_search(self, square_size, lower, upper):
        while True:
            halfway = int((lower + upper) / 2)
            if halfway == lower:
                return upper - 1
            if halfway == upper:
                return lower
            half_fits = self.fits(square_size, halfway)
            if half_fits:
                upper = halfway
            else:
                lower = halfway

    def find_lowest_fits(self, square_size, lower, upper):
        lowest_row = self.binary_search(square_size, lower, upper)
        col = self.find_left_border(lowest_row) - 1
        return lowest_row - square_size - 1, col - 1

class TestTractor(unittest.TestCase):
    def test_count_beam(self):
        size = 50
        with open('day19_input.txt') as infile:
            program = list(map(int, infile.read().split(',')))
        tractor = Tractor(program, (size, size))
        result = tractor.count_affected_points()
        self.assertEqual(199, result)

    def test_find_left_border(self):
        grid_size = 1000
        with open('day19_input.txt') as infile:
            program = list(map(int, infile.read().split(',')))
        tractor = Tractor(program, (grid_size, grid_size))
        result = tractor.find_left_border(617)
        self.assertEqual(401, result)

    def test_fits(self):
        with open('day19_input.txt') as infile:
            program = list(map(int, infile.read().split(',')))
        tractor = Tractor(program, None)
        self.assertEqual(True, tractor.fits(100, 10000))
        self.assertEqual(False, tractor.fits(100, 617))
        self.assertEqual(False, tractor.fits(100, 1027))
        self.assertEqual(True, tractor.fits(100, 1127))

    def test_find_lowest_fits(self):
        grid_size = 1500
        with open('day19_input.txt') as infile:
            program = list(map(int, infile.read().split(',')))
        tractor = Tractor(program, None)
        self.assertEqual((1018, 726), tractor.find_lowest_fits(100, 200, 1500))
        print(10000*1018 + 726)

    def test_plot_square(self):
        grid_size = 1200
        with open('day19_input.txt') as infile:
            program = list(map(int, infile.read().split(',')))
        tractor = Tractor(program, (grid_size, grid_size))
        tractor.count_affected_points()
        left = 1018
        top = 726
        tractor.area[left:left + 100, top:top + 100] = 2
        tractor.show_plot()


if __name__ == '__main__':
    unittest.main()

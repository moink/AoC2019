import unittest
from collections import deque, MutableMapping

import math
from numpy.testing import assert_array_equal
from itertools import zip_longest

import numpy as np

import matplotlib.pyplot as plt

TEST_PROGRAM = [
    3, 8, 1005, 8, 330, 1106, 0, 11, 0, 0, 0, 104, 1, 104, 0, 3, 8, 102,
    -1, 8, 10, 1001, 10, 1, 10, 4, 10, 108, 0, 8, 10, 4, 10, 1001, 8, 0,
    28, 1, 1103, 17, 10, 1006, 0, 99, 1006, 0, 91, 1, 102, 7, 10, 3, 8,
    1002, 8, -1, 10, 101, 1, 10, 10, 4, 10, 108, 1, 8, 10, 4, 10, 1002,
    8, 1, 64, 3, 8, 102, -1, 8, 10, 1001, 10, 1, 10, 4, 10, 108, 0, 8,
    10, 4, 10, 102, 1, 8, 86, 2, 4, 0, 10, 1006, 0, 62, 2, 1106, 13, 10,
    3, 8, 1002, 8, -1, 10, 1001, 10, 1, 10, 4, 10, 1008, 8, 0, 10, 4,
    10, 101, 0, 8, 120, 1, 1109, 1, 10, 1, 105, 5, 10, 3, 8, 102, -1, 8,
    10, 1001, 10, 1, 10, 4, 10, 108, 1, 8, 10, 4, 10, 1002, 8, 1, 149,
    1, 108, 7, 10, 1006, 0, 40, 1, 6, 0, 10, 2, 8, 9, 10, 3, 8, 102, -1,
    8, 10, 1001, 10, 1, 10, 4, 10, 1008, 8, 1, 10, 4, 10, 1002, 8, 1,
    187, 1, 1105, 10, 10, 3, 8, 102, -1, 8, 10, 1001, 10, 1, 10, 4, 10,
    1008, 8, 1, 10, 4, 10, 1002, 8, 1, 213, 1006, 0, 65, 1006, 0, 89, 1,
    1003, 14, 10, 3, 8, 102, -1, 8, 10, 1001, 10, 1, 10, 4, 10, 108, 0,
    8, 10, 4, 10, 102, 1, 8, 244, 2, 1106, 14, 10, 1006, 0, 13, 3, 8,
    102, -1, 8, 10, 1001, 10, 1, 10, 4, 10, 108, 0, 8, 10, 4, 10, 1001,
    8, 0, 273, 3, 8, 1002, 8, -1, 10, 1001, 10, 1, 10, 4, 10, 108, 1, 8,
    10, 4, 10, 1001, 8, 0, 295, 1, 104, 4, 10, 2, 108, 20, 10, 1006, 0,
    94, 1006, 0, 9, 101, 1, 9, 9, 1007, 9, 998, 10, 1005, 10, 15, 99,
    109, 652, 104, 0, 104, 1, 21102, 937268450196, 1, 1, 21102, 1, 347,
    0, 1106, 0, 451, 21101, 387512636308, 0, 1, 21102, 358, 1, 0, 1105,
    1, 451, 3, 10, 104, 0, 104, 1, 3, 10, 104, 0, 104, 0, 3, 10, 104, 0,
    104, 1, 3, 10, 104, 0, 104, 1, 3, 10, 104, 0, 104, 0, 3, 10, 104, 0,
    104, 1, 21101, 0, 97751428099, 1, 21102, 1, 405, 0, 1105, 1, 451,
    21102, 1, 179355806811, 1, 21101, 416, 0, 0, 1106, 0, 451, 3, 10,
    104, 0, 104, 0, 3, 10, 104, 0, 104, 0, 21102, 1, 868389643008, 1,
    21102, 439, 1, 0, 1105, 1, 451, 21102, 1, 709475853160, 1, 21102,
    450, 1, 0, 1105, 1, 451, 99, 109, 2, 22102, 1, -1, 1, 21101, 0, 40,
    2, 21101, 482, 0, 3, 21102, 1, 472, 0, 1105, 1, 515, 109, -2, 2106,
    0, 0, 0, 1, 0, 0, 1, 109, 2, 3, 10, 204, -1, 1001, 477, 478, 493, 4,
    0, 1001, 477, 1, 477, 108, 4, 477, 10, 1006, 10, 509, 1101, 0, 0,
    477, 109, -2, 2105, 1, 0, 0, 109, 4, 2101, 0, -1, 514, 1207, -3, 0,
    10, 1006, 10, 532, 21101, 0, 0, -3, 21202, -3, 1, 1, 22101, 0, -2,
    2, 21101, 1, 0, 3, 21101, 0, 551, 0, 1105, 1, 556, 109, -4, 2106, 0,
    0, 109, 5, 1207, -3, 1, 10, 1006, 10, 579, 2207, -4, -2, 10, 1006,
    10, 579, 22102, 1, -4, -4, 1105, 1, 647, 21201, -4, 0, 1, 21201, -3,
    -1, 2, 21202, -2, 2, 3, 21101, 0, 598, 0, 1106, 0, 556, 22101, 0, 1,
    -4, 21102, 1, 1, -1, 2207, -4, -2, 10, 1006, 10, 617, 21101, 0, 0,
    -1, 22202, -2, -1, -2, 2107, 0, -3, 10, 1006, 10, 639, 22102, 1, -1,
    1, 21102, 1, 639, 0, 105, 1, 514, 21202, -2, -1, -2, 22201, -4, -2,
    -4, 109, -5, 2105, 1, 0]


def grouper(iterable, n):
    args = [iter(iterable)] * n
    return zip_longest(*args)


class Memory(MutableMapping):

    def __init__(self, init_vals):
        self.contents = {i: val for i, val in enumerate(init_vals)}

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise TypeError('Index must be an integer')
        try:
            result = self.contents[item]
        except KeyError:
            if item < 0:
                raise
            result = 0
        return result

    def __iter__(self):
        return self.contents.__iter__()

    def __len__(self):
        return max(self.contents.keys())

    def __setitem__(self, key, value):
        self.contents[key] = value

    def __delitem__(self, key):
        del self.contents[key]


class Computer():

    def __init__(self, program):
        self.program = Memory(program)
        self.pointer = 0
        self.relative_base = 0
        self.inputs = deque()

    def add_to_inputs(self, value):
        self.inputs.append(value)

    def run_program(self):
        while self.program[self.pointer] != 99:
            op_code = self.program[self.pointer] % 100
            if op_code == 1:
                self.add()
            elif op_code == 2:
                self.multiply()
            elif op_code == 3:
                self.read_input()
            elif op_code == 4:
                param_1 = self.prepare_get_param(1)
                yield param_1
                self.pointer = self.pointer + 2
            elif op_code == 5:
                self.jump_if_true()
            elif op_code == 6:
                self.jump_if_false()
            elif op_code == 7:
                self.compare_less_than()
            elif op_code == 8:
                self.compare_equal()
            elif op_code == 9:
                self.change_relative_base()
            else:
                raise ValueError('No such operation ' + str(op_code))
        return

    def change_relative_base(self):
        param = self.prepare_get_param(1)
        self.relative_base = self.relative_base + param
        self.pointer = self.pointer + 2

    def compare_equal(self):
        param_1 = self.prepare_get_param(1)
        param_2 = self.prepare_get_param(2)
        self.set_param(3, int(param_1 == param_2))
        self.pointer = self.pointer + 4

    def compare_less_than(self):
        param_1 = self.prepare_get_param(1)
        param_2 = self.prepare_get_param(2)
        self.set_param(3, int(param_1 < param_2))
        self.pointer = self.pointer + 4

    def jump_if_false(self):
        param_1 = self.prepare_get_param(1)
        param_2 = self.prepare_get_param(2)
        if not param_1:
            self.pointer = param_2
        else:
            self.pointer = self.pointer + 3

    def jump_if_true(self):
        param_1 = self.prepare_get_param(1)
        param_2 = self.prepare_get_param(2)
        if param_1:
            self.pointer = param_2
        else:
            self.pointer = self.pointer + 3

    def read_input(self):
        self.set_param(1, self.inputs.popleft())
        self.pointer = self.pointer + 2

    def multiply(self):
        param_1 = self.prepare_get_param(1)
        param_2 = self.prepare_get_param(2)
        self.set_param(3, param_1 * param_2)
        self.pointer = self.pointer + 4

    def add(self):
        param_1 = self.prepare_get_param(1)
        param_2 = self.prepare_get_param(2)
        self.set_param(3, param_1 + param_2)
        self.pointer = self.pointer + 4

    def prepare_get_param(self, param_num):
        mode = self.get_mode(param_num)
        val = self.program[self.pointer + param_num]
        if mode == 0:
            result = self.program[val]
        elif mode == 1:
            result = val
        elif mode == 2:
            result = self.program[val + self.relative_base]
        else:
            raise ValueError('Unknown mode {}'.format(mode))
        return result

    def get_mode(self, param_num):
        mode = (self.program[self.pointer] //
                (10 ** (param_num + 1))) % 10
        if mode not in [0, 1, 2]:
            raise ValueError('Unknown mode {} from {}'
                             .format(mode, self.program[self.pointer]))
        return mode

    def set_param(self, param_num, value):
        mode = self.get_mode(param_num)
        val = self.program[self.pointer + param_num]
        if mode == 0:
            self.program[val] = value
        elif mode == 2:
            self.program[val + self.relative_base] = value
        else:
            raise ValueError('Unknown mode {}'.format(mode))


class PaintingRobot:
    def __init__(self, grid, position, program):
        self.grid = grid
        self.position = position
        self.facing = 0
        self.computer = Computer(program)

    def paint_grid(self):
        been_painted = set()
        cur_colour = self.grid[self.position]
        self.computer.add_to_inputs(cur_colour)
        for new_colour, direction in grouper(self.computer.run_program(), 2):
            been_painted.add(self.position)
            self.paint_panel(new_colour)
            self.turn_and_move(direction)
            cur_colour = self.grid[self.position]
            self.computer.add_to_inputs(cur_colour)
        return self.grid, len(been_painted)

    def paint_panel(self, colour):
        if colour not in [0, 1]:
            raise ValueError('Invalid colour {}'.format(colour))
        self.grid[self.position] = colour

    def turn_and_move(self, direction):
        if direction == 0:  # turn left
            self.facing = self.facing - 90
        elif direction == 1: # turn right
            self.facing = self.facing + 90
        else:
            raise ValueError('Invalid direction {}'.format(direction))
        self.facing = self.facing % 360
        x, y = self.position
        if self.facing == 0:
            y = y - 1
        elif self.facing == 90:
            x = x + 1
        elif self.facing == 180:
            y = y + 1
        elif self.facing == 270:
            x = x - 1
        self.position = x, y


class TestRobot(unittest.TestCase):

    def test_copy_program(self):
        program = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006,
                   101, 0, 99]
        output = list(Computer(program).run_program())
        self.assertEqual(program, output)

    def test_sixteen_digit(self):
        program = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
        output = list(Computer(program).run_program())[0]
        self.assertIsInstance(output, int)
        self.assertEqual(16, len(str(output)))

    def test_output_middle(self):
        program = [104, 1125899906842624, 99]
        output = list(Computer(program).run_program())[0]
        self.assertEqual(1125899906842624, output)

    def run_get_mode_test(self, code, param_num, expected_mode):
        mode = Computer([code]).get_mode(param_num)
        self.assertEqual(expected_mode, mode)

    def test_get_mode(self):
        self.run_get_mode_test(0, 1, 0)
        self.run_get_mode_test(0, 2, 0)
        self.run_get_mode_test(100, 1, 1)
        self.run_get_mode_test(100, 2, 0)
        self.run_get_mode_test(200, 1, 2)
        self.run_get_mode_test(200, 2, 0)
        self.run_get_mode_test(2000, 1, 0)
        self.run_get_mode_test(2000, 2, 2)
        self.run_get_mode_test(21107, 1, 1)
        self.run_get_mode_test(21107, 2, 1)
        self.run_get_mode_test(21107, 3, 2)

    def test_paint_grid(self):
        grid_size = 72
        initial_pos = int(math.ceil(grid_size/2))
        initial_grid = np.zeros((grid_size, grid_size), int)
        robot = PaintingRobot(initial_grid, (initial_pos, initial_pos),
                              TEST_PROGRAM)
        final_grid, num_painted = robot.paint_grid()
        self.assertEqual(1564, num_painted)

    def test_paint_panel_black(self):
        initial_grid = np.zeros((5, 5), int)
        robot = PaintingRobot(initial_grid, (2, 2), TEST_PROGRAM)
        robot.paint_panel(0)
        final_grid = robot.grid
        assert_array_equal(initial_grid, final_grid)

    def test_paint_panel_white(self):
        initial_grid = np.zeros((5, 5), int)
        expected_grid = initial_grid.copy()
        expected_grid[2, 2] = 1
        robot = PaintingRobot(initial_grid, (2, 2), TEST_PROGRAM)
        robot.paint_panel(1)
        final_grid = robot.grid
        assert_array_equal(expected_grid, final_grid)

    def test_paint_grid(self):
        grid_size = 86
        initial_pos = int(math.ceil(grid_size/2))
        initial_grid = np.zeros((grid_size, grid_size), int)
        initial_grid[(initial_pos, initial_pos)] = 1
        robot = PaintingRobot(initial_grid, (initial_pos, initial_pos),
                              TEST_PROGRAM)
        final_grid, num_painted = robot.paint_grid()
        self.assertEqual(249, num_painted)
        plt.imshow(final_grid.transpose())
        plt.show()


if __name__ == '__main__':
    unittest.main()

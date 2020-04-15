import unittest
from collections import deque, MutableMapping

import math
from numpy.testing import assert_array_equal
from itertools import zip_longest
import contextlib
import numpy as np



PROGRAM = [
    3, 1033, 1008, 1033, 1, 1032, 1005, 1032, 31, 1008, 1033, 2, 1032, 1005,
    1032, 58, 1008, 1033, 3, 1032, 1005, 1032, 81, 1008, 1033, 4, 1032, 1005,
    1032, 104, 99, 101, 0, 1034, 1039, 1001, 1036, 0, 1041, 1001, 1035, -1,
    1040, 1008, 1038, 0, 1043, 102, -1, 1043, 1032, 1, 1037, 1032, 1042, 1106,
    0, 124, 101, 0, 1034, 1039, 101, 0, 1036, 1041, 1001, 1035, 1, 1040, 1008,
    1038, 0, 1043, 1, 1037, 1038, 1042, 1105, 1, 124, 1001, 1034, -1, 1039,
    1008, 1036, 0, 1041, 1002, 1035, 1, 1040, 1001, 1038, 0, 1043, 1002, 1037,
    1, 1042, 1106, 0, 124, 1001, 1034, 1, 1039, 1008, 1036, 0, 1041, 102, 1,
    1035, 1040, 1001, 1038, 0, 1043, 102, 1, 1037, 1042, 1006, 1039, 217, 1006,
    1040, 217, 1008, 1039, 40, 1032, 1005, 1032, 217, 1008, 1040, 40, 1032,
    1005, 1032, 217, 1008, 1039, 39, 1032, 1006, 1032, 165, 1008, 1040, 39,
    1032, 1006, 1032, 165, 1101, 2, 0, 1044, 1106, 0, 224, 2, 1041, 1043, 1032,
    1006, 1032, 179, 1102, 1, 1, 1044, 1106, 0, 224, 1, 1041, 1043, 1032, 1006,
    1032, 217, 1, 1042, 1043, 1032, 1001, 1032, -1, 1032, 1002, 1032, 39, 1032,
    1, 1032, 1039, 1032, 101, -1, 1032, 1032, 101, 252, 1032, 211, 1007, 0, 59,
    1044, 1106, 0, 224, 1101, 0, 0, 1044, 1106, 0, 224, 1006, 1044, 247, 101, 0,
    1039, 1034, 1001, 1040, 0, 1035, 1002, 1041, 1, 1036, 102, 1, 1043, 1038,
    101, 0, 1042, 1037, 4, 1044, 1105, 1, 0, 33, 20, 19, 43, 28, 91, 62, 55, 96,
    28, 52, 9, 24, 99, 11, 45, 80, 58, 96, 2, 8, 76, 1, 37, 5, 95, 18, 6, 97,
    67, 47, 4, 19, 29, 74, 57, 45, 65, 17, 43, 93, 33, 71, 93, 26, 2, 86, 11,
    31, 74, 85, 36, 94, 20, 89, 68, 45, 99, 43, 21, 3, 92, 69, 95, 8, 30, 84,
    45, 10, 64, 95, 49, 60, 60, 45, 30, 94, 36, 17, 97, 90, 39, 4, 97, 76, 28,
    80, 92, 5, 66, 20, 69, 95, 43, 95, 35, 30, 67, 67, 87, 36, 44, 11, 83, 62,
    73, 42, 80, 20, 99, 79, 46, 1, 75, 85, 24, 5, 84, 47, 78, 91, 91, 38, 74,
    16, 31, 96, 37, 60, 69, 12, 96, 2, 5, 83, 24, 67, 42, 7, 67, 94, 77, 34, 6,
    75, 2, 61, 37, 15, 11, 65, 13, 63, 39, 42, 93, 22, 12, 89, 58, 98, 28, 69,
    13, 98, 68, 34, 13, 93, 56, 85, 28, 92, 45, 84, 79, 70, 12, 27, 85, 1, 86,
    94, 57, 64, 30, 75, 78, 49, 91, 19, 94, 77, 34, 40, 15, 64, 26, 34, 31, 70,
    65, 34, 65, 7, 73, 61, 8, 23, 82, 55, 78, 36, 93, 10, 29, 64, 42, 99, 34,
    91, 17, 33, 98, 45, 44, 74, 98, 60, 76, 6, 44, 73, 11, 13, 11, 73, 92, 55,
    90, 3, 54, 23, 75, 28, 36, 82, 89, 84, 6, 39, 31, 39, 98, 34, 61, 21, 93,
    48, 71, 80, 7, 46, 76, 71, 17, 7, 91, 6, 22, 76, 70, 27, 98, 35, 29, 69, 93,
    42, 81, 62, 46, 87, 47, 51, 66, 2, 60, 3, 76, 68, 68, 74, 70, 3, 89, 18, 2,
    57, 74, 79, 97, 16, 5, 73, 19, 90, 49, 6, 41, 88, 83, 34, 63, 52, 84, 14,
    19, 76, 78, 88, 19, 92, 90, 34, 16, 69, 45, 85, 30, 71, 16, 77, 30, 43, 65,
    85, 66, 11, 2, 72, 3, 83, 84, 14, 86, 90, 74, 79, 35, 33, 29, 78, 9, 92, 35,
    64, 32, 30, 66, 9, 65, 30, 85, 81, 44, 95, 41, 22, 16, 28, 75, 63, 72, 23,
    5, 73, 24, 89, 80, 25, 40, 88, 62, 3, 68, 6, 80, 6, 39, 17, 76, 24, 78, 6,
    90, 79, 38, 44, 78, 85, 29, 48, 25, 75, 27, 76, 92, 19, 93, 21, 61, 56, 13,
    64, 92, 52, 77, 12, 33, 77, 41, 75, 86, 29, 34, 65, 38, 66, 17, 15, 95, 50,
    87, 52, 64, 72, 73, 6, 26, 80, 71, 8, 86, 1, 23, 67, 10, 72, 89, 9, 95, 60,
    20, 46, 64, 99, 34, 46, 65, 14, 54, 93, 84, 4, 13, 86, 12, 26, 68, 56, 33,
    83, 12, 93, 42, 74, 9, 99, 62, 22, 20, 83, 75, 13, 71, 96, 53, 96, 41, 8,
    15, 76, 97, 55, 8, 78, 85, 57, 79, 30, 87, 17, 46, 62, 85, 14, 70, 63, 82,
    28, 46, 96, 35, 89, 6, 9, 27, 44, 86, 93, 28, 9, 97, 73, 14, 7, 84, 64, 15,
    62, 14, 17, 88, 92, 82, 11, 47, 63, 73, 13, 94, 98, 88, 15, 37, 38, 11, 2,
    74, 20, 73, 94, 26, 96, 64, 56, 80, 53, 48, 85, 85, 35, 15, 90, 63, 9, 42,
    99, 81, 97, 26, 94, 32, 24, 96, 61, 38, 18, 57, 22, 76, 7, 5, 43, 55, 97,
    74, 35, 99, 86, 24, 25, 8, 60, 75, 18, 61, 14, 97, 52, 64, 97, 45, 29, 69,
    91, 43, 40, 99, 58, 72, 73, 70, 45, 5, 97, 37, 89, 77, 32, 92, 94, 6, 33,
    72, 64, 35, 75, 14, 32, 99, 64, 54, 78, 1, 92, 35, 30, 71, 11, 48, 82, 61,
    49, 12, 46, 75, 54, 52, 33, 92, 24, 11, 72, 72, 16, 17, 57, 72, 68, 46, 15,
    85, 58, 74, 55, 54, 87, 97, 44, 94, 16, 84, 57, 56, 96, 33, 79, 7, 70, 50,
    23, 98, 91, 6, 62, 51, 73, 68, 17, 83, 93, 56, 15, 81, 99, 88, 15, 13, 93,
    53, 48, 69, 2, 14, 83, 86, 39, 4, 54, 69, 52, 42, 60, 79, 92, 38, 68, 90,
    48, 77, 46, 77, 16, 89, 3, 96, 77, 11, 77, 23, 73, 98, 35, 3, 1, 97, 48, 62,
    36, 74, 13, 93, 19, 71, 23, 70, 64, 64, 14, 71, 86, 98, 20, 95, 1, 97, 30,
    92, 16, 98, 63, 94, 56, 90, 49, 94, 28, 88, 43, 84, 38, 74, 83, 62, 4, 98,
    63, 69, 0, 0, 21, 21, 1, 10, 1, 0, 0, 0, 0, 0, 0]


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

    def set_input(self, value):
        for val in value:
            self.inputs.append(val)

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


class RepairDroid:
    def __init__(self, program, size):
        self.start_position = (size // 2 + 1, size // 2 + 1)
        self.position = self.start_position
        self.grid = np.full((size, size), fill_value=np.nan)
        self.grid[self.position] = 1
        self.computer = Computer(program)
        self.program = self.computer.run_program()
        self.direction = 1

    def explore(self):
        self.take_one_step()
        step = 1
        steps = 0
        while self.position != self.start_position:
        # while tile < 2:
            tile = self.take_one_step()
            step = step + 1
            if tile == 2:
                steps = step
        np.save('maze.np', self.grid)
        plt.show()
        return steps

    def take_one_step(self):
        tile = self.try_turn_right()
        if tile:
            return tile
        tile = self.try_go_straight()
        if tile:
            return tile
        tile = self.try_turn_left()
        if tile:
            return tile
        tile = self.turn_around()
        return tile

    def try_turn_right(self):
        dir_change = {1: 4, 2: 3, 3: 1, 4: 2}
        return self.try_turning(dir_change)

    def try_go_straight(self):
        dir_change = {key: key for key in range(1, 5)}
        return self.try_turning(dir_change)

    def try_turn_left(self):
        dir_change = {1: 3, 2: 4, 3: 2, 4: 1}
        return self.try_turning(dir_change)

    def turn_around(self):
        dir_change = {1: 2, 2: 1, 3: 4, 4: 3}
        return self.try_turning(dir_change)

    def try_turning(self, dir_change):
        direction = dir_change[self.direction]
        tile = self.try_movement(direction)
        if tile:
            self.direction = direction
        return tile

    def try_movement(self, direction):
        self.computer.set_input(direction)
        new_position = self.move_direction(direction)
        tile = next(self.program)
        self.grid[new_position] = tile
        if tile:
            self.position = new_position
        self.draw_map()
        return tile

    def draw_map(self):
        to_draw = self.grid.copy()
        to_draw[self.position] = 3
        plt.clf()
        plt.imshow(to_draw.transpose())
        plt.draw()
        plt.pause(0.001)

    def move_direction(self, direction):
        x, y = self.position
        if direction == 4:
            x = x + 1
        elif direction == 3:
            x = x - 1
        elif direction == 1:
            y = y - 1
        elif direction == 2:
            y = y + 1
        else:
            raise ValueError('Invalid direction ' + str(direction))
        position = x, y
        return position


class MazeSolver:
    def __init__(self, filename):
        self.grid = np.load(filename)
        size = self.grid.shape[0]
        start_position = (size // 2 + 1, size // 2 + 1)
        self.grid[start_position] = 3

    def fill_water(self):
        steps = 0
        while True:
            steps = steps + 1
            try:
                self.water_step()
            except RuntimeError:
                return steps

    def fill_oxygen(self):
        steps = 0
        while (self.grid == 1).any():
            steps = steps + 1
            with contextlib.suppress(RuntimeError):
                self.water_step(2)
        return steps

    def water_step(self, water_index=3):
        filled = np.argwhere(self.grid == water_index)
        for point in filled:
            self.expand_from_point(point, water_index)
        plt.clf()
        plt.imshow(self.grid.transpose())
        plt.draw()
        plt.pause(0.01)

    def expand_from_point(self, point, water_index=3):
        x, y = point
        self.try_to_fill(x-1, y, water_index)
        self.try_to_fill(x+1, y, water_index)
        self.try_to_fill(x, y-1, water_index)
        self.try_to_fill(x, y+1, water_index)

    def try_to_fill(self, x, y, water_index=3):
        if self.grid[x, y] == 1:
            self.grid[x, y] = water_index
        # elif self.grid[x, y] == 2:
        #     raise RuntimeError('Found oxygen source')

class TestDroid(unittest.TestCase):

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

    def test_move_east(self):
        size = 8
        droid = RepairDroid(PROGRAM, size)
        droid.try_movement(4)
        expected_result = np.full((size, size), 2.0)
        expected_result[4, 3] = 0
        assert_array_equal(expected_result, droid.grid)

    def test_take_one_step(self):
        size = 8
        droid = RepairDroid(PROGRAM, size)
        try:
            droid.take_one_step()
        except Exception:
            plt.show()
            raise
        plt.show()

    def test_explore(self):
        size = 41
        droid = RepairDroid(PROGRAM, size)
        steps = droid.explore()
        self.assertEqual(229, steps)

class TestMazeSolver(unittest.TestCase):

    def test_one_water_step(self):
        solver = MazeSolver('maze.np.npy')
        # plt.imshow(solver.grid.transpose())
        # plt.show()
        solver.water_step()

    def test_fill_water(self):
        solver = MazeSolver('maze.np.npy')
        steps = solver.fill_water()
        self.assertEqual(300, steps)

    def test_fill_oxygen(self):
        solver = MazeSolver('maze.np.npy')
        steps = solver.fill_oxygen()
        self.assertEqual(312, steps)
        plt.show()

if __name__ == '__main__':
    unittest.main()

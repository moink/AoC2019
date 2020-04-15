import unittest
from collections import deque, MutableMapping
from itertools import permutations, cycle

BOOST_CODE = [1102, 34463338, 34463338, 63, 1007, 63, 34463338, 63, 1005, 63,
              53, 1101, 3, 0, 1000, 109, 988, 209, 12, 9, 1000, 209, 6, 209, 3,
              203, 0, 1008, 1000, 1, 63, 1005, 63, 65, 1008, 1000, 2, 63, 1005,
              63, 904, 1008, 1000, 0, 63, 1005, 63, 58, 4, 25, 104, 0, 99, 4, 0,
              104, 0, 99, 4, 17, 104, 0, 99, 0, 0, 1102, 1, 31, 1018, 1102, 352,
              1, 1023, 1101, 0, 1, 1021, 1101, 0, 33, 1003, 1102, 1, 36, 1007,
              1102, 21, 1, 1005, 1101, 359, 0, 1022, 1101, 0, 787, 1024, 1102,
              1, 24, 1011, 1101, 30, 0, 1014, 1101, 22, 0, 1016, 1101, 0, 0,
              1020, 1102, 1, 29, 1000, 1101, 778, 0, 1025, 1102, 23, 1, 1017,
              1102, 1, 28, 1002, 1101, 38, 0, 1019, 1102, 1, 27, 1013, 1102, 1,
              32, 1012, 1101, 0, 37, 1006, 1101, 444, 0, 1027, 1102, 1, 20,
              1009, 1101, 0, 447, 1026, 1101, 0, 39, 1008, 1101, 35, 0, 1010,
              1102, 559, 1, 1028, 1102, 26, 1, 1004, 1102, 1, 25, 1015, 1102, 1,
              34, 1001, 1101, 0, 554, 1029, 109, -3, 2101, 0, 9, 63, 1008, 63,
              34, 63, 1005, 63, 205, 1001, 64, 1, 64, 1105, 1, 207, 4, 187,
              1002, 64, 2, 64, 109, 23, 21107, 40, 39, -7, 1005, 1013, 227,
              1001, 64, 1, 64, 1106, 0, 229, 4, 213, 1002, 64, 2, 64, 109, -17,
              1202, -2, 1, 63, 1008, 63, 36, 63, 1005, 63, 249, 1106, 0, 255, 4,
              235, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, -6, 1202, 10, 1, 63,
              1008, 63, 36, 63, 1005, 63, 277, 4, 261, 1106, 0, 281, 1001, 64,
              1, 64, 1002, 64, 2, 64, 109, -2, 1208, 9, 26, 63, 1005, 63, 303,
              4, 287, 1001, 64, 1, 64, 1106, 0, 303, 1002, 64, 2, 64, 109, 32,
              1206, -7, 321, 4, 309, 1001, 64, 1, 64, 1106, 0, 321, 1002, 64, 2,
              64, 109, -29, 1207, 7, 20, 63, 1005, 63, 337, 1105, 1, 343, 4,
              327, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, 27, 2105, 1, -2, 1001,
              64, 1, 64, 1106, 0, 361, 4, 349, 1002, 64, 2, 64, 109, -25, 2108,
              39, 7, 63, 1005, 63, 377, 1106, 0, 383, 4, 367, 1001, 64, 1, 64,
              1002, 64, 2, 64, 109, 1, 1201, 6, 0, 63, 1008, 63, 36, 63, 1005,
              63, 409, 4, 389, 1001, 64, 1, 64, 1105, 1, 409, 1002, 64, 2, 64,
              109, 1, 2102, 1, 1, 63, 1008, 63, 33, 63, 1005, 63, 435, 4, 415,
              1001, 64, 1, 64, 1105, 1, 435, 1002, 64, 2, 64, 109, 28, 2106, 0,
              -3, 1106, 0, 453, 4, 441, 1001, 64, 1, 64, 1002, 64, 2, 64, 109,
              -13, 21101, 41, 0, 1, 1008, 1018, 44, 63, 1005, 63, 477, 1001, 64,
              1, 64, 1106, 0, 479, 4, 459, 1002, 64, 2, 64, 109, 4, 21108, 42,
              42, -2, 1005, 1019, 501, 4, 485, 1001, 64, 1, 64, 1106, 0, 501,
              1002, 64, 2, 64, 109, -21, 2101, 0, 2, 63, 1008, 63, 28, 63, 1005,
              63, 523, 4, 507, 1105, 1, 527, 1001, 64, 1, 64, 1002, 64, 2, 64,
              109, 26, 1205, -5, 545, 4, 533, 1001, 64, 1, 64, 1105, 1, 545,
              1002, 64, 2, 64, 109, 3, 2106, 0, -1, 4, 551, 1106, 0, 563, 1001,
              64, 1, 64, 1002, 64, 2, 64, 109, -33, 1201, 4, 0, 63, 1008, 63,
              28, 63, 1005, 63, 583, 1105, 1, 589, 4, 569, 1001, 64, 1, 64,
              1002, 64, 2, 64, 109, 11, 2107, 27, -3, 63, 1005, 63, 609, 1001,
              64, 1, 64, 1106, 0, 611, 4, 595, 1002, 64, 2, 64, 109, 8, 21102,
              43, 1, 3, 1008, 1018, 43, 63, 1005, 63, 637, 4, 617, 1001, 64, 1,
              64, 1105, 1, 637, 1002, 64, 2, 64, 109, -5, 21108, 44, 41, 0,
              1005, 1010, 653, 1105, 1, 659, 4, 643, 1001, 64, 1, 64, 1002, 64,
              2, 64, 109, -13, 2108, 21, 8, 63, 1005, 63, 681, 4, 665, 1001, 64,
              1, 64, 1106, 0, 681, 1002, 64, 2, 64, 109, 6, 1207, 0, 34, 63,
              1005, 63, 703, 4, 687, 1001, 64, 1, 64, 1105, 1, 703, 1002, 64, 2,
              64, 109, 7, 1208, -7, 35, 63, 1005, 63, 723, 1001, 64, 1, 64,
              1106, 0, 725, 4, 709, 1002, 64, 2, 64, 109, -13, 2102, 1, 7, 63,
              1008, 63, 23, 63, 1005, 63, 745, 1105, 1, 751, 4, 731, 1001, 64,
              1, 64, 1002, 64, 2, 64, 109, 13, 1205, 10, 767, 1001, 64, 1, 64,
              1105, 1, 769, 4, 757, 1002, 64, 2, 64, 109, 14, 2105, 1, 0, 4,
              775, 1001, 64, 1, 64, 1106, 0, 787, 1002, 64, 2, 64, 109, -20,
              21107, 45, 46, 7, 1005, 1011, 809, 4, 793, 1001, 64, 1, 64, 1105,
              1, 809, 1002, 64, 2, 64, 109, -3, 2107, 25, 3, 63, 1005, 63, 827,
              4, 815, 1106, 0, 831, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, 13,
              1206, 7, 847, 1001, 64, 1, 64, 1106, 0, 849, 4, 837, 1002, 64, 2,
              64, 109, -11, 21101, 46, 0, 7, 1008, 1010, 46, 63, 1005, 63, 871,
              4, 855, 1106, 0, 875, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, 15,
              21102, 47, 1, -4, 1008, 1014, 48, 63, 1005, 63, 895, 1106, 0, 901,
              4, 881, 1001, 64, 1, 64, 4, 64, 99, 21102, 27, 1, 1, 21101, 0,
              915, 0, 1106, 0, 922, 21201, 1, 63208, 1, 204, 1, 99, 109, 3,
              1207, -2, 3, 63, 1005, 63, 964, 21201, -2, -1, 1, 21102, 1, 942,
              0, 1106, 0, 922, 21202, 1, 1, -1, 21201, -2, -3, 1, 21101, 957, 0,
              0, 1105, 1, 922, 22201, 1, -1, -2, 1106, 0, 968, 21201, -2, 0, -2,
              109, -3, 2106, 0, 0]


class Memory(MutableMapping):

    def __init__(self, init_vals):
        self.contents = {i: val for i, val in enumerate(init_vals)}

    def __getitem__(self, item):
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
        if not isinstance(value, int):
            raise TypeError('Value must be an integer')
        self.contents[key] = value

    def __delitem__(self, key):
        del self.contents[key]


class Amplifier():

    def __init__(self, program):
        self.program = Memory(program)
        self.pointer = 0
        self.relative_base = 0

    def run_program(self, input_val):
        self.inputs = deque(input_val)
        outputs = []
        while self.program[self.pointer] != 99:
            op_code = self.program[self.pointer] % 100
            if op_code == 1:
                self.add()
            elif op_code == 2:
                self.multiply()
            elif op_code == 3:
                self.read_input()
            elif op_code == 4:
                self.generate_output(outputs)
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
        return outputs

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

    def generate_output(self, outputs):
        param_1 = self.prepare_get_param(1)
        outputs.append(param_1)
        self.pointer = self.pointer + 2

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

class TestAmplifiers(unittest.TestCase):

    def test_copy_program(self):
        program = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006,
                   101, 0, 99]
        output = Amplifier(program).run_program([])
        self.assertEqual(program, output)

    def test_sixteen_digit(self):
        program = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
        output = Amplifier(program).run_program([])[0]
        self.assertIsInstance(output, int)
        self.assertEqual(16, len(str(output)))

    def test_output_middle(self):
        program = [104, 1125899906842624, 99]
        output = Amplifier(program).run_program([])[0]
        self.assertEqual(1125899906842624, output)

    def test_right_answer(self):
        output = Amplifier(BOOST_CODE).run_program([1])[0]
        self.assertEqual(3507134798, output)

    def test_right_answer_part_two(self):
        output = Amplifier(BOOST_CODE).run_program([2])[0]
        self.assertEqual(84513, output)

    def run_get_mode_test(self, code, param_num, expected_mode):
        mode = Amplifier([code]).get_mode(param_num)
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


if __name__ == '__main__':
    unittest.main()

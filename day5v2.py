import unittest
from collections import deque

TEST_PROGRAM = [3, 225, 1, 225, 6, 6, 1100, 1, 238, 225, 104, 0, 1102, 27, 28,
                225, 1, 113, 14, 224, 1001, 224, -34, 224, 4, 224, 102, 8, 223,
                223, 101, 7, 224, 224, 1, 224, 223, 223, 1102, 52, 34, 224, 101,
                -1768, 224, 224, 4, 224, 1002, 223, 8, 223, 101, 6, 224, 224, 1,
                223, 224, 223, 1002, 187, 14, 224, 1001, 224, -126, 224, 4, 224,
                102, 8, 223, 223, 101, 2, 224, 224, 1, 224, 223, 223, 1102, 54,
                74, 225, 1101, 75, 66, 225, 101, 20, 161, 224, 101, -54, 224,
                224, 4, 224, 1002, 223, 8, 223, 1001, 224, 7, 224, 1, 224, 223,
                223, 1101, 6, 30, 225, 2, 88, 84, 224, 101, -4884, 224, 224, 4,
                224, 1002, 223, 8, 223, 101, 2, 224, 224, 1, 224, 223, 223,
                1001, 214, 55, 224, 1001, 224, -89, 224, 4, 224, 102, 8, 223,
                223, 1001, 224, 4, 224, 1, 224, 223, 223, 1101, 34, 69, 225,
                1101, 45, 67, 224, 101, -112, 224, 224, 4, 224, 102, 8, 223,
                223, 1001, 224, 2, 224, 1, 223, 224, 223, 1102, 9, 81, 225, 102,
                81, 218, 224, 101, -7290, 224, 224, 4, 224, 1002, 223, 8, 223,
                101, 5, 224, 224, 1, 223, 224, 223, 1101, 84, 34, 225, 1102, 94,
                90, 225, 4, 223, 99, 0, 0, 0, 677, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 1105, 0, 99999, 1105, 227, 247, 1105, 1, 99999, 1005, 227,
                99999, 1005, 0, 256, 1105, 1, 99999, 1106, 227, 99999, 1106, 0,
                265, 1105, 1, 99999, 1006, 0, 99999, 1006, 227, 274, 1105, 1,
                99999, 1105, 1, 280, 1105, 1, 99999, 1, 225, 225, 225, 1101,
                294, 0, 0, 105, 1, 0, 1105, 1, 99999, 1106, 0, 300, 1105, 1,
                99999, 1, 225, 225, 225, 1101, 314, 0, 0, 106, 0, 0, 1105, 1,
                99999, 1007, 677, 677, 224, 102, 2, 223, 223, 1005, 224, 329,
                101, 1, 223, 223, 1108, 226, 677, 224, 1002, 223, 2, 223, 1005,
                224, 344, 101, 1, 223, 223, 1008, 677, 677, 224, 102, 2, 223,
                223, 1005, 224, 359, 101, 1, 223, 223, 8, 226, 677, 224, 1002,
                223, 2, 223, 1006, 224, 374, 101, 1, 223, 223, 108, 226, 677,
                224, 1002, 223, 2, 223, 1006, 224, 389, 1001, 223, 1, 223, 1107,
                226, 677, 224, 102, 2, 223, 223, 1005, 224, 404, 1001, 223, 1,
                223, 7, 226, 677, 224, 1002, 223, 2, 223, 1005, 224, 419, 101,
                1, 223, 223, 1107, 677, 226, 224, 102, 2, 223, 223, 1006, 224,
                434, 1001, 223, 1, 223, 1107, 226, 226, 224, 1002, 223, 2, 223,
                1006, 224, 449, 101, 1, 223, 223, 1108, 226, 226, 224, 1002,
                223, 2, 223, 1005, 224, 464, 101, 1, 223, 223, 8, 677, 226, 224,
                102, 2, 223, 223, 1005, 224, 479, 101, 1, 223, 223, 8, 226, 226,
                224, 1002, 223, 2, 223, 1006, 224, 494, 1001, 223, 1, 223, 1007,
                226, 677, 224, 1002, 223, 2, 223, 1006, 224, 509, 1001, 223, 1,
                223, 108, 226, 226, 224, 1002, 223, 2, 223, 1006, 224, 524,
                1001, 223, 1, 223, 1108, 677, 226, 224, 102, 2, 223, 223, 1006,
                224, 539, 101, 1, 223, 223, 1008, 677, 226, 224, 102, 2, 223,
                223, 1006, 224, 554, 101, 1, 223, 223, 107, 226, 677, 224, 1002,
                223, 2, 223, 1006, 224, 569, 101, 1, 223, 223, 107, 677, 677,
                224, 102, 2, 223, 223, 1006, 224, 584, 101, 1, 223, 223, 7, 677,
                226, 224, 102, 2, 223, 223, 1005, 224, 599, 101, 1, 223, 223,
                1008, 226, 226, 224, 1002, 223, 2, 223, 1005, 224, 614, 1001,
                223, 1, 223, 107, 226, 226, 224, 1002, 223, 2, 223, 1005, 224,
                629, 101, 1, 223, 223, 7, 226, 226, 224, 102, 2, 223, 223, 1006,
                224, 644, 1001, 223, 1, 223, 1007, 226, 226, 224, 102, 2, 223,
                223, 1006, 224, 659, 101, 1, 223, 223, 108, 677, 677, 224, 102,
                2, 223, 223, 1005, 224, 674, 1001, 223, 1, 223, 4, 223, 99, 226]

def run_program(program, input_list):
    pointer = 0
    output = []
    input_list = deque(input_list)
    while program[pointer] != 99:
        op_code = program[pointer] % 100
        if op_code == 1: # addition
            param_1, param_2 = prepare_two_parameters(pointer, program)
            program[program[pointer + 3]] = param_1 + param_2
            pointer = pointer + 4
        elif op_code == 2: # multiplication
            param_1, param_2 = prepare_two_parameters(pointer, program)
            program[program[pointer + 3]] = param_1 * param_2
            pointer = pointer + 4
        elif op_code == 3: #input
            program[program[pointer + 1]] = input_list.popleft()
            pointer = pointer + 2
        elif op_code == 4: # output
            param_1 = extract_one_param(pointer, program)
            output.append(param_1)
            pointer = pointer + 2
        elif op_code == 5: # jump-if-true
            param_1, param_2 = prepare_two_parameters(pointer, program)
            if param_1:
                pointer = param_2
            else:
                pointer = pointer + 3
        elif op_code == 6: # jump-if-false
            param_1, param_2 = prepare_two_parameters(pointer, program)
            if not(param_1):
                pointer = param_2
            else:
                pointer = pointer + 3
        elif op_code == 7: # less than
            param_1, param_2 = prepare_two_parameters(pointer, program)
            program[program[pointer + 3]] = int(param_1 < param_2)
            pointer = pointer + 4
        elif op_code == 8: # equal
            param_1, param_2 = prepare_two_parameters(pointer, program)
            program[program[pointer + 3]] = int(param_1 == param_2)
            pointer = pointer + 4
        else:
            raise ValueError('No such operation ' + str(op_code))
    return output, program


def extract_one_param(pointer, program):
    mode_param_1 = (program[pointer] // 100) % 10
    if mode_param_1:
        param_1 = program[pointer + 1]
    else:
        param_1 = program[program[pointer + 1]]
    return param_1


def prepare_two_parameters(pointer, program):
    mode_param_1 = (program[pointer] // 100) % 10
    mode_param_2 = (program[pointer] // 1000) % 100
    if mode_param_1:
        param_1 = program[pointer + 1]
    else:
        param_1 = program[program[pointer + 1]]
    if mode_param_2:
        param_2 = program[pointer + 2]
    else:
        param_2 = program[program[pointer + 2]]
    return param_1, param_2


class TestIntCode(unittest.TestCase):

    def test_run_program_input_output(self):
        program = [3, 0, 4, 0, 99]
        input = 14
        expected = [14]
        result, _ = run_program(program, [input])
        self.assertEqual(expected, result)

    def test_run_test_program(self):
        program = TEST_PROGRAM
        input = [1]
        expected = [0, 0, 0, 0, 0, 0, 0, 0, 0, 16348437]
        result, _ = run_program(program, input)
        self.assertEqual(expected, result)

    def run_calc_int_code_test(self, input, output):
        _, result = run_program(input, [])
        self.assertEqual(output, result)

    def test_calc_int_code(self):
        self.run_calc_int_code_test([1, 0, 0, 0, 99], [2, 0, 0, 0, 99])
        self.run_calc_int_code_test([2, 3, 0, 3, 99], [2, 3, 0, 6, 99])
        self.run_calc_int_code_test([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801])
        self.run_calc_int_code_test([1, 1, 1, 4, 99, 5, 6, 0, 99],
                                    [30, 1, 1, 4, 2, 5, 6, 0, 99])

    def run_equal_to_eight_test(self, program):
        result, _ = run_program(program, [4])
        self.assertEqual([0], result)
        result, _ = run_program(program, [8])
        self.assertEqual([1], result)

    def test_equal_to_eight(self):
        self.run_equal_to_eight_test([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8])
        self.run_equal_to_eight_test([3, 3, 1108, -1, 8, 3, 4, 3, 99])

    def run_less_than_eight_test(self, program):
        result, _ = run_program(program, [4])
        self.assertEqual([1], result)
        result, _ = run_program(program, [9])
        self.assertEqual([0], result)

    def test_less_than_eight(self):
        self.run_less_than_eight_test([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8])
        self.run_less_than_eight_test([3, 3, 1107, -1, 8, 3, 4, 3, 99])

    def test_long_eight_program(self):
        prog = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006,
                20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20,
                1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20,
                1105, 1, 46, 98, 99]
        # result, _ = run_program(prog, [4])
        # self.assertEqual([999], result)
        # result, _ = run_program(prog, [8])
        # self.assertEqual([1000], result)
        result,_ = run_program(prog, [13])
        self.assertEqual([1001], result)

    def test_run_test_program_part_two(self):
        program = TEST_PROGRAM
        input = [5]
        expected = [6959377]
        result, program = run_program(program, input)
        print(max(program))
        self.assertEqual(expected, result)

if __name__ == '__main__':
    unittest.main()

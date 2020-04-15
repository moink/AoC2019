import unittest
from collections import deque

OPERATIONS = {1: 'add', 2: 'multiply', 3: 'input', 4: 'output',
              5: 'jump-if-true', 6:'jump-if-false', 7: 'less than',
              8: 'equals'}
NUMBER_OF_PARAMETERS = {'add': 3, 'multiply': 3, 'input': 1, 'output': 1,
                        'jump-if-true': 2, 'jump-if-false': 2, 'less than': 3,
                        'equals': 3}
PARAM_MODES = {0: 'position', 1: 'immediate'}
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


def run_program(program, inputs):
    i = 0
    inputs = deque(inputs)
    outputs = []
    while i < len(program) and program[i] != 99:
        operation, param_mode = interpret_op_code(program[i])
        num_params = len(param_mode)
        params = get_params(program[i + 1:i + num_params + 1], param_mode,
                            program)
        output, program, inputs, jump_to = apply_operation(
            operation, params, program, inputs)
        if output is not None:
            outputs.append(output)
        if jump_to is not None:
            i = jump_to
        else:
            i = i + num_params + 1
    return outputs, program


def apply_operation(oper, params, program, inputs):
    output = None
    jump_to = None
    if oper == 'add':
        program[params[2]] = params[0] + params[1]
    elif oper == 'multiply':
        program[params[2]] = params[0] * params[1]
    elif oper == 'input':
        program[params[0]] = inputs.popleft()
    elif oper == 'output':
        output = params[0]
    elif oper == 'jump-if-true':
        if params[0]:
            jump_to = params[1]
    elif oper == 'jump-if-false':
        if not(params[0]):
            jump_to = params[1]
    elif oper == 'less than':
        program[params[2]] = int(params[0] < params[1])
    elif oper == 'equals':
        program[params[2]] = int(params[0] == params[1])
    return output, program, inputs, jump_to


def get_params(param_codes, param_modes, program):
    results = []
    for code, mode in zip(param_codes, param_modes):
        if mode == 'position':
            result = program[code]
        else:  # immediate mode
            result = code
        results.append(result)
    return results


def interpret_op_code(code):
    code_str = str(code)
    op_code = int(code_str[-2:])
    operation = OPERATIONS[op_code]
    num_params = NUMBER_OF_PARAMETERS[operation]
    mode_part = code_str[-3::-1]
    if mode_part:
        param_modes = [PARAM_MODES[int(char)] for char in mode_part]
    else:
        param_modes = []
    for i in range(len(param_modes), num_params):
        param_modes.append(PARAM_MODES[0])
    if operation != 'output' or not(param_modes):
        param_modes[-1] = PARAM_MODES[1]
    return operation, param_modes


class TestIntCode(unittest.TestCase):

    def test_interpret_op_code(self):
        operation, param_modes = interpret_op_code(1002)
        self.assertEqual('multiply', operation)
        self.assertEqual(['position', 'immediate', 'immediate'], param_modes)

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
        expected = [16348437]
        result, program = run_program(program, input)
        print(max(program))
        self.assertEqual(expected, result)

if __name__ == '__main__':
    unittest.main()

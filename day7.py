import unittest
from collections import deque
from itertools import permutations, cycle

TEST_PROGRAM = [
    3, 8, 1001, 8, 10, 8, 105, 1, 0, 0, 21, 42, 63, 76, 101, 114, 195, 276,
    357, 438, 99999, 3, 9, 101, 2, 9, 9, 102, 5, 9, 9, 1001, 9, 3, 9, 1002,
    9, 5, 9, 4, 9, 99, 3, 9, 101, 4, 9, 9, 102, 5, 9, 9, 1001, 9, 5, 9, 102,
    2, 9, 9, 4, 9, 99, 3, 9, 1001, 9, 3, 9, 1002, 9, 5, 9, 4, 9, 99, 3, 9,
    1002, 9, 2, 9, 101, 5, 9, 9, 102, 3, 9, 9, 101, 2, 9, 9, 1002, 9, 3, 9, 4,
    9, 99, 3, 9, 101, 3, 9, 9, 102, 2, 9, 9, 4, 9, 99, 3, 9, 1001, 9, 2, 9,
    4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 102, 2,
    9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9,
    1001, 9, 1, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4,
    9, 3, 9, 1001, 9, 1, 9, 4, 9, 99, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1001,
    9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9,
    1001, 9, 1, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9,
    3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9,
    4, 9, 99, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1002, 9,
    2, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9,
    1001, 9, 1, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4,
    9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 99, 3, 9, 1001,
    9, 1, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9,
    1001, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9,
    3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9,
    4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 99, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101,
    1, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3,
    9, 1002, 9, 2, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4,
    9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 101, 2, 9,
    9, 4, 9, 99]


class Amplifier():

    def __init__(self, program, phase):
        self.program = list(program)
        self.pointer = 0
        self.inputs = deque([phase])

    def run_program(self, input_val):
        self.inputs.append(input_val)
        while self.program[self.pointer] != 99:
            op_code = self.program[self.pointer] % 100
            if op_code == 1:  # addition
                param_1, param_2 = self.prepare_two_parameters()
                self.program[self.program[self.pointer + 3]] = param_1 + param_2
                self.pointer = self.pointer + 4
            elif op_code == 2:  # multiplication
                param_1, param_2 = self.prepare_two_parameters()
                self.program[self.program[self.pointer + 3]] = param_1 * param_2
                self.pointer = self.pointer + 4
            elif op_code == 3:  # input
                self.program[
                    self.program[self.pointer + 1]] = self.inputs.popleft()
                self.pointer = self.pointer + 2
            elif op_code == 4:  # output
                param_1 = self.extract_one_param()
                self.pointer = self.pointer + 2
                return param_1
            elif op_code == 5:  # jump-if-true
                param_1, param_2 = self.prepare_two_parameters()
                if param_1:
                    self.pointer = param_2
                else:
                    self.pointer = self.pointer + 3
            elif op_code == 6:  # jump-if-false
                param_1, param_2 = self.prepare_two_parameters()
                if not (param_1):
                    self.pointer = param_2
                else:
                    self.pointer = self.pointer + 3
            elif op_code == 7:  # less than
                param_1, param_2 = self.prepare_two_parameters()
                self.program[self.program[self.pointer + 3]] = int(
                    param_1 < param_2)
                self.pointer = self.pointer + 4
            elif op_code == 8:  # equal
                param_1, param_2 = self.prepare_two_parameters()
                self.program[self.program[self.pointer + 3]] = int(
                    param_1 == param_2)
                self.pointer = self.pointer + 4
            else:
                raise ValueError('No such operation ' + str(op_code))
        return None

    def extract_one_param(self):
        mode_param_1 = (self.program[self.pointer] // 100) % 10
        if mode_param_1:
            param_1 = self.program[self.pointer + 1]
        else:
            param_1 = self.program[self.program[self.pointer + 1]]
        return param_1

    def prepare_two_parameters(self):
        mode_param_1 = (self.program[self.pointer] // 100) % 10
        mode_param_2 = (self.program[self.pointer] // 1000) % 100
        if mode_param_1:
            param_1 = self.program[self.pointer + 1]
        else:
            param_1 = self.program[self.program[self.pointer + 1]]
        if mode_param_2:
            param_2 = self.program[self.pointer + 2]
        else:
            param_2 = self.program[self.program[self.pointer + 2]]
        return param_1, param_2


def run_feedback_loop(program, signal):
    amps = [Amplifier(program, phase) for phase in signal]
    result = 0
    for amp in cycle(amps):
        old_result = result
        result = amp.run_program(result)
        if result is None:
            break
    return old_result


def run_amplifier_sequence(program, signal):
    result = 0
    for phase in signal:
        amp = Amplifier(program, phase)
        result = amp.run_program(result)
    return result


def optimize_amplifier_sequence(program, num_amplifiers):
    signals = permutations(range(num_amplifiers))
    thrusts = {run_amplifier_sequence(program, signal): signal
               for signal in signals}
    highest_thrust = max(thrusts.keys())
    best_signal = thrusts[highest_thrust]
    return highest_thrust


def optimize_feedback_loop(program, num_amplifiers):
    signals = permutations(range(5, 5 + num_amplifiers))
    thrusts = {run_feedback_loop(program, signal): signal
               for signal in signals}
    highest_thrust = max(thrusts.keys())
    best_signal = thrusts[highest_thrust]
    return highest_thrust, best_signal


class TestAmplifiers(unittest.TestCase):
    def test_run_amplifier_sequence(self):
        program = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0,
                   0]
        signal = [4, 3, 2, 1, 0]
        thrust = run_amplifier_sequence(program, signal)
        self.assertEqual(43210, thrust)

    def run_optimize_test(self, program, num_amplifiers, expected):
        signal = optimize_amplifier_sequence(program, num_amplifiers)
        self.assertEqual(expected, signal)

    def test_optimize_amplifier_sequence1(self):
        program = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0,
                   0]
        expected = 43210
        self.run_optimize_test(program, 5, expected)

    def test_optimize_amplifier_sequence2(self):
        program = [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23,
                   101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0]
        expected = 54321
        self.run_optimize_test(program, 5, expected)

    def test_optimize_amplifier_sequence3(self):
        program = [3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31,
                   0, 33, 1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4,
                   31, 99, 0, 0, 0]
        expected = 65210
        self.run_optimize_test(program, 5, expected)

    def test_result_part_one(self):
        program = TEST_PROGRAM
        expected = 255590
        self.run_optimize_test(program, 5, expected)

    def test_run_feedback_loop(self):
        program = [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26,
                   27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5]
        signal = [9, 8, 7, 6, 5]
        thrust = run_feedback_loop(program, signal)
        self.assertEqual(139629729, thrust)

    def test_optimize_feedback_loop(self):
        program = [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26,
                   27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5]
        thrust, signal = optimize_feedback_loop(program, 5)
        self.assertEqual((9, 8, 7, 6, 5), signal)
        self.assertEqual(139629729, thrust)

    def test_optimize_feedback_loop2(self):
        program = [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5,
                   55, 1005, 55, 26, 1001, 54, -5, 54, 1105, 1, 12, 1, 53,
                   54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4,
                   53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10]
        thrust, signal = optimize_feedback_loop(program, 5)
        self.assertEqual((9,7,8,5,6), signal)
        self.assertEqual(18216, thrust)

    def test_right_answer_part_two(self):
        program = TEST_PROGRAM
        thrust, signal = optimize_feedback_loop(program, 5)
        self.assertEqual(58285150, thrust)


if __name__ == '__main__':
    unittest.main()

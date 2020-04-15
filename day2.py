import itertools
import unittest

INITIAL_MEMORY = [1, 0, 0, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 10, 1, 19,
                  1, 5, 19, 23, 1, 23, 5, 27, 1, 27, 13, 31, 1, 31, 5, 35, 1, 9,
                  35, 39, 2, 13, 39, 43, 1, 43, 10, 47, 1, 47, 13, 51, 2, 10,
                  51, 55, 1, 55, 5, 59, 1, 59, 5, 63, 1, 63, 13, 67, 1, 13, 67,
                  71, 1, 71, 10, 75, 1, 6, 75, 79, 1, 6, 79, 83, 2, 10, 83, 87,
                  1, 87, 5, 91, 1, 5, 91, 95, 2, 95, 10, 99, 1, 9, 99, 103, 1,
                  103, 13, 107, 2, 10, 107, 111, 2, 13, 111, 115, 1, 6, 115,
                  119, 1, 119, 10, 123, 2, 9, 123, 127, 2, 127, 9, 131, 1, 131,
                  10, 135, 1, 135, 2, 139, 1, 10, 139, 0, 99, 2, 0, 14, 0]


def calc_int_code(values):
    i = 0
    while values[i] != 99:
        result = calculate_result(values[i], values[values[i + 1]],
                                  values[values[i + 2]])
        values[values[i + 3]] = result
        i = i + 4
    return values


def calculate_result(oper, arg1, arg2):
    if oper == 1:  # addition
        result = arg1 + arg2
    elif oper == 2:  # multiplication
        result = arg1 * arg2
    else:
        raise RuntimeError('No operator with code ' + str(oper))
    return result


def run_program(noun, verb):
    memory = INITIAL_MEMORY.copy()
    memory[1] = noun
    memory[2] = verb
    values = calc_int_code(memory)
    return values[0]


def grid_search(right_answer):
    for noun, verb in itertools.product(range(100), range(100)):
        answer = run_program(noun, verb)
        if answer == right_answer:
            return noun, verb
    raise RuntimeError('No right answer')


class TestIntcode(unittest.TestCase):

    def run_calc_int_code_test(self, input, output):
        result = calc_int_code(input)
        self.assertEqual(output, result)

    def test_calc_int_code(self):
        self.run_calc_int_code_test([1, 0, 0, 0, 99], [2, 0, 0, 0, 99])
        self.run_calc_int_code_test([2, 3, 0, 3, 99], [2, 3, 0, 6, 99])
        self.run_calc_int_code_test([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801])
        self.run_calc_int_code_test([1, 1, 1, 4, 99, 5, 6, 0, 99],
                                    [30, 1, 1, 4, 2, 5, 6, 0, 99])

    def test_overall_result(self):
        input = INITIAL_MEMORY.copy()
        input[1] = 12
        input[2] = 2
        output = calc_int_code(input)
        result = output[0]
        self.assertEqual(3562624, result)

    def test_run_program(self):
        noun = 12
        verb = 2
        output = run_program(noun, verb)
        self.assertEqual(3562624, output)

    def test_right_answer(self):
        noun = 82
        verb = 98
        output = run_program(noun, verb)
        self.assertEqual(19690720, output)

    def test_grid_search(self):
        noun, verb = grid_search(19690720)
        print(noun)
        print(verb)


if __name__ == '__main__':
    unittest.main()

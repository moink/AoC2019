import unittest
from collections import MutableMapping, Mapping
from functools import partial, lru_cache
from itertools import cycle, chain, repeat
from operator import gt

import numpy as np
from numpy.testing import assert_array_equal

BASE_PATTERN = [0, 1, 0, -1]


@lru_cache(maxsize=None)
def sets_in_pattern(number, length):
    ones = [x for n in range(number, length, 4 * (number + 1))
            for x in range(n, min(length, n + number + 1))]
    minus = [x for n in range(3*number+2, length, 4 * (number + 1))
             for x in range(n, min(length, n + number + 1))]
    return ones, minus


def run_n_phases_optimized(signal, phases, digits, multiplier):
    full_signal = to_mapper(signal, multiplier)
    result = [calc_one_digit_optimized(full_signal, phases, digit)
              for digit in digits]
    # result = ''.join(str(calc_one_digit_optimized(full_signal, phases, digit))
    #                  for digit in digits)
    return result


def to_mapper(signal, multiplier):
    class mapper(Mapping):
        def __init__(self, signal):
            self.contents = signal
        def __getitem__(self, item):
            return int(self.contents[item % len(self.contents)])
        def __len__(self):
            return multiplier * len(self.contents)
        def __iter__(self):
            return repeat(self.contents, multiplier)
        def __hash__(self):
            return hash(self.contents)
    return mapper(signal)


@lru_cache(maxsize=4096)
def calc_one_digit_optimized(init_signal, phases, digit):
    if phases == 0:
        return init_signal[digit]
    ones, minus = sets_in_pattern(digit, len(init_signal))
    to_add = calc_to_add(init_signal, ones, phases)
    to_sub = calc_to_add(init_signal, minus, phases)
    return abs(to_add - to_sub) % 10


# @lru_cache(maxsize=4096)
def calc_to_add(init_signal, ones, phases):
    amount = 0
    for n in ones:
        amount = (amount + calc_one_digit_optimized(init_signal, phases - 1, n))
    return amount


# @lru_cache(maxsize=4096)
def sum_gen(gen_exp):
    to_add = sum(gen_exp)
    return to_add


class TestFftReader(unittest.TestCase):

    def test_create_pattern(self):
        pattern = create_pattern(0, 8)
        expected = [1, 0, -1, 0, 1, 0, -1, 0]
        self.assertEqual(expected, pattern)
        pattern = create_pattern(1, 8)
        expected = [0, 1, 1, 0, 0, -1, -1, 0]
        self.assertEqual(expected, pattern)
        pattern = create_pattern(7, 8)
        expected = [0, 0, 0, 0, 0, 0, 0, 1]
        self.assertEqual(expected, pattern)

    def test_ones_in_pattern(self):
        self.run_sets_test(0, 8, [0, 4], [2, 6])
        self.run_sets_test(1, 8, [1, 2], [5, 6])
        self.run_sets_test(7, 8, [7], [])
        self.run_sets_test(523, 1000, range(523, 1000), [])
        self.run_sets_test(
            114, 1000, chain.from_iterable([range(114, 229), range(574, 689)]),
            chain.from_iterable([range(344, 459), range(804, 919)]))
        self.run_sets_test(
            10, 1000, chain.from_iterable(
                [range(n, n+11) for n in range(10, 1000, 44)]),
            chain.from_iterable(
                [range(n, n+11) for n in range(32, 1000, 44)]))

    def run_sets_test(self, number, length, expected_ones, expected_minus):
        ones, minus_ones = sets_in_pattern(number, length)
        try:
            assert_array_equal(np.asarray(expected_ones), ones, verbose=True)
        except AssertionError:
            self.assertEqual(set(expected_ones), set(ones))
        try:
            assert_array_equal(np.asarray(expected_minus), minus_ones)
        except AssertionError:
            self.assertEqual(set(expected_minus), set(minus_ones))

    def test_calc_one_digit(self):
        signal = 12345678
        sig_list = to_int_list(signal)
        digit = calc_one_digit(sig_list, 0)
        self.assertEqual(4, digit)
        digit = calc_one_digit(sig_list, 2)
        self.assertEqual(2, digit)
        digit = calc_one_digit(sig_list, 7)
        self.assertEqual(8, digit)

    def test_calc_one_digit_optimized(self):
        signal = '12345678'
        sig_list = to_int_list(signal)
        digit = calc_one_digit_optimized(signal, 1, 0)
        self.assertEqual(4, digit)
        digit = calc_one_digit_optimized(signal, 1, 2)
        self.assertEqual(2, digit)
        digit = calc_one_digit_optimized(signal, 1, 7)
        self.assertEqual(8, digit)

    def test_run_one_phase(self):
        signal = 12345678
        sig_list = to_int_list(signal)
        result = run_one_phase(sig_list)
        expected = to_int_list(48226158)
        self.assertEqual(expected, result)

    def test_run_n_phases(self):
        signal = 12345678
        result = run_n_phases(signal, 4)
        self.assertEqual('01029498', result)

    def test_run_100_phases(self):
        self.run_100_phases_test('80871224585914546619083218645595', '24176176')
        self.run_100_phases_test('19617804207202209144916044189917', '73745418')
        self.run_100_phases_test('69317163492948606335995924319873', '52432133')

    def test_run_100_phases_faster(self):
        signal = '80871224585914546619083218645595'
        result = run_n_phases_optimized(signal, 100, [4], 20)
        self.assertEqual('2', result)

    def run_100_phases_test(self, signal, expected):
        result = run_n_phases_optimized(signal, 100, range(8), 1)
        self.assertEqual(expected, result)

    def test_answer_part_1(self):
        with open('day16_input.txt') as infile:
            signal = infile.read()
        expected = '67481260'
        self.run_100_phases_test(signal, expected)

    def test_answer_part_2(self):
        with open('day16_input.txt') as infile:
            part_signal = infile.read()
        startnum = int(part_signal[0:7])
        result = run_n_phases_optimized(part_signal, 100,
                                        range(startnum, startnum+8), 10000)
        expected = '67481260'
        self.assertEqual(expected, result)

if __name__ == '__main__':
    unittest.main()

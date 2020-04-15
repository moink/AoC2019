import unittest
import numpy as np
from numpy.testing import assert_array_equal
import scipy.signal

TEST_INPUT = """
....#
#..#.
#..##
..#..
#...."""

REAL_DATA = """
#.##.
###.#
#...#
##..#
.#..."""

CONVOLVE_MATRIX = np.asarray([[0, 1, 0], [1, 0, 1], [0, 1, 0]])

def read_input(string_input):
    rows = [row.strip() for row in string_input.splitlines() if row]
    num_rows = len(rows)
    num_cols = len(rows[0])
    result = np.zeros((num_rows, num_cols), dtype=int)
    for row_num, row in enumerate(rows):
        for col_num, char in enumerate(row):
            if char == '#':
                result[row_num, col_num] = 1
            else:
                result[row_num, col_num] = 0
    return result


def count_neighbours(state):
    result = scipy.signal.convolve2d(state, CONVOLVE_MATRIX, mode='same')
    return result


def one_step(state):
    counts = count_neighbours(state)
    result = np.where(np.logical_and(state == 1, counts != 1), 0, state)
    result = np.where(np.logical_and(state == 0,
                                     np.logical_or(counts == 1, counts == 2)),
                      1, result)
    return result


def biodiversity(state):
    power2 = np.power(2, np.reshape(range(state.size), state.shape))
    return np.sum(power2 * state)


def appears_twice(state):
    past_biodiversity = set()
    while True:
        state = one_step(state)
        bio_d = biodiversity(state)
        if bio_d in past_biodiversity:
            return bio_d
        past_biodiversity.add(bio_d)

class TestBugSimulation(unittest.TestCase):

    def test_read_input(self):
        expected_result = np.asarray([
            [0, 0, 0, 0, 1],
            [1, 0, 0, 1, 0],
            [1, 0, 0, 1, 1],
            [0, 0, 1, 0, 0],
            [1, 0, 0, 0, 0]])
        result = read_input(TEST_INPUT)
        assert_array_equal(expected_result, result)

    def test_one_step(self):
        start_state = read_input(TEST_INPUT)
        expected = read_input("""
            #..#.
            ####.
            ###.#
            ##.##
            .##..""")
        result = one_step(start_state)
        assert_array_equal(expected, result)

    def test_four_steps(self):
        state = read_input(TEST_INPUT)
        expected = read_input("""
            ####.
            ....#
            ##..#
            .....
            ##...""")
        for _ in range(4):
            state = one_step(state)
        assert_array_equal(expected, state)

    def test_biodiversity(self):
        state= read_input("""
            .....
            .....
            .....
            #....
            .#...""")
        result = biodiversity(state)
        self.assertEqual(2129920, result)

    def test_appears_twice(self):
        state = read_input(TEST_INPUT)
        result = appears_twice(state)
        self.assertEqual(2129920, result)

    def test_part_one(self):
        state = read_input(REAL_DATA)
        result = appears_twice(state)
        self.assertEqual(32505887, result)


if __name__ == '__main__':
    unittest.main()

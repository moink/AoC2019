import contextlib
import unittest
import numpy as np
from numpy.testing import assert_array_equal

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


def read_input(string_input, num_steps):
    rows = [row.strip() for row in string_input.splitlines() if row]
    num_rows = len(rows)
    num_cols = len(rows[0])
    result = np.zeros((2 * num_steps, num_rows, num_cols), dtype=int)
    for row_num, row in enumerate(rows):
        for col_num, char in enumerate(row):
            if char == '#':
                result[num_steps, row_num, col_num] = 1
            else:
                result[num_steps, row_num, col_num] = 0
    return result


def count_neighbours(state):
    count = np.zeros_like(state)
    num_levels, num_rows, num_cols = state.shape
    for level in range(num_levels):
        for row in range(num_rows):
            for col in range(num_cols):
                neighbours = list_neighbours((level, row, col))
                for cell in neighbours:
                    with contextlib.suppress(IndexError):
                        count[level, row, col] = (count[level, row, col]
                                                  + state[cell])
    return count


def one_step(state):
    counts = count_neighbours(state)
    result = np.where(np.logical_and(state == 1, counts != 1), 0, state)
    result = np.where(np.logical_and(state == 0,
                                     np.logical_or(counts == 1, counts == 2)),
                      1, result)
    result [:, 2, 2] = 0
    return result


def list_neighbours(cell):
    level, row, col = cell
    result = []
    deltas = ((0, 1), (0, -1), (1, 0), (-1, 0))
    for delta_row, delta_col in deltas:
        new_row = row + delta_row
        new_col = col + delta_col
        if new_row == 2 and new_col == 2:
            if row == 1 and col == 2:
                result.extend([
                    (level + 1, 0, 0), (level + 1, 0, 1), (level + 1, 0, 2),
                    (level + 1, 0, 3), (level + 1, 0, 4)])
            elif row == 2 and col == 1:
                result.extend([
                    (level + 1, 0, 0), (level + 1, 1, 0), (level + 1, 2, 0),
                    (level + 1, 3, 0), (level + 1, 4, 0)])
            elif row == 3 and col == 2:
                result.extend([
                    (level + 1, 4, 0), (level + 1, 4, 1), (level + 1, 4, 2),
                    (level + 1, 4, 3), (level + 1, 4, 4)])
            else: # row == 2 and col == 3:
                result.extend([
                    (level + 1, 0, 4), (level + 1, 1, 4), (level + 1, 2, 4),
                    (level + 1, 3, 4), (level + 1, 4, 4)])
        elif new_row < 0:
            result.append((level - 1, 1, 2))
        elif new_col < 0:
            result.append((level - 1, 2, 1))
        elif new_row > 4:
            result.append((level - 1, 3, 2))
        elif new_col > 4:
            result.append((level - 1, 2, 3))
        else:
            result.append((level, new_row, new_col))

    return result


class TestBugSimulation(unittest.TestCase):

    def test_read_input(self):
        expected_result = np.asarray([
            [0, 0, 0, 0, 1],
            [1, 0, 0, 1, 0],
            [1, 0, 0, 1, 1],
            [0, 0, 1, 0, 0],
            [1, 0, 0, 0, 0]])
        result = read_input(TEST_INPUT, 200)
        shape = result.shape
        self.assertEqual((400, 5, 5), shape)
        assert_array_equal(expected_result, result[200])

    def test_list_neighbours(self):
        result = list_neighbours((0, 2, 3))
        expected_result = [(0, 1, 3), (1, 0, 4), (1, 1, 4), (1, 2, 4),
                           (1, 3, 4), (1, 4, 4), (0, 2, 4), (0, 3, 3)]
        self.assertEqual(set(expected_result), set(result))

    def test_ten_steps(self):
        state = read_input(TEST_INPUT, 200)
        expected = read_input("""
            .#...
            .#.##
            .#...
            .....
            .....""", 200)
        for _ in range(10):
            state = one_step(state)
        assert_array_equal(expected[200], state[200])

    def test_part_two(self):
        num_steps = 200
        state = read_input(REAL_DATA, num_steps)
        for _ in range(num_steps):
            state = one_step(state)
        result = np.sum(state)
        self.assertEqual(1980, result)


if __name__ == '__main__':
    unittest.main()

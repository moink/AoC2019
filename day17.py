import contextlib
import unittest
from day15 import Computer
from functools import partial

def run_ascii(program):
    computer = Computer(program)
    return ''.join(chr(code) for code in computer.run_program())


def is_scaff(scaff_map, position):
    row_num, col_num = position
    result = False
    with contextlib.suppress(IndexError):
        if scaff_map[row_num][col_num] == '#':
            result = True
    return result

def find_intersections(scaff_map):
    scaff_map = [row.strip() for row in scaff_map.splitlines() if row]
    result = []
    for row_num, row in enumerate(scaff_map, start=1):
        for col_num, char in enumerate(row, start=1):
            to_check = [(row_num, col_num), (row_num - 1, col_num),
                        (row_num + 1, col_num), (row_num, col_num - 1),
                        (row_num, col_num + 1 )]
            if all(map(partial(is_scaff, scaff_map), to_check)):
                result.append((col_num, row_num))
    return result

def get_alignment_sum(scaff_map):
    intersections = find_intersections(scaff_map)
    return sum(row * col for row, col in intersections)


def follow_path(first_seq, A, B, C, video):
    asc = '\n'.join((first_seq, A, B, C, video)) + '\n'
    inputs = [ord(char) for char in asc]
    with open('day17input.txt') as infile:
        program = list(map(int, infile.read().split(',')))
    program[0] = 2
    computer = Computer(program)
    computer.set_input(inputs)
    return ''.join(chr(code) for code in computer.run_program())

class TestAscii(unittest.TestCase):
    def test_run_ascii(self):
        with open('day17input.txt') as infile:
            program = list(map(int, infile.read().split(',')))
        scaff_map = run_ascii(program)
        chars_used = set(scaff_map)
        chars_allowed = {'.', '#', '^', 'v', '<', '>', '\n'}
        self.assertTrue(chars_used.issubset(chars_allowed))
        print(''.join(scaff_map))

    def test_find_intersections(self):
        scaff_map = """
            ..#..........
            ..#..........
            #######...###
            #.#...#...#.#
            #############
            ..#...#...#..
            ..#####...^.."""
        result = find_intersections(scaff_map)
        expected_result = [(2, 2), (2, 4), (6, 4), (10, 4)]
        self.assertEqual(expected_result, result)

    def test_get_alignment_sum(self):
        scaff_map = """
            ..#..........
            ..#..........
            #######...###
            #.#...#...#.#
            #############
            ..#...#...#..
            ..#####...^.."""
        result = get_alignment_sum(scaff_map)
        self.assertEqual(76, result)

    def test_result_part_one(self):
        with open('day17input.txt') as infile:
            program = list(map(int, infile.read().split(',')))
        scaff_map = run_ascii(program)
        result = get_alignment_sum(scaff_map)
        self.assertEqual(2660, result)

    def test_follow_path(self):
        known_path = (
            'L,10,R,8,L,6,R,6, L,8,L,8,R,8, L,10,R,8,L,6,R,6'  # A B A
            'R,8,L,6,L,10,L,10, L,10,R,8,L,6,R,6, L,8,L,8,R,8'  # C A B
            'R,8,L,6,L,10,L,10, L,8,L,8,R,8,'  # C B
            'R,8,L,6,L,10,L,10, L,8,L,8,R,8')  # C B
        A = 'L,10,R,8,L,6,R,6'
        B = 'L,8,L,8,R,8'
        C = 'R,8,L,6,L,10,L,10'
        first_seq = 'A,B,A,C,A,B,C,B,C,B'
        video = 'n'
        result = follow_path(first_seq, A, B, C, video)
        print(result)
        print(ord(result[-1]))


if __name__ == '__main__':
    unittest.main()

import operator

import math
import unittest
from itertools import permutations, zip_longest, chain
from collections import defaultdict


def is_between(point1, point2, point3):
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    dotproduct = (x1 - x2) * (x3 - x2) + (y1 - y2) * (y3 - y2)
    if dotproduct < 0:
        return False
    squaredlengthba = (x3 - x2) * (x3 - x2) + (y3 - y2) * (y3 - y2)
    if dotproduct > squaredlengthba:
        return False
    return True


def check_is_blocking(station, could_block, check_blocked):
    if not is_collinear(station, could_block, check_blocked):
        return False
    if is_between(station, could_block, check_blocked):
        return False
    return distance(station, could_block) < distance(station, check_blocked)


def is_collinear(point1, point2, point3):
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    a = x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)
    return a == 0


def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((y1-y2)**2 + (x1-x2)**2)


def read_map(map):
    result = set()
    for row_num, row in enumerate(map.splitlines(keepends=False)):
        row = row.strip()
        for col_num, char in enumerate(row):
            if char == '#':
                result.add((col_num, row_num))
    return result


def count_detected(ast_set):
    result = {position: 0 for position in ast_set}
    for station_asteroid, check_blocked in permutations(ast_set, 2):
        remaining_asteroids = ast_set.difference({station_asteroid,
                                                  check_blocked})
        blocked = False
        for blocking in remaining_asteroids:
            if check_is_blocking(station_asteroid, blocking, check_blocked):
                blocked = True
                break
        if not blocked:
            result[station_asteroid] = result[station_asteroid] + 1
    return result


def pick_station(ast_map):
    ast_set = read_map(ast_map)
    visible = count_detected(ast_set)
    loc, max_visible= max(visible.items(), key=operator.itemgetter(1))
    return loc, max_visible

def get_angle(station, asteroid):
    y_station, x_station = station
    y_asteroid, x_asteroid = asteroid
    return math.degrees(math.atan2((y_asteroid - y_station),
                                    -(x_asteroid - x_station))) % 360


def sequence_vaporizing(station, asteroids):
    asteroids = asteroids.difference({station})
    groups = defaultdict(list)
    for asteroid in asteroids:
        groups[get_angle(station, asteroid)].append(asteroid)
    for angle_group in groups.values():
        angle_group.sort(key=lambda asteroid: distance(station, asteroid))
    interim = [val for key, val in sorted(groups.items())]
    zipped = list(zip_longest(*interim))
    result = list(filter(None, chain.from_iterable(zipped)))
    return result


class TestAsteroidBlocking(unittest.TestCase):
    def test_is_blocking(self):
        station = (0, 0)
        could_block = (1, 1)
        check_blocked = (2, 2)
        result = check_is_blocking(station, could_block, check_blocked)
        self.assertEqual(True, result)

    def test_not_blocking(self):
        station = (0, 0)
        could_block = (2, 1)
        check_blocked = (2, 2)
        result = check_is_blocking(station, could_block, check_blocked)
        self.assertEqual(False, result)

    def test_between(self):
        station = (0, 3)
        check_blocked = (0, 1)
        could_block = (0, 4)
        result = check_is_blocking(station, could_block, check_blocked)
        self.assertEqual(False, result)

    def test_read_map(self):
        ast_map = """.#..#
                     .....
                     #####
                     ....#
                     ...##"""
        expected_result = {(1, 0), (4, 0),
                           (0, 2), (1, 2), (2, 2), (3, 2), (4, 2),
                           (4, 3),
                           (3, 4), (4, 4)}
        result = read_map(ast_map)
        self.assertEqual(expected_result, result)

    def test_count_detected(self):
        ast_map = """.#..#
                     .....
                     #####
                     ....#
                     ...##"""
        ast_set = read_map(ast_map)
        expected_result = {(1, 0): 7, (4, 0):7,
                           (0, 2): 6, (1, 2): 7, (2, 2): 7, (3, 2): 7,
                           (4, 2): 5,
                           (4, 3): 7,
                           (3, 4): 8, (4, 4): 7}
        result = count_detected(ast_set)
        self.assertEqual(expected_result, result)

    def test_pick_station_1(self):
        ast_map = """......#.#.
                     #..#.#....
                     ..#######.
                     .#.#.###..
                     .#..#.....
                     ..#....#.#
                     #..#....#.
                     .##.#..###
                     ##...#..#.
                     .#....####"""
        self.run_pick_station_test(ast_map, (5, 8), 33)

    def test_pick_station_2(self):
        ast_map = """#.#...#.#.
                     .###....#.
                     .#....#...
                     ##.#.#.#.#
                     ....#.#.#.
                     .##..###.#
                     ..#...##..
                     ..##....##
                     ......#...
                     .####.###."""
        self.run_pick_station_test(ast_map, (1, 2), 35)

    def test_pick_station_3(self):
        as_map = """.#..#..###
                    ####.###.#
                    ....###.#.
                    ..###.##.#
                    ##.##.#.#.
                    ....###..#
                    ..#.#..#.#
                    #..#.#.###
                    .##...##.#
                    .....#.#.."""
        self.run_pick_station_test(as_map, (6, 3), 41)

    def test_pick_station_4(self):
        as_map = """.#..##.###...#######
                    ##.############..##.
                    .#.######.########.#
                    .###.#######.####.#.
                    #####.##.#.##.###.##
                    ..#####..#.#########
                    ####################
                    #.####....###.#.#.##
                    ##.#################
                    #####.##.###..####..
                    ..######..##.#######
                    ####.##.####...##..#
                    .#####..#.######.###
                    ##...#.##########...
                    #.##########.#######
                    .####.#.###.###.#.##
                    ....##.##.###..#####
                    .#.#.###########.###
                    #.#.#.#####.####.###
                    ###.##.####.##.#..##"""
        self.run_pick_station_test(as_map, (11, 13), 210)

    def run_pick_station_test(self, ast_map, expected_loc, expected_count):
        loc, count = pick_station(ast_map)
        self.assertEqual(expected_loc, loc)
        self.assertEqual(expected_count, count)

    def test_answer_part_1(self):
        with open('day10_input.txt') as map_file:
            ast_map = map_file.read()
        loc, count = pick_station(ast_map)
        self.assertEqual(334, count)

    def test_get_angle(self):
        self.run_get_angle_test((1, 1), (1, 0), 0)
        self.run_get_angle_test((1, 1), (2, 0), 45)
        self.run_get_angle_test((1, 1), (2, 1), 90)
        self.run_get_angle_test((1, 1), (2, 2), 135)
        self.run_get_angle_test((11, 13), (11, 12),0)

    def run_get_angle_test(self, station, asteroid, expected_angle):
        angle = get_angle(station, asteroid)
        self.assertEqual(expected_angle, angle)

    def test_sequence_vaporizing(self):
        as_map = """.#..##.###...#######
                    ##.############..##.
                    .#.######.########.#
                    .###.#######.####.#.
                    #####.##.#.##.###.##
                    ..#####..#.#########
                    ####################
                    #.####....###.#.#.##
                    ##.#################
                    #####.##.###..####..
                    ..######..##.#######
                    ####.##.####...##..#
                    .#####..#.######.###
                    ##...#.##########...
                    #.##########.#######
                    .####.#.###.###.#.##
                    ....##.##.###..#####
                    .#.#.###########.###
                    #.#.#.#####.####.###
                    ###.##.####.##.#..##"""
        ast_set = read_map(as_map)
        result = sequence_vaporizing((11, 13), ast_set)
        self.assertEqual((11, 12), result[0])
        self.assertEqual((12, 1), result[1])
        self.assertEqual((12, 2), result[2])
        self.assertEqual((12, 8), result[9])
        self.assertEqual((16, 0), result[19])
        self.assertEqual((16, 9), result[49])
        self.assertEqual((10, 16), result[99])
        self.assertEqual((9, 6), result[198])
        self.assertEqual((8, 2), result[199])
        self.assertEqual((10, 9), result[200])
        self.assertEqual((11, 1), result[-1])

    def test_answer_part_1(self):
        with open('day10_input.txt') as map_file:
            ast_map = map_file.read()
        ast_set = read_map(ast_map)
        station, count = pick_station(ast_map)
        result = sequence_vaporizing(station, ast_set)
        self.assertEqual((11, 19), result[199])

if __name__ == '__main__':
    unittest.main()

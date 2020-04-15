from collections import defaultdict
from string import ascii_uppercase

import math
import numpy as np
import unittest
from numpy.testing import assert_array_equal
from matplotlib import pyplot as plt

TEST_MAP_1 = """
         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       """

TEST_MAP_2 = """
                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               """

TEST_MAP_3 = """
             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                      """
MULT = 2
PLOT_X = 6
PLOT_Y = 3
PLOT_UPDATE = 50

def convert_to_array(rows):
    mapping = defaultdict(lambda: 1)
    mapping['.'] = 0
    max_len = max(len(row) for row in rows)
    rows = [row[2:max_len-2] for row in rows[2:-2]]
    result = [[mapping[char] for char in row] for row in rows]
    one_maze = np.asarray(result)
    return np.tile(one_maze, (MULT * PLOT_X * PLOT_Y, 1, 1))


def find_portals(rows):
    portals = defaultdict(set)
    num_rows = len(rows)
    num_cols = max(len(row) for row in rows)
    for row_num, row in enumerate(rows):
        for col_num, char in enumerate(row):
            if char in ascii_uppercase:
                try:
                    right_is_letter = row[col_num + 1] in ascii_uppercase
                except IndexError:
                    right_is_letter = False
                try:
                    down_is_letter = (rows[row_num + 1][col_num]
                                      in ascii_uppercase)
                except IndexError:
                    down_is_letter = False
                if right_is_letter:
                    portal_name = char + row[col_num + 1]
                    portal_position, _ = farther_from_center(col_num, num_cols)
                    portals[portal_name].add((row_num - 2, portal_position))
                if down_is_letter:
                    portal_name = char + rows[row_num + 1][col_num]
                    portal_position, _ = farther_from_center(row_num, num_rows)
                    portals[portal_name].add((portal_position, col_num - 2))
    return dict(portals)


def farther_from_center(position, size):
    if position == 0 or size/2 < position < size - 4:
        result = position
    else:
        result = position - 3
    if position == 0 or position > size - 4:
        kind = 'o'
    else:
        kind = 'i'
    return result, kind

class PathFinder:
    def __init__(self, area_map):
        rows = [row for row in area_map.splitlines() if row]
        self.grid = convert_to_array(rows)
        middle = len(rows) // 2 - 1
        self.grid[0, middle, middle] = 0
        self.portals = find_portals(rows)
        self.end_point = list(self.portals['ZZ'])[0]
        self.start_point = list(self.portals['AA'])[0]
        self.portal_squares = set.union(*self.portals.values())
        self.old_leaves = set()
        self.new_leaves = set()
        # self.show()

    def take_one_recursive_step(self):
        for point in self.old_leaves:
            self.expand_from_point(point, 2)
        self.take_recursive_portal_steps()
        self.draw()

    def draw(self):
        if self.steps % PLOT_UPDATE == 0:
            z, _, _ = self.grid.shape
            plt.clf()
            for i, grid in enumerate(self.grid):
                if i < PLOT_Y * PLOT_X:
                    ax = plt.subplot(PLOT_Y, PLOT_X, i + 1)
                    ax.set_axis_off()
                    plt.imshow(grid)
            plt.subplots_adjust(wspace=0.01, hspace=0.01)
            plt.draw()
            plt.pause(0.001)

    def take_one_water_step(self):
        filled = np.argwhere(self.grid == 2)
        for point in filled:
            self.expand_from_point(point, 2)
        self.take_portal_steps(filled)
        plt.clf()
        plt.imshow(self.grid)
        plt.draw()
        plt.pause(0.01)

    def expand_from_point(self, point, water_index=2):
        z, x, y = point
        self.try_to_fill(z, x-1, y, water_index)
        self.try_to_fill(z, x+1, y, water_index)
        self.try_to_fill(z, x, y-1, water_index)
        self.try_to_fill(z, x, y+1, water_index)

    def try_to_fill(self, z, y, x, water_index=3):
        if x >= 0 and y >= 0:
            try:
                empty = self.grid[z, y, x] == 0
            except IndexError:
                empty = False
            if empty:
                self.new_leaves.add((z, y, x))
                self.grid[z, y, x] = 2

    def show(self):
        plt.clf()
        plt.imshow(self.grid)
        plt.show()

    def take_portal_steps(self, filled):
        for y, x in filled:
            if (y, x) in self.portal_squares:
                right_set = [val for val in self.portals.values()
                             if (y, x) in val]
                for fill_point in right_set[0]:
                    self.grid[fill_point] = 2
                    # self.portal_squares = self.portal_squares.difference(
                    #     {fill_point})

    def take_recursive_portal_steps(self):
        for z, y, x in self.old_leaves:
            if (y, x) in self.portal_squares:
                right_set = [val for val in self.portals.values()
                             if (y, x) in val]
                for fill_point in right_set[0]:
                    if fill_point != (y, x):
                        lvl_change = self.get_level_change((y, x))
                        if lvl_change > 0 or z > 0:
                            self.try_to_fill(z + lvl_change, fill_point[0],
                                       fill_point[1])
                            # self.portal_squares = self.portal_squares.difference(
                            #     {fill_point})

    def find_full_path_length(self):
        self.steps = 0
        while self.grid[self.end_point] == 0:
            self.steps = self.steps + 1
            self.take_one_water_step()
        # self.show()
        return self.steps

    def find_recursive_path_length(self):
        self.steps = 0
        self.try_to_fill(0, self.start_point[0], self.start_point[1])
        while self.grid[0, self.end_point[0], self.end_point[1]] == 0:
        # seq = {'0 AAo to XFi' : 16, '1 XFo to CKi' : 11, '2CKo to ZHi': 15,
        #        '3 ZHo to WBi' : 11, '4 WBo to ICi' : 11}
        # for name, steps in seq.items():
        #     for step in range(steps):
            self.old_leaves = self.new_leaves
            self.new_leaves = set()
            self.steps = self.steps + 1
            self.take_one_recursive_step()
            # print(self.steps)
            # print(name)
            # self.draw()
            # plt.show()
        return self.steps

    def get_level_change(self, fill_point):
        _, nrows, ncols = self.grid.shape
        if min(fill_point) < 3:
            return -1
        if nrows - fill_point[0] < 3:
            return -1
        if ncols - fill_point[1] < 3:
            return -1
        return 1




class TestPathfinder(unittest.TestCase):
    def test_take_one_water_step(self):
        finder = PathFinder(TEST_MAP_1)
        finder.grid[0, 7] = 2
        # finder.show()
        finder.take_one_water_step()
        finder.show()
        result = finder.grid
        expected_result = np.asarray([
            [1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1]])
        assert_array_equal(expected_result, result)

    def test_take_one_portal_step(self):
        finder = PathFinder(TEST_MAP_1)
        finder.grid[4, 7] = 2
        # finder.show()
        finder.take_one_water_step()
        finder.show()
        result = finder.grid
        expected_result = np.asarray([
            [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [2, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1]])
        assert_array_equal(expected_result, result)

    def test_convert_to_array(self):
        rows = [row for row in TEST_MAP_1.splitlines() if row]
        result = convert_to_array(rows)
        expected_result = np.asarray([
            [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1]])
        assert_array_equal(expected_result, result)

    def test_find_full_path(self):
        finder = PathFinder(TEST_MAP_1)
        result = finder.find_full_path_length()
        self.assertEqual(23, result)

    def test_find_full_path_2(self):
        finder = PathFinder(TEST_MAP_2)
        result = finder.find_full_path_length()
        self.assertEqual(58, result)

    def test_part_1(self):
        with open('day20_input.txt') as infile:
            area_map = infile.read()
        finder = PathFinder(area_map)
        result = finder.find_full_path_length()
        self.assertEqual(556, result)

    def test_distance_3(self):
        finder = PathFinder(TEST_MAP_3)
        try:
            result = finder.find_recursive_path_length()
        except IndexError:
            print(finder.steps)
            plt.show()
            raise
        plt.show()
        self.assertEqual(396, result)

    def test_part_2(self):
        with open('day20_input.txt') as infile:
            area_map = infile.read()
        finder = PathFinder(area_map)
        try:
            result = finder.find_recursive_path_length()
        except IndexError:
            plt.show()
            raise
        plt.show()
        self.assertEqual(6532, result)

if __name__ == '__main__':
    unittest.main()

import contextlib
import unittest
from collections import defaultdict
from functools import lru_cache
from string import ascii_uppercase
import networkx as nx
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


def find_shortest_paths(portals, tree):
    result = defaultdict(dict)
    sources = {name: pos for name, pos in portals.items() if name != 'ZZ'}
    for source_name, source_set in sources.items():
        targets = {name: pos for name, pos in portals.items()
                   if name not in (source_name, 'AA')}
        for target_name, target_set in targets.items():
            paths = []
            for source in source_set:
                for target in target_set:
                    try:
                        path_length = nx.shortest_path_length(tree, source,
                                                              target)
                    except nx.NetworkXNoPath:
                        pass
                    else:
                        paths.append(path_length)
            with contextlib.suppress(ValueError):
                result[source_name][target_name] = min(paths) + 1
    return result


def find_edges(rows):
    rows = [row[2:-2] for row in rows[2:-2]]
    edges = []
    for x, row in enumerate(rows):
        for y, char in enumerate(row):
            if char == '.':
                to_test = [(x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1)]
                for x_test, y_test in to_test:
                    try:
                        char = rows[x_test][y_test]
                    except IndexError:
                        pass
                    else:
                        if char == '.':
                            edges.append(((x, y), (x_test, y_test)))
    return edges


def find_recursive_portals(rows):
    num_rows = len(rows)
    num_cols = max(len(row) for row in rows)
    portals = {}
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
                    portal_position, kind = farther_from_center(col_num,
                                                                 num_cols)
                    portals[portal_name + kind] = (row_num - 2, portal_position)
                if down_is_letter:
                    portal_name = char + rows[row_num + 1][col_num]
                    portal_position, kind = farther_from_center(row_num,
                                                                 num_rows)
                    portals[portal_name + kind] = (portal_position, col_num - 2)
    start_pos = portals.pop('AAo')
    end_pos = portals.pop('ZZo')
    return start_pos, portals, end_pos

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


def find_full_path(area_map):
    paths = compute_paths(area_map)
    edges = ((source, target, dist)
             for source, targets in paths.items()
             for target, dist in targets.items())
    tree = nx.Graph()
    tree.add_weighted_edges_from(edges)
    # nx.draw_networkx(tree)
    # plt.show()
    distance = nx.dijkstra_path_length(tree, 'AA', 'ZZ')
    return distance - 1


def compute_paths(area_map):
    rows = [row for row in area_map.splitlines() if row]
    portals = find_portals(rows)
    edges = find_edges(rows)
    tree = nx.Graph()
    tree.add_edges_from(edges)
    result = find_shortest_paths(portals, tree)
    return dict(result)


def find_recursive_shortest_paths(portals, start_pos, end_pos, tree):
    result = defaultdict(dict)
    sources = {name: pos for name, pos in portals.items()}
    sources['AA'] = start_pos
    for source_name, source in sources.items():
        targets = {name: pos for name, pos in portals.items()
                   if name != source_name}
        targets['ZZ'] = end_pos
        for target_name, target in targets.items():
            try:
                path_length = nx.shortest_path_length(tree, source, target)
            except nx.NetworkXNoPath:
                pass
            else:
                result[source_name][target_name] = path_length + 1
    return result

def compute_recursive_paths(area_map):
    rows = [row for row in area_map.splitlines() if row]
    start_pos, portals, end_pos = find_recursive_portals(rows)
    edges = find_edges(rows)
    tree = nx.Graph()
    tree.add_edges_from(edges)
    result = find_recursive_shortest_paths(portals, start_pos, end_pos, tree)
    return dict(result)

@lru_cache
def score(portals, cur_portal, level, through):
    if cur_portal == 'ZZ' and level == 0:
        return 0
    avail_scores = []
    for (portal, dist, lvl_change) in get_avail_portals(portals, cur_portal,
                                                        through):
        new_through = through.union({portal})
        new_score = score(portals, portal, level + lvl_change, new_through) + \
                    dist
        avail_scores.append(new_score)
    return min(avail_scores)

def get_avail_portals(paths, portal_in, level, through):
    portal_out = reverse_portal(portal_in)
    result = set()
    portals = set(paths.keys).difference(through)
    for portal, dist in paths[portal_out].items():
        if portal in portals and (portal != 'ZZ' or level != 0):
            lvl_change = get_level_change(portal)
            result.add((portal, dist, lvl_change))
    return result



class TestPathFinder(unittest.TestCase):
    def test_compute_paths(self):
        expected_result = {'AA': {'BC': 5, 'FG': 31, 'ZZ': 27},
                           'BC': {'DE': 7, 'FG': 33, 'ZZ': 29},
                           'DE': {'BC': 7, 'FG': 5},
                           'FG': {'BC': 33, 'DE': 5, 'ZZ': 7}}
        paths = compute_paths(TEST_MAP_1)
        self.assertEqual(expected_result, paths)

    def test_find_portals(self):
        expected_result = {'AA': {(0, 7)}, 'BC': {(6, 0), (4, 7)},
                           'DE': {(8, 4), (11, 0)}, 'FG': {(10, 9), (13, 0)},
                           'ZZ': {(14, 11)}}
        rows = [row for row in TEST_MAP_1.splitlines() if row]
        result = find_portals(rows)
        self.assertEqual(expected_result, result)

    def test_find_portals_2(self):
        expected_result = {'AA': {(0, 17)},
                           'AS': {(6, 15), (15, 30)},
                           'CP': {(6, 19), (32, 17)},
                           'VT': {(9, 30), (21, 24)},
                           'YN': {(11, 24), (21, 0)},
                           'DI': {(13, 0), (19, 6)},
                           'ZZ': {(15, 0)},
                           'QG': {(15, 24), (21, 30)},
                           'JO': {(17, 0), (26, 11)},
                           'BU': {(19, 24), (32, 9)},
                           'LF': {(19, 30), (26, 13)},
                           'JP': {(26, 19), (32, 13)}}
        rows = [row for row in TEST_MAP_2.splitlines() if row]
        result = find_portals(rows)
        self.assertEqual(expected_result, result)

    def test_find_full_path(self):
        result = find_full_path(TEST_MAP_1)
        self.assertEqual(23, result)

    def test_find_full_path2(self):
        result = find_full_path(TEST_MAP_2)
        self.assertEqual(58, result)

    def test_part_1(self):
        with open('day20_input.txt') as infile:
            area_map = infile.read()
        result = find_full_path(area_map)
        self.assertEqual(result, 556)  # 558 is too high
        print(result)

    def test_find_recursive_portals(self):
        expected_result = {'BCo': (6, 0), 'BCi': (4, 7),
                           'DEi': (8, 4), 'DEo': (11, 0),
                           'FGi': (10, 9),'FGo': (13, 0)}
        rows = [row for row in TEST_MAP_1.splitlines() if row]
        in_loc, result, out_loc = find_recursive_portals(rows)
        self.assertEqual(expected_result, result)
        self.assertEqual((0, 7), in_loc)
        self.assertEqual((14, 11), out_loc)

    def test_compute_recursive_paths(self):
        expected_result = {'AA': {'BCi': 5, 'FGi': 31, 'ZZ': 27},
                           'BCi': {'FGi': 33, 'ZZ': 29},
                           'BCo': {'DEi': 7},
                           'DEi': {'BCo': 7},
                           'DEo': {'FGo': 5},
                           'FGi': {'BCi': 33, 'ZZ': 7},
                           'FGo': {'DEo': 5}}
        paths = compute_recursive_paths(TEST_MAP_1)
        self.assertEqual(expected_result, paths)


if __name__ == '__main__':
    unittest.main()

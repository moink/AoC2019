import unittest
import contextlib
from functools import lru_cache
from string import ascii_lowercase, ascii_uppercase
from collections import defaultdict

import networkx as nx
import matplotlib.pyplot as plt


class PathFinder:
    
    def __init__(self, area_map):
        self.key_paths = precompute_paths(area_map)
        self.all_keys = set(char for char in area_map if char in
                            '@0123' + ascii_lowercase)

    @lru_cache(None)
    def get_reachable_keys(self, latest, keys_found):
        all_keys = self.key_paths[latest]
        reachable_keys = {key: dist for key, (dist, doors) in all_keys.items()
                          if set(doors).issubset(keys_found) and key not in
                          keys_found}
        return reachable_keys

    def find_path_length(self):
        return self.score('@', '@')

    @lru_cache(None)
    def score(self, start_pos, keys):
        if set(keys) == self.all_keys:
            return 0
        possible_scores = []
        for key, steps in self.get_reachable_keys(start_pos, keys).items():
            new_keys = ''.join(sorted(keys + key))
            key_score = self.score(key, new_keys)
            possible_scores.append(key_score + steps)
        return min(possible_scores)

    @lru_cache(None)
    def multi_score(self, start_pos, keys):
        if set(keys) == self.all_keys:
            return 0
        possible_scores = []
        for pos in start_pos:
            for key, steps in self.get_reachable_keys(pos, keys).items():
                new_keys = ''.join(sorted(keys + key))
                new_pos = start_pos.replace(pos, key)
                key_score = self.multi_score(new_pos, new_keys)
                possible_scores.append(key_score + steps)
        return min(possible_scores)

    def find_multi_path_length(self):
        return self.multi_score('0123', '0123')




def precompute_paths(area_map):
    rows = [row.strip() for row in area_map.splitlines()]
    edges = []
    nodes = []
    result = defaultdict(dict)
    for x, row in enumerate(rows):
        for y, char in enumerate(row):
            if char != '#':
                nodes.append(((x, y), {'name': char}))
                to_test = [(x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1)]
                for x_test, y_test in to_test:
                    char = rows[x_test][y_test]
                    if char != '#':
                        edges.append(((x, y), (x_test, y_test)))
    tree = nx.Graph()
    tree.add_nodes_from(nodes)
    tree.add_edges_from(edges)
    for source_name in '@0123' + ascii_lowercase:
        source = find_node(tree, source_name)
        if source:
            for target_name in ascii_lowercase:
                target = find_node(tree, target_name)
                try:
                    path = nx.shortest_path(tree, source, target)
                except nx.NetworkXNoPath:
                    pass
                else:
                    if target and target_name != source_name:
                        result[source_name][target_name] = (
                            len(path) - 1, doors_on_path(area_map, path))
    return result


def doors_on_path(area_map, path):
    rows = [row.strip() for row in area_map.splitlines()]
    result = []
    for i, j in path:
        char = rows[i][j]
        if char in ascii_uppercase:
            result.append(char.lower())
    return ''.join(sorted(result))

def find_node(tree, name):
    for node in tree.nodes(data='name'):
        if node[1] == name:
            return node[0]


def create_part_two_map():
    with open('day18_input.txt') as infile:
        area_map = infile.read()
    chars = [[char for char in row.strip()] for row in area_map.splitlines()]
    new_walls = ((40, 40), (39, 40), (41, 40), (40, 39), (40, 41))
    for x, y in new_walls:
        chars[x][y] = '#'
    chars[39][39] = '0'
    chars[39][41] = '1'
    chars[41][41] = '2'
    chars[41][39] = '3'
    area_map = '\n'.join((''.join(row) for row in chars))
    return area_map

class TestPathFinder(unittest.TestCase):

    def test_precompute_paths(self):
        area_map = """#########
                      #b.A.@.a#
                      #########"""
        expected_result = {'@': {'a': (2, ''), 'b': (4, 'a')},
                           'a': {'b': (6, 'a')},
                           'b': {'a': (6, 'a')}}
        result = precompute_paths(area_map)
        self.assertEqual(expected_result, result)

    def test_distance_to_keys_simplest(self):
        area_map = """#########
                      #b.A.@.a#
                      #########"""
        exp_result = {'a' : 2}
        finder = PathFinder(area_map)
        result = finder.get_reachable_keys('@', frozenset())
        self.assertEqual(exp_result, result)

    def test_create_decision_tree_edges(self):
        area_map = """#########
                      #b.A.@.a#
                      #########"""
        finder = PathFinder(area_map)
        expected_edges = {(('@', frozenset({'@'})),
                           ('a', frozenset({'a','@'})), 2),
                          (('a', frozenset({'a', '@'})),
                           ('b', frozenset({'a', 'b', '@'})), 6)}
        edges = finder.create_decision_tree_edges(frozenset('@'), '@')
        self.assertEqual(expected_edges, edges)

    def test_distance(self):
        area_map = """#########
                      #b.A.@.a#
                      #########"""
        self.run_distance_test(area_map, 8)

    def run_distance_test(self, area_map, expected):
        finder = PathFinder(area_map)
        distance = finder.find_path_length()
        self.assertEqual(expected, distance)

    def test_distance_two(self):
        area_map = """########################
                      #f.D.E.e.C.b.A.@.a.B.c.#
                      ######################.#
                      #d.....................#
                      ########################"""
        self.run_distance_test(area_map, 86)

    def test_distance_three(self):
        area_map = """########################
                      #...............b.C.D.f#
                      #.######################
                      #.....@.a.B.c.d.A.e.F.g#
                      ########################"""
        self.run_distance_test(area_map, 132)

    def test_distance_four(self):
        area_map = """#################
                      #i.G......e....p#
                      ########.########
                      #j.A..b........o#
                      ########@########
                      #k.E..a...g..B.n#
                      ########.########
                      #l..............#
                      #################"""
        self.run_distance_test(area_map, 110)

    def test_distance_five(self):
        area_map = """#################
                      #i.G..c...e..H.p#
                      ########.########
                      #j.A..b...f..D.o#
                      ########@########
                      #k.E..a...g..B.n#
                      ########.########
                      #l.F..d...h..C.m#
                      #################"""
        self.run_distance_test(area_map, 136)

    def test_part_one(self):
        with open('day18_input.txt') as infile:
            area_map = infile.read()
        self.run_distance_test(area_map, 4118)

    def test_precompute_paths_big(self):
        with open('day18_input.txt') as infile:
            area_map = infile.read()
        result = precompute_paths(area_map)
        print(result)

    def test_precompute_paths_part_two(self):
        area_map = create_part_two_map()
        result = precompute_paths(area_map)
        print(result)

    def test_multi_distance_one(self):
        area_map = """#######
                      #a.#Cd#
                      ##0#1##
                      #######
                      ##2#3##
                      #cB#Ab#
                      #######"""
        self.run_multi_distance_test(area_map, 8)

    def run_multi_distance_test(self, area_map, expected):
        finder = PathFinder(area_map)
        distance = finder.find_multi_path_length()
        self.assertEqual(expected, distance)

    def test_multi_distance_two(self):
        area_map = """#############
                      #g#f.D#..h#l#
                      #F###e#E###.#
                      #dCba0#1BcIJ#
                      #############
                      #nK.L2#3G...#
                      #M###N#H###.#
                      #o#m..#i#jk.#
                      #############"""
        self.run_multi_distance_test(area_map, 72)

    def test_part_two(self):
        area_map = create_part_two_map()
        self.run_multi_distance_test(area_map, 72)


if __name__ == '__main__':
    unittest.main()

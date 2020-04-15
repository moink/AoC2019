import unittest
import contextlib
from functools import lru_cache
from string import ascii_lowercase, ascii_uppercase
from collections import defaultdict

import networkx as nx
import matplotlib.pyplot as plt

def find_path_edges(area_map):
    rows = [row.strip() for row in area_map.splitlines()]
    clear = ascii_lowercase + '.@'
    edges = set()
    for row_number, row in enumerate(rows[:-1]):
        for col_number,char in enumerate(row[:-1]):
            if char in clear:
                if rows[row_number][col_number + 1] in clear:
                    edge = ((row_number, col_number),
                            (row_number, col_number + 1))
                    edges.add(edge)
                if rows[row_number + 1][col_number] in clear:
                    edge = ((row_number, col_number),
                            (row_number + 1, col_number))
                    edges.add(edge)
    return edges

def find_position(area_map, char):
    rows = [row.strip() for row in area_map.splitlines()]
    for row_number, row in enumerate(rows):
        col_number = row.find(char)
        if col_number != -1:
            return (row_number, col_number)
    raise ValueError('No such character "' + char + '" in map')

def find_all_key_positions(area_map):
    result = {}
    for char in ascii_lowercase + '@':
        with contextlib.suppress(ValueError):
            result[char] = find_position(area_map, char)
    return result


def find_open_path_edges(area_map):
    result = defaultdict(set)
    rows = [row.strip() for row in area_map.splitlines()]
    clear = ascii_lowercase + '.@'
    for door in ascii_uppercase:
        try:
            x, y = find_position(area_map, door)
        except ValueError:
            pass
        else:
            to_test = [(x-1, y), (x+1, y), (x, y+1), (x, y-1)]
            for x_test, y_test in to_test:
                if rows[x_test][y_test] in clear:
                    result[door.lower()].add(((x, y), (x_test, y_test)))
    return result

class PathFinder:
    
    def __init__(self, area_map):
        base_path_edges = find_path_edges(area_map)
        self.base_tree = nx.Graph()
        self.base_tree.add_edges_from(base_path_edges)
        self.key_locations = find_all_key_positions(area_map)
        self.open_path_edges = find_open_path_edges(area_map)

    @lru_cache(None)
    def get_reachable_keys(self, latest, keys_found):
        tree = self.base_tree.copy()
        cur_pos = self.key_locations[latest]
        for key in keys_found:
            tree.add_edges_from(self.open_path_edges[key])
        not_found = set(ascii_lowercase).difference(keys_found)
        with contextlib.suppress(KeyError):
            not_found.remove(latest)
        result = {}
        # nx.draw_networkx(tree)
        # plt.show()
        for key in not_found:
            try:
                position = self.key_locations[key]
            except KeyError:
                pass
            else:
                with contextlib.suppress(nx.exception.NetworkXNoPath,
                                         nx.exception.NodeNotFound):
                    result[key] = nx.shortest_path_length(tree, cur_pos,
                                                          position)
        return result

    # @lru_cache(None)
    def create_decision_tree_edges(self, already_found, start_pos):
        result = []
        keys = self.get_reachable_keys(start_pos, already_found)
        for key, dist in keys.items():
            now_found = ''.join(sorted(already_found + key))
            result.append(((start_pos, already_found), (key, now_found), dist))
            new_edges = self.create_decision_tree_edges(now_found, key)
            result = result + new_edges
        return result

    def find_path_length(self):
        start = ('@', '@')
        edges = self.create_decision_tree_edges(*start)
        key_graph = nx.DiGraph()
        key_graph.add_weighted_edges_from(edges)
        # nx.draw_networkx(key_graph)
        # plt.show()
        target_part = ''.join(sorted(self.key_locations.keys()))
        targets = [node for node in key_graph.nodes if node[1] == target_part]
        lengths = [nx.shortest_path_length(key_graph, start, target, 'weight')
                   for target in targets]
        return min(lengths)


class TestPathFinder(unittest.TestCase):

    def test_find_open_path_edges(self):
        area_map = """#########
                      #b.A.@.a#
                      #########"""
        expected_result = {'a': {((1, 3), (1, 2)), ((1, 3), (1, 4))}}
        result = find_open_path_edges(area_map)
        self.assertEqual(expected_result, result)

    def test_find_open_path_edges_vertical(self):
        area_map = """###.#
                      ###Q#
                      ###.#"""
        expected_result = {'q': {((1, 3), (0, 3)), ((1, 3), (2 ,3))}}
        result = find_open_path_edges(area_map)
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

    def test_part_one(self):
        with open('day18_input.txt') as infile:
            area_map = infile.read()
        self.run_distance_test(area_map, 100)

if __name__ == '__main__':
    unittest.main()

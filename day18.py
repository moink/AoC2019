import contextlib
import unittest
from string import ascii_lowercase
import networkx as nx
import matplotlib.pyplot as plt


def find_position(area_map, char):
    rows = [row.strip() for row in area_map.splitlines()]
    for row_number, row in enumerate(rows):
        col_number = row.find(char)
        if col_number != -1:
            return (row_number, col_number)
    raise ValueError('No such character "' + char + '" in map')


def find_all_key_positions(area_map):
    result = {}
    for char in ascii_lowercase:
        with contextlib.suppress(ValueError):
            result[char] = find_position(area_map, char)
    return result


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


def distance_to_keys(area_map):
    cur_position = find_position(area_map, '@')
    key_positions = find_all_key_positions(area_map)
    path_graph = nx.Graph()
    edges = find_path_edges(area_map)
    path_graph.add_edges_from(edges)
    result = {}
    for key, position in key_positions.items():
        with contextlib.suppress(nx.exception.NetworkXNoPath,
                                 nx.exception.NodeNotFound):
            result[key] = nx.shortest_path_length(path_graph, cur_position,
                                                  position)
    return result


def pick_up_key(area_map, key):
    area_map = area_map.replace('@', '.')
    area_map = area_map.replace(key, '@')
    area_map = area_map.replace(key.upper(), '.')
    return area_map


def create_decision_tree_edges(area_map, start):
    result = set()
    for key, distance in distance_to_keys(area_map).items():
        new_map = pick_up_key(area_map, key)
        prefix = ''.join(sorted(start + key))
        new_edges = create_decision_tree_edges(new_map, prefix)
        result = new_edges.union({(start, prefix, distance)})
    return result


def find_dist_to_all_keys(area_map):
    letters = ''.join(sorted(char for char in area_map if char in
                             ascii_lowercase))
    key_graph = nx.DiGraph()
    edges = create_decision_tree_edges(area_map, '@')
    key_graph.add_weighted_edges_from(edges)
    nx.draw_networkx(key_graph)
    plt.show()
    target = '@' + letters
    path_length = nx.shortest_path_length(key_graph, '@', target, 'weight')
    return path_length

class TestPathFinding(unittest.TestCase):

    def test_find_position(self):
        area_map = """#########
                      #b.A.@.a#
                      #########"""
        position = find_position(area_map, '@')
        self.assertEqual((1, 5), position)

    def test_list_accessible_keys_simplest(self):
        area_map = """#########
                      #b.A.@.a#
                      #########"""
        expected_keys = {'a': 2}
        keys = list_accessible_keys(area_map)
        self.assertEqual(expected_keys, keys)

    def test_find_all_key_positions_simplest(self):
        area_map = """#########
                      #b.A.@.a#
                      #########"""
        expected_positions = {'a': (1, 7), 'b':(1, 1)}
        positions = find_all_key_positions(area_map)
        self.assertEqual(expected_positions, positions)

    def test_find_path_edges(self):
        area_map = """#########
                      #b.A.@.a#
                      #########"""
        exp_edges = {((1, 1), (1, 2)), ((1, 4), (1, 5)), ((1, 5), (1, 6)),
                     ((1, 6), (1, 7))}
        self.run_find_path_edges_test(area_map, exp_edges)

    def test_find_path_edges_two(self):
        area_map = """#########
                      #b.A.@.a#
                      #..#.####
                      #########"""
        exp_edges = {((1, 1), (1, 2)), ((1, 4), (1, 5)), ((1, 5), (1, 6)),
                     ((1, 6), (1, 7)), ((2, 1), (2, 2)), ((1, 1), (2, 1)),
                     ((1, 2), (2, 2)), ((1, 4), (2, 4))}
        self.run_find_path_edges_test(area_map, exp_edges)

    def run_find_path_edges_test(self, area_map, exp_edges):
        edges = find_path_edges(area_map)
        self.assertEqual(exp_edges, edges)

    def test_distance_to_keys_simplest(self):
        area_map = """#########
                      #b.A.@.a#
                      #########"""
        exp_result = {'a' : 2}
        distances = distance_to_keys(area_map)
        self.assertEqual(exp_result, distances)

    def test_pick_up_key(self):
        area_map = """#########
                      #b.A.@.a#
                      #########"""
        expected = """#########
                      #b.....@#
                      #########"""
        result = pick_up_key(area_map, 'a')
        self.assertEqual(expected, result)

    def test_create_decision_tree_edges(self):
        area_map = """#########
                      #b.A.@.a#
                      #########"""
        expected_edges = {('@', '@a', 2), ('@a', '@ab', 6)}
        edges = create_decision_tree_edges(area_map,'@')
        self.assertEqual(expected_edges, edges)

    def test_distance(self):
        area_map = """#########
                      #b.A.@.a#
                      #########"""
        self.run_distance_test(area_map, 8)

    def run_distance_test(self, area_map, expected):
        distance = find_dist_to_all_keys(area_map)
        self.assertEqual(expected, distance)

    def test_distance_two(self):
        area_map = """########################
                      #f.D.E.e.C.b.A.@.a.B.c.#
                      ######################.#
                      #d.....................#
                      ########################"""
        self.run_distance_test(area_map, 86)

    def test_part_one(self):
        with open('day18_input.txt') as infile:
            area_map = infile.read()
        self.run_distance_test(area_map, 100)


if __name__ == '__main__':
    unittest.main()

import networkx as nx
import unittest

def count_orbital_transfers(orbit_map):
    orbit_graph = nx.Graph()
    for record in orbit_map:
        orbited, orbiter = record.split(')')
        orbit_graph.add_edge(orbited, orbiter)
    path = nx.shortest_path(orbit_graph, 'YOU', 'SAN')
    return len(path) - 3

def get_orbit_counts(orbit_map):
    orbit_dict = {}
    for record in orbit_map:
        orbited, orbiter = record.split(')')
        orbit_dict[orbiter] = orbited
    result = {'COM' : 0}
    result = add_all_that_orbit('COM', orbit_dict, result)
    return result

def add_all_that_orbit(orbited, orbit_dict, result):
    orbits_this = [key for key, val in orbit_dict.items() if val==orbited]
    for orbiter in orbits_this:
        result[orbiter] = result[orbited] + 1
        add_all_that_orbit(orbiter, orbit_dict, result)
    return result

def load_file(filename):
    with open(filename) as input_file:
        result = input_file.read().splitlines()
    return result

class TestOrbit(unittest.TestCase):
    def test_orbit_counts(self):
        test_data = ['COM)B',
                     'B)C',
                     'C)D',
                     'D)E',
                     'E)F',
                     'B)G',
                     'G)H',
                     'D)I',
                     'E)J',
                     'J)K',
                     'K)L']
        counts = get_orbit_counts(test_data)
        self.assertEqual(3, counts['D'])
        self.assertEqual(7, counts['L'])
        self.assertEqual(42, sum(counts.values()))

    def test_load_file(self):
        result = load_file('day6_input.txt')
        self.assertEqual('PJK)X3G', result[0])
        self.assertEqual('ZM3)JGN', result[1])
        self.assertEqual('NTG)MFS', result[-1])

    def test_right_answer(self):
        orbit_map = load_file('day6_input.txt')
        counts = get_orbit_counts(orbit_map)
        self.assertEqual(106065, sum(counts.values()))

    def test_count_orbital_transfers(self):
        test_data = ['COM)B',
                     'B)C',
                     'C)D',
                     'D)E',
                     'E)F',
                     'B)G',
                     'G)H',
                     'D)I',
                     'E)J',
                     'J)K',
                     'K)L',
                     'K)YOU',
                     'I)SAN']
        result = count_orbital_transfers(test_data)
        self.assertEqual(4, result)

    def test_right_answer_part_two(self):
        orbit_map = load_file('day6_input.txt')
        result = count_orbital_transfers(orbit_map)
        self.assertEqual(253, result)

if __name__ == '__main__':
    unittest.main()

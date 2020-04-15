import unittest
from collections import defaultdict
import math

def calculate_fuel_for_one_trillion(reactions):
    react = convert_to_dict(reactions)
    trillion = 1000000000000
    lower_limit = 0
    upper_limit = int(trillion/max(react['FUEL'][1].values()))
    while lower_limit < upper_limit:
        halfway = int((lower_limit + upper_limit)/2)
        required = calculate_required_ore(react, halfway)
        if required < trillion:
            lower_limit = halfway + 1
        else:
            upper_limit = halfway - 1
    required = calculate_required_ore(react, lower_limit)
    if required < trillion:
        result = lower_limit
    else:
        result = lower_limit - 1
    return result


def calculate_required_ore(react, required_fuel=1):
    #react = convert_to_dict(reactions)
    requirements = defaultdict(int)
    requirements['FUEL'] = required_fuel
    while (get_requirements_to_fill(requirements)):
        fill_one_requirement(requirements, react)
    return requirements['ORE']

def fill_one_requirement(requirements, reactions):
    to_fill = get_requirements_to_fill(requirements)
    product = to_fill.pop()
    output_amount, reactants = reactions[product]
    n = int(math.ceil(requirements[product] / output_amount))
    for name, amount in reactants.items():
        requirements[name] = requirements[name] + n * amount
    requirements[product] = requirements[product] - n * output_amount

def get_requirements_to_fill(requirements):
    result = [key for key, val in requirements.items() if key!='ORE' and val>0]
    return result

def get_requirements(reactions, product, requirements):
    output_amount, reactants = reactions[product]
    for name, amount in reactants.items():
        requirements[name] = requirements[name] + amount
    return requirements

def convert_to_dict(reactions):
    result = {}
    for reaction in reactions.splitlines():
        reactants, product = reaction.split('=>')
        product_amount, product_name = product.split()
        reactant_dict = {}
        for reactant in reactants.split(','):
            reactant_amount, reactant_name = reactant.split()
            reactant_dict[reactant_name] = int(reactant_amount)
        result[product_name] = (int(product_amount), reactant_dict)
    return result


class TestNanoFactory(unittest.TestCase):
    def test_calculate_required_ore(self):
        reactions = """10 ORE => 10 A
                        1 ORE => 1 B
                        7 A, 1 B => 1 C
                        7 A, 1 C => 1 D
                        7 A, 1 D => 1 E
                        7 A, 1 E => 1 FUEL"""
        ore = calculate_required_ore(reactions)
        self.assertEqual(31, ore)

    def test_convert_to_dict(self):
        reactions = """10 ORE => 10 A
                        1 ORE => 1 B
                        7 A, 1 B => 1 C
                        7 A, 1 C => 1 D
                        7 A, 1 D => 1 E
                        7 A, 1 E => 1 FUEL"""
        expected_result = {'A': (10, {'ORE': 10}),
                           'B': (1, {'ORE': 1}),
                           'C': (1, {'A': 7, 'B': 1}),
                           'D': (1, {'A': 7, 'C': 1}),
                           'E': (1, {'A': 7, 'D': 1}),
                           'FUEL': (1, {'A': 7, 'E': 1})}
        result = convert_to_dict(reactions)
        self.assertEqual(expected_result, result)

    def test_part_one(self):
        with open('day14_input.txt') as input_file:
            reactions = input_file.read()
        ore = calculate_required_ore(reactions)
        self.assertEqual(907302, ore)

    def test_one_trillion(self):
        reactions = """157 ORE => 5 NZVS
                        165 ORE => 6 DCFZ
                        44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
                        12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
                        179 ORE => 7 PSHF
                        177 ORE => 5 HKGWZ
                        7 DCFZ, 7 PSHF => 2 XJWVT
                        165 ORE => 2 GPVTF
                        3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""
        result = calculate_fuel_for_one_trillion(reactions)
        self.assertEqual(82892753, result)

    def test_part_two(self):
        with open('day14_input.txt') as input_file:
            reactions = input_file.read()
        result = calculate_fuel_for_one_trillion(reactions)
        self.assertEqual(1670299, result)

if __name__ == '__main__':
    unittest.main()

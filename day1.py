import unittest
import pandas as pd

def calculate_fuel(mass):
    initial_fuel = mass // 3 - 2
    if initial_fuel <= 0:
        return 0
    return initial_fuel + calculate_fuel(initial_fuel)

def load_data():
    data = pd.read_csv('input_data.txt', squeeze=True, header=None)
    return data

def calculate_sum():
    data = load_data()
    module_fuels = data.apply(calculate_fuel)
    result = module_fuels.sum()
    return result

class TestFuelCalc(unittest.TestCase):

    def run_fuel_test(self, mass, fuel):
        result = calculate_fuel(mass)
        self.assertEqual(fuel, result)

    def test_calculate_sum(self):
        result = calculate_sum()
        self.assertEqual(5105716, result)

    def test_calculate_fuel(self):
        self.run_fuel_test(12, 2)
        self.run_fuel_test(14, 2)
        self.run_fuel_test(1969, 966)
        self.run_fuel_test(100756, 50346)

    def test_load_data(self):
        result = load_data()
        self.assertEqual(result.iloc[0], 124846)
        self.assertEqual(result.iloc[1], 99745)
        self.assertEqual(result.iloc[-1], 51323)


if __name__ == '__main__':
    main()

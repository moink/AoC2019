import unittest
import numpy as np
import pandas as pd
from pandas.util.testing import assert_frame_equal, assert_series_equal
import matplotlib.pyplot as plt

def read_data(filename):
    with open(filename) as in_file:
        result = in_file.read()
    return result

def decompose_layers(input_val, shape):
    new_shape = (-1, shape[1], shape[0])
    digits = np.asarray([int(char) for char in input_val])
    interim = digits.reshape(new_shape)
    result = {}
    for i, layer in enumerate(interim, start=1):
        result[i] = pd.DataFrame(index=range(shape[1]), columns=range(shape[0]),
                                 data=layer, dtype='int64')
    return result

def get_value_counts(layers):
    result = {}
    min_value = min((layer.min().min() for layer in layers.values()))
    max_value = max((layer.max().max() for layer in layers.values()))
    for key, layer in layers.items():
        result[key] = pd.Series(index=range(min_value, max_value+1), data=0)
        for col in layer.columns:
            result[key] = result[key].add(layer[col].value_counts(),
                                          fill_value=0)
        result[key] = result[key].astype('int64')
    return result

def stack_layers(layers):
    order = sorted(list(layers.keys()), reverse=True)
    result = layers[order[0]]
    for layer_number in order[1:]:
        layer = layers[layer_number]
        layer.replace(2, np.nan, inplace=True)
        result.update(layer)
    result = result.astype('int64')
    return result

def display_image(filename, shape):
    input_data = read_data(filename)
    layers = decompose_layers(input_data, shape)
    result = stack_layers(layers)
    plt.imshow(result)
    plt.show()

class TestImage(unittest.TestCase):
    def test_decompose_layers(self):
        input_val = '123456789012'
        shape = (3, 2)
        expected_result ={1: pd.DataFrame([[1,2,3], [4,5,6]]),
                          2: pd.DataFrame([[7,8,9], [0,1,2]])}
        result = decompose_layers(input_val, shape)
        for key, val in expected_result.items():
            assert_frame_equal(val, result[key])

    def test_get_value_counts(self):
        layers ={1: pd.DataFrame([[1,2,3], [4,5,6]]),
                 2: pd.DataFrame([[7,8,9], [0,1,2]])}
        result = get_value_counts(layers)
        expected_result = {
            1: pd.Series(index=range(10), data=[0, 1, 1, 1, 1, 1, 1, 0, 0, 0]),
            2: pd.Series(index=range(10), data=[1, 1, 1, 0, 0, 0, 0, 1, 1, 1])}
        for key, val in expected_result.items():
            assert_series_equal(val, result[key])

    def test_read_data(self):
        result = read_data('day8_input.txt')
        self.assertEqual('2', result[0])
        self.assertEqual('2', result[1])
        self.assertEqual('1', result[2])
        self.assertEqual('0', result[-1])

    def test_right_answer(self):
        data = read_data('day8_input.txt')
        layers = decompose_layers(data, (25, 6))
        counts = get_value_counts(layers)
        zeros = {count[0]:layer for layer, count in counts.items()}
        min_zero_layer = zeros[min(zeros.keys())]
        ones = counts[min_zero_layer][1]
        twos = counts[min_zero_layer][2]
        result = ones * twos
        self.assertEqual(1064, result)

    def test_stack_layers(self):
        layers = {1: pd.DataFrame([[0, 2], [2, 2]]),
                  2: pd.DataFrame([[1, 1], [2, 2]]),
                  3: pd.DataFrame([[2, 2], [1, 2]]),
                  4: pd.DataFrame([[0, 0], [0, 0]])}
        expected_result = pd.DataFrame([[0, 1], [1, 0]])
        result = stack_layers(layers)
        assert_frame_equal(expected_result, result)

    def test_display_image(self):
        result = display_image('day8_input.txt', (25, 6))
if __name__ == '__main__':
    unittest.main()

from collections import defaultdict

import numpy as np
from matplotlib import pyplot as plt


def load_grid(filename, chars = None):
    if chars is None:
        chars = {0: '.', 1: '#'}
    arr = []
    with open(filename) as infile:
        lines = infile.readlines()
    for line in lines:
        arr.append([])
        for char in line:
            for key, val in chars.items():
                if char in val:
                    arr[-1].append(key)
    return np.asarray(arr)


def show_grid(grid):
    plt.clf()
    plt.imshow(grid)
    plt.show()


def draw_grid(grid):
    plt.clf()
    plt.imshow(grid)
    plt.draw()
    plt.pause(0.001)


def dict_from_file(filename, sep = ' => ', key='left'):
    result = {}
    with open(filename) as infile:
        lines = infile.readlines()
    for line in lines:
        left, right = line.split(sep)
        if key == 'left':
            result[left.strip()] = right.strip()
        else:
            result[right.strip()] = left.strip()
    return result

def dict_of_list_from_file(filename, sep = ' => ', key='left'):
    result = defaultdict(list)
    with open(filename) as infile:
        lines = infile.readlines()
    for line in lines:
        left, right = line.split(sep)
        if key == 'left':
            result[left.strip()].append(right.strip())
        else:
            result[right.strip()].append(left.strip())
    return dict(result)

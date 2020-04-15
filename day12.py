import unittest
import numpy as np
from numpy.testing import assert_array_equal
from itertools import combinations

class MoonSimulation:
    def __init__(self, init_position):
        self.position = np.asarray(init_position)
        self.velocity = np.zeros(self.position.shape, dtype=int)
        self.init_position = self.position.copy()
        self.init_velocity = self.velocity.copy()

    def apply_one_step(self):
        self.apply_gravity()
        self.apply_velocity()

    def apply_gravity(self):
        for index1, index2 in combinations(range(len(self.velocity)), 2):
            moon1 = self.position[index1]
            moon2 = self.position[index2]
            gravity = self.calculate_gravity(moon1, moon2)
            self.velocity[index1] = self.velocity[index1] + gravity
            self.velocity[index2] = self.velocity[index2] - gravity

    def apply_velocity(self):
        self.position = self.position + self.velocity

    @staticmethod
    def calculate_gravity(moon1, moon2):
        result = np.zeros(moon1.shape)
        for index, (x1, x2) in enumerate(zip(moon1, moon2)):
            if x2 > x1:
                direction = 1
            elif x2 < x1:
                direction = -1
            else:
                direction = 0
            result[index] = direction
        return result

    def apply_steps(self, n_steps):
        for step in range(n_steps):
            self.apply_one_step()

    @property
    def total_energy(self):
        potential = np.abs(self.position).sum(axis=1)
        kinetic = np.abs(self.velocity).sum(axis=1)
        total = potential * kinetic
        return total.sum()

    def calculate_loop_length(self):
        self.apply_one_step()
        steps = 1
        while not(self.initial_state_reached()):
            self.apply_one_step()
            steps = steps + 1
            if steps % 10000 == 0:
                print(steps)
        return steps

    def initial_state_reached(self):
        return ((self.position == self.init_position).all()
                and (self.velocity == self.init_velocity).all())

class TestMoonSimulation(unittest.TestCase):
    def test_one_step(self):
        sim = MoonSimulation([[-1, 0, 2],
                              [2, -10, -7],
                              [4, -8, 8],
                              [3, 5, -1]])
        sim.apply_one_step()
        exp_pos = np.asarray([[2, -1, 1],
                              [3, -7, -4],
                              [1, -7, 5],
                              [2, 2, 0]])
        exp_vel = np.asarray([[3, -1, -1],
                              [1, 3, 3],
                              [-3, 1, -3],
                              [-1, -3, 1]])
        assert_array_equal(exp_pos, sim.position)
        assert_array_equal(exp_vel, sim.velocity)

    def test_calculate_gravity(self):
        ganymede = np.asarray([3])
        callisto = np.asarray([5])
        gravity = MoonSimulation.calculate_gravity(ganymede, callisto)
        assert_array_equal(np.asarray([1]), gravity)

    def test_ten_steps(self):
        sim = MoonSimulation([[-1, 0, 2],
                              [2, -10, -7],
                              [4, -8, 8],
                              [3, 5, -1]])
        sim.apply_steps(10)
        exp_pos = np.asarray([[2, 1, -3],
                              [1, -8, 0],
                              [3, -6, 1],
                              [2, 0, 4]])
        exp_vel = np.asarray([[-3, -2, 1],
                              [-1, 1, 3],
                              [3, 2, -3],
                              [1, -1, -1]])
        assert_array_equal(exp_pos, sim.position)
        assert_array_equal(exp_vel, sim.velocity)

    def test_total_energy(self):
        sim = MoonSimulation([[-1, 0, 2],
                              [2, -10, -7],
                              [4, -8, 8],
                              [3, 5, -1]])
        sim.apply_steps(10)
        energy = sim.total_energy
        self.assertEqual(179, energy)

    def test_right_answer_part_one(self):
        sim = MoonSimulation([[-1, -4, 0],
                              [4, 7, -1],
                              [-14, -10, 9],
                              [1, 2, 17]])
        sim.apply_steps(1000)
        energy = sim.total_energy
        self.assertEqual(7988, energy)

    def test_calculate_loop_length(self):
        sim = MoonSimulation([[-1, 0, 2],
                              [2, -10, -7],
                              [4, -8, 8],
                              [3, 5, -1]])
        loop = sim.calculate_loop_length()
        self.assertEqual(2772, loop)

    # def test_right_answer_part_two(self):
    #     sim = MoonSimulation([[-1, -4, 0],
    #                           [4, 7, -1],
    #                           [-14, -10, 9],
    #                           [1, 2, 17]])
    #     loop = sim.calculate_loop_length()
    #     self.assertEqual(2772, loop)

    def test_right_answer_part_two_z(self):
        sim = MoonSimulation([[0],
                              [-1],
                              [9],
                              [17]])
        loop = sim.calculate_loop_length()
        self.assertEqual(60424, loop)

    def test_right_answer_part_two_x(self):
        sim = MoonSimulation([[-1],
                              [4],
                              [-14],
                              [1]])
        loop = sim.calculate_loop_length()
        self.assertEqual(231614, loop)

    def test_right_answer_part_two_y(self):
        sim = MoonSimulation([[-4],
                              [7],
                              [-10],
                              [2]])
        loop = sim.calculate_loop_length()
        self.assertEqual(193052, loop)

    def test_lcm(self):
        ans1 = np.lcm(60424, 231614)
        ans = np.lcm(ans1, 193052)
        expected = 337721412394184
        self.assertEqual(0, expected % 60424)
        self.assertEqual(0, expected % 231614)
        self.assertEqual(0, expected % 193052)

if __name__ == '__main__':
    unittest.main()

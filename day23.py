import unittest
from intcode import Computer


def run_network():
    with open('day23_input.txt') as infile:
        program = list(map(int, infile.read().split(',')))
    computers = {}
    programs = {}
    for address in range(50):
        computer = Computer(program)
        computer.set_input([address])
        computers[address] = computer
        programs[address] = computer.run_program()
    messages = {address : [] for address in range(50)}
    nat_value = None
    nat_y_sent = set()
    while True:
        for address, program in programs.items():
            output = next(program)
            if output is not None:
                messages[address].append(output)
                if len(messages[address]) == 3:
                    destination, x, y = messages.pop(address)
                    if destination == 255:
                        nat_value = (x, y)
                    else:
                        computers[destination].set_input((x, y))
                    messages[address] = []
            idle = all(len(computer.inputs) == 0
                       for computer in computers.values())
            if idle and nat_value:
                computers[0].set_input(nat_value)
                y = nat_value[1]
                if y in nat_y_sent:
                    return y
                nat_y_sent.add(y)
                nat_value = None


class TestNetwork(unittest.TestCase):
    def test_run_network(self):
        result = run_network()
        self.assertEqual(14370, result)


if __name__ == '__main__':
    unittest.main()

from itertools import combinations

from day15 import Computer
from string import Template


def create_drop_commands(to_drop):
    return '\n'.join('drop ' + item for item in to_drop)


def run_dropping(to_drop):
    with open('day25_results/input.txt') as infile:
        command_template = infile.read()
    drop_commands = create_drop_commands(to_drop)
    temp = Template(command_template)
    commands = temp.substitute(drop_commands=drop_commands)
    inputs = [ord(char) for char in commands]
    with open('day25.txt') as infile:
        program = list(map(int, infile.read().split(',')))
    computer = Computer(program)
    computer.set_input(inputs)
    count = 0
    result = []
    try:
        for output in computer.run_program():
            count = count + 1
            display = chr(output)
            result.append(display)
    except IndexError:
        return ''.join(result)
    return ''.join(result)


def parse_output(output):
    for line in output.splitlines():
        if line.startswith('A loud, robotic voice'):
            if 'heavier' in line:
                return -1, line
            elif 'lighter' in line:
                return 1, line
    return 0, output


def main():
    can_drop = {'dark matter', 'hologram', 'astrolabe', 'whirled peas',
                'klein bottle', 'candy cane', 'tambourine', 'ornament'}
    tested = {}
    for num_carry in range(9):
        print(num_carry + 1)
        for keep in combinations(can_drop, num_carry + 1):
            print('.', end='')
            output = run_dropping(can_drop.difference(keep))
            result, line = parse_output(output)
            if result == 0:
                print(line)
                return
            tested[frozenset(keep)] = result
    print(tested)


if __name__ == '__main__':
    main()
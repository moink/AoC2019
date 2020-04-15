from day15 import Computer


def run_springboard_program(asc):
    inputs = [ord(char) for char in asc]
    with open('day21.txt') as infile:
        program = list(map(int, infile.read().split(',')))
    computer = Computer(program)
    computer.set_input(inputs)
    output = list(computer.run_program())
    try:
        display = ''.join(chr(code) for code in output)
    except ValueError:
        display = ''.join(chr(code) for code in output[:-1]) + str(output[-1])
    return display


def run_with_files(input_file='day21_results/input.txt',
                   output_file='day21_results/output.txt'):
    with open(input_file) as infile:
        program = infile.read()
    display = run_springboard_program(program)
    with open(output_file, 'w') as outfile:
        outfile.write(display)


if __name__ == '__main__':
    run_with_files()

def part2(data):
    offset = int(''.join(map(str, data[:7])))
    data = (data*10000)[offset:]
    for _ in range(100):
        suffix_sum = 0
        for i in range(len(data)-1, -1, -1):
            suffix_sum = (suffix_sum + data[i]) % 10
            data[i] = suffix_sum
    return ''.join(map(str, data[:8]))

if __name__ == '__main__':
    with open('day16_input.txt') as infile:
        data = list(map(int, infile.read()))
    print(part2(data))


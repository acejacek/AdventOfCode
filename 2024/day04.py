import numpy as np

def scan_line(line):
    count = line.count("XMAS")
    reverse = line[::-1]
    count += reverse.count("XMAS")
    return count


def transpose_array(a):
    width = len(a[0])
    b = [""] * width
    for line in a:
        for i in range(width):
            b[i] += line[i]
    return b


def get_diagonal(a):
    count = 0
    width = len(a[0])
    for offset in range(-width, width):
        string = ""
        for x in range(width):
            y = x + offset
            if y < width and y >= 0:
                string += a[x][y]

        res = scan_line(string)
        count += res

    for x in range(0, 2 * width):
        string = ""
        y = 0
        for offset in range(0, width):
            tx = x - offset
            ty = y + offset
            if tx >= 0 and tx < width and ty  >=0 and ty < width:
                string += a[tx][ty]

        res = scan_line(string)
        count += res

    return count

def print_a(a):
    for line in a:
        print(line)


def calculate_sum(a):
    count = 0
    # count horizontal
    for line in a:
        count += scan_line(line)

    # count vertical
    a = transpose_array(a)
    for line in a:
        count += scan_line(line)

    # count diagonal
    count += get_diagonal(a)

    return count

a = np.loadtxt("day04.test", dtype=str)
assert calculate_sum(a) == 18

a = np.loadtxt("day04.txt", dtype=str)
print("Part 1:", calculate_sum(a))


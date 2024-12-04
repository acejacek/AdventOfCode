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

def peek(a, x, y):
    w = len(a[0])
    if x < 0 or y < 0 or x >= w or y >= w:
        return 'outOfRange'
 
    return a[y][x]

"""
x1,y1    x2,y2
   MS   MS
     \ /
      A
     / \
   MS   MS
x4,y4    x3,y3
"""
def is_it_MAS(a, xs, y):
    found = 0
    for x in xs:
        x1 = x - 1
        y1 = y - 1

        x2 = x + 1
        y2 = y - 1
        
        x3 = x + 1
        y3 = y + 1
        
        x4 = x - 1
        y4 = y + 1

        NW = 0
        SE = 0
        if (peek(a, x1, y1) == 'M' and peek(a, x3, y3) == 'S') or \
            (peek(a, x1, y1) == 'S' and peek(a, x3, y3) == 'M'):
            NW = 1
        if (peek(a, x2, y2) == 'M' and peek(a, x4, y4) == 'S') or \
            (peek(a, x2, y2) == 'S' and peek(a, x4, y4) == 'M'):
            SE = 1

        if NW == SE == 1:
            found += 1

    return found

def find_A(a):
    found = 0
    y = 0
    for line in a:
        posA = [x for x, letter in enumerate(line) if letter == "A"] # find letter A
        found += is_it_MAS(a, posA, y)  # scan, if it's X-MAS around it
        y += 1

    return found


a = np.loadtxt("day04.test", dtype=str)
assert calculate_sum(a) == 18
assert find_A(a) == 9

a = np.loadtxt("day04.txt", dtype=str)
print("Part 1:", calculate_sum(a))
print("Part 2:", find_A(a))

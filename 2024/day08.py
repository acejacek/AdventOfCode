#!/usr/bin/env python3
def calculate(filename, part = 1):

    def findFreq(f):
        locations = []
        for y, line in enumerate(lines):
            if f in line:
                locations += ([complex(x, y) for x, loc in enumerate(line) if loc == f])
        return locations
                
    def findAntinode(a, b):
        if a != b:
            # calculate delta
            delta = a - b
            # antinode position of A due to interference with B
            newA = a + delta
            if newA.real >= 0 and newA.real < w and newA.imag >= 0 and newA.imag < h:
                return newA

    def findAntinodeWithHarmonics(a, b):
        nodes = []
        if a != b:
            delta = a - b
            # generate antinodes at antenna and every delta until out of bounds
            newA = a
            while newA.real >= 0 and newA.real < w and newA.imag >= 0 and newA.imag < h:
                nodes += [newA]
                newA += delta
        return nodes

    with open(filename, "r") as file:
        lines = file.readlines()

    w = len(lines[0]) - 1
    h = len(lines)
    antinodes = set()
    antennas = []

    # where are antennas?
    for y, line in enumerate(lines):
        antennas += [(x, y, ant) for x, ant in enumerate(line) if (ant != "." and ant != "\n")]

    for antenna in antennas:
        source = complex(antenna[0], antenna[1])
        # generate list of same frequency antennas
        others = findFreq(antenna[2])
        # find antinodes and add to the set
        for other in others:
            if part == 1:
                antinodes.add(findAntinode(source, other))
            if part == 2:
                for node in findAntinodeWithHarmonics(source, other):
                    antinodes.add(node)

    antinodes.discard(None)
    return len(antinodes)


assert calculate("day08.test") == 14
print("Part 1:", calculate("day08.txt"))

assert calculate("day08.test", part = 2) == 34
print("Part 2:", calculate("day08.txt", part = 2))


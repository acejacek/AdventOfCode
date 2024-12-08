
def calculate(filename, part = 1):

    def findFreq(f):
        y = 0
        locations = []
        for line in lines:
            if f in line:
                locations += ([(x, y) for x, loc in enumerate(line) if loc == f])
            y += 1
        return locations
                
    def findAntinode(a, b):
        if a != b:
            dx = a[0] - b[0]
            dy = a[1] - b[1]
            newAx = a[0] + dx
            newAy = a[1] + dy
            if newAx >= 0 and newAx < w and newAy >= 0 and newAy < h:
                return (newAx, newAy)
        return

    def findAntinodeWithHarmonics(a, b):
        nodes = []
        if a != b:
            dx = a[0] - b[0]
            dy = a[1] - b[1]

            newAx = a[0]
            newAy = a[1]

            while newAx >= 0 and newAx < w and newAy >= 0 and newAy < h:
                nodes += [(newAx, newAy)]
                newAx += dx
                newAy += dy

        return nodes


    with open(filename, "r") as file:
        lines = file.readlines()

    w = len(lines[0]) - 1
    h = len(lines)
    antinodes = set()
    """
    findAntinodeWithHarmonics((1,2),(0,0))
    findAntinodeWithHarmonics((3,1),(0,0))
    findAntinodeWithHarmonics((3,1),(1,2))
    exit()
    """
    y = 0
    antenas = []
    for line in lines:
        antenas += [(x, y, ant) for x, ant in enumerate(line) if (ant != "." and ant != "\n")]
        y += 1

    for antena in antenas:
        others = findFreq(antena[2])
        for other in others:
            if part == 1:
                antinodes.add(findAntinode((antena[0], antena[1]), other))
            if part == 2:
                for node in findAntinodeWithHarmonics((antena[0], antena[1]), other):
                    antinodes.add(node)

    antinodes.discard(None)
    return len(antinodes)


assert calculate("day08.test") == 14
print("Part 1:", calculate("day08.txt"))

assert calculate("day08.test", part = 2) == 34
print("Part 2:", calculate("day08.txt", part = 2))


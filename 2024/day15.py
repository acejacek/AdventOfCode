#!/usr/bin/env python3

class Wall:
    def __init__(self, pos):
        self.pos = pos

class Box:
    def __init__(self, pos):
        self.pos = pos

    def gpsCoord(self):
        return self.pos[1] * 100 + self.pos[0]

    def colide(self, pos):
        return self.pos == pos

    def move(self, direction):
        if direction == ">":
            newPos = (self.pos[0] + 1, self.pos[1])
        elif direction == "<":
            newPos = (self.pos[0] - 1, self.pos[1])
        elif direction == "v":
            newPos = (self.pos[0], self.pos[1] + 1)
        else:
            newPos = (self.pos[0], self.pos[1] - 1)

        for wall in walls:
            if wall.pos == newPos:
                return False

        for box in boxes:
            if box.colide(newPos):
                if not box.move(direction):
                    return False
        self.pos = newPos
        return True

class Robot(Box):
    pass

class WideBox(Box):

    def __init__(self, pos):
        self.pos = pos
        self.half = (pos[0] + 1, pos[1])

    def colide(self, pos):
        return self.pos == pos or self.half == pos

    def move(self, direction):
        if direction == ">":
            newPos = (self.pos[0] + 1, self.pos[1])
        elif direction == "<":
            newPos = (self.pos[0] - 1, self.pos[1])
        elif direction == "v":
            newPos = (self.pos[0], self.pos[1] + 1)
        else:
            newPos = (self.pos[0], self.pos[1] - 1)

        newHalf = (newPos[0] + 1, newPos[1])

        for wall in walls:
            if wall.pos == newPos or wall.pos == newHalf:
                return False

        for box in boxes:
            if box.pos == self.pos: continue
            if box.colide(newPos) or box.colide(newHalf):
                if not box.move(direction):
                    return False
        self.pos = newPos
        self.half = newHalf
        return True

def calculate(filename, part = 1):

    global walls
    walls = []
    global boxes
    boxes = []
    moveLoad = False
    y = 0
    movements = ""
    robot = 0

    with open(filename, "r") as file:
        while line := file.readline():
            if line == "\n":
                moveLoad = True
                continue

            if moveLoad:
                movements += line
            else:
                if part == 1:
                    for x, elem in enumerate(line):
                        if elem == "#":
                            walls += [Wall((x, y))]
                        if elem == "O":
                            boxes += [Box((x, y))]
                        if elem == "@":
                            robot = Robot((x, y))
                else:
                    for x, elem in enumerate(line):
                        x *= 2
                        if elem == "#":
                            walls += [Wall((x, y))]
                            walls += [Wall((x + 1, y))]
                        if elem == "O":
                            boxes += [WideBox((x, y))]
                        if elem == "@":
                            robot = Robot((x, y))
                y += 1

    for move in movements:
        if move != "\n":
            robot.move(move)

    return sum([box.gpsCoord() for box in boxes])

assert calculate("day15.test") == 2028
assert calculate("day15.test2") == 10092
a = calculate("day15.txt")
print("Part 1:", a)

assert calculate("day15.test3", part = 2) == 618
assert calculate("day15.test2", part = 2) == 9021
a = calculate("day15.txt", part = 2)
print("Part 2:", a)

#!/usr/bin/env python3

class Box:
    def __init__(self, pos):
        self.pos = pos

    def gpsCoord(self):
        return self.pos[1] * 100 + self.pos[0]

    def colide(self, pos):
        return self.pos == pos

    def move(self, direction, check = False):
        if direction == ">":
            newPos = (self.pos[0] + 1, self.pos[1])
        elif direction == "<":
            newPos = (self.pos[0] - 1, self.pos[1])
        elif direction == "v":
            newPos = (self.pos[0], self.pos[1] + 1)
        else:
            newPos = (self.pos[0], self.pos[1] - 1)

        for wall in walls:
            if wall == newPos:
                return False

        for box in boxes:
            if box.pos == self.pos: continue
            if box.colide(newPos):
                if not box.move(direction, check):
                    return False

        if not check:
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

    def move(self, direction, check = False):
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
            if wall == newPos or wall == newHalf:
                return False

        for box in boxes:
            if box.pos == self.pos: continue
            if box.colide(newPos) or box.colide(newHalf):
                if not box.move(direction, check):
                    return False

        if not check:
            self.pos = newPos
            self.half = newHalf
        return True

def calculate(filename, part = 1):

    global walls
    global boxes
    walls = set()
    boxes = set()
    moveLoad = False
    movements = ""

    with open(filename, "r") as file:
        y = 0
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
                            walls.add((x, y))
                        if elem == "O":
                            boxes.add(Box((x, y)))
                        if elem == "@":
                            robot = Robot((x, y))
                else:
                    for x, elem in enumerate(line):
                        x *= 2
                        if elem == "#":
                            walls.add((x, y))
                            walls.add((x + 1, y))
                        if elem == "O":
                            boxes.add(WideBox((x, y)))
                        if elem == "@":
                            robot = Robot((x, y))
                y += 1  

    for direction in movements:
        if direction != "\n":

            if part == 1:
                robot.move(direction)

            # for part 2 i need to implement two pases for movement
            else:
                # firstly only checks, if movement is possible. In some cases 
                # for movements up/down only part stacked of boxes can be moved
                # wchich gives false reading, that total movement is possible
                if robot.move(direction, check = True):
                    robot.move(direction)
            """otherwise thias happens:
              stage 1   stage 2
               ###      ###[]   <- this moved, because got push (flag "check" prevents that)
                [][]     []     <- this stays, because is blocked
                 []       []    <- this stays still too
                 @        @
                 ^
            """

    return sum([box.gpsCoord() for box in boxes])

assert calculate("day15.test") == 2028
assert calculate("day15.test2") == 10092
a = calculate("day15.txt")
print("Part 1:", a)

assert calculate("day15.test", part = 2) == 1751
assert calculate("day15.test2", part = 2) == 9021
assert calculate("day15.test3", part = 2) == 618
a = calculate("day15.txt", part = 2)
print("Part 2:", a)

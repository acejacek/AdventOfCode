from enum import IntEnum

class Direction(IntEnum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4


class Part1:

    def __init__(self, filename):
        with open(filename, "r") as file:
            self.lines = file.readlines()
        
        self.h = 0;
        for line in self.lines:
            self.w = len(line) - 1   # ignore \n
            if "^" in line:
                self.startx = line.index("^")
                self.starty = self.h

            self.h += 1

        self.reset()
        self.visit()

    def reset(self):
        """bring all to initial stage"""
        self.visited = set()
        self.x = self.startx 
        self.y = self.starty
        self.direction = Direction.NORTH

    def visit(self):
        """add location to visited locations, skip duplicates"""
        self.visited.add((self.x, self.y))

    def print(self):
        """show maze"""
        for line in self.lines:
            print(line.rstrip())

    def isInMaze(self, x, y):
        return x >= 0 and x < self.w and y >= 0 and y < self.h

    def peek(self, x, y):
        """look into location, return what's there. 0 if outsde maze"""
        if self.isInMaze(x, y):
            return self.lines[y][x]

        return 0

    def step(self):
        """ walk in set direction, turn right if obstacle, 0 if out of maze"""
        match self.direction:
            case Direction.NORTH:
                x1 = self.x
                y1 = self.y - 1
                dest = self.peek(x1, y1)
                if dest == 0:         # next step is out of maze
                    return True
                elif dest == "#":     # change dir 90 deg right
                    self.direction = Direction.EAST
                else:
                    self.y -= 1       # walk ahead
                    self.visit()

            case Direction.EAST:
                x1 = self.x + 1
                y1 = self.y
                dest = self.peek(x1, y1)
                if dest == 0:
                    return True
                elif dest == "#":
                    self.direction = Direction.SOUTH
                else:
                    self.x += 1
                    self.visit()

            case Direction.SOUTH:
                x1 = self.x
                y1 = self.y + 1
                dest = self.peek(x1, y1)
                if dest == 0:
                    return True
                elif dest == "#":
                    self.direction = Direction.WEST
                else:
                    self.y += 1
                    self.visit()

            case Direction.WEST:
                x1 = self.x - 1
                y1 = self.y
                dest = self.peek(x1, y1)
                if dest == 0:
                    return True
                elif dest == "#":
                    self.direction = Direction.NORTH
                else:
                    self.x -= 1
                    self.visit()

            case _:
                print("Something wrong with directions")
                exit()
                return

    def walk(self):
        """Walk until exits maze"""
        exitFound = False
        while not exitFound:
            exitFound = self.step()

        return len(self.visited)


class Part2(Part1):

    def __init__(self, filename):
        super().__init__(filename)
        self.reset()  # clears visit of start point inherited from Part1

    def reset(self):
        """bring all to initial stage"""
        super().reset()
        self.obstruction = (-1 , -1)
        self.isLoop = False

    def visit(self):
        """add location to visited locations, set isLoop on revisit"""
        trace = (self.x, self.y, self.direction)
        if trace in self.visited:
            self.isLoop = True
            return

        self.visited.add(trace)

    def peek(self, x, y):
        """look into location, consider obstacles as #. 0 if outsde maze"""
        if not self.isInMaze(x, y):
            return 0

        if (x, y) == (self.obstruction[0], self.obstruction[1]):
            return "#"

        return self.lines[y][x]

    def walk(self):
        """walk until exits maze or steps on own tracks"""
        exitFound = False
        while not exitFound:
            if self.isLoop:
                return 1
            exitFound = self.step()
                
        return 0

    def iterateWalks(self):
        """do walks iterating through all possible obstacles"""
        obstacles = set()
        self.walk() # do the initial walk to get all possible locations
        # it does not make sense to put obstacles anywhere outside initial walk
        for (x, y, _) in self.visited:
            obstacles.add((x, y))

        loops = 0
        for obstacle in obstacles:
            self.reset()
            self.obstruction = obstacle
            loops += self.walk()

        return loops


guard = Part1("day06.test")
assert guard.walk() == 41

guard = Part1("day06.txt")
print("Part 1:", guard.walk())

guard = Part2("day06.test")
assert guard.iterateWalks() == 6

guard = Part2("day06.txt")
print("Part 2:", guard.iterateWalks())


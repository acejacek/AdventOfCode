
class Part1:

    def __init__(self, filename):

        self.lines = []
        self.visited = []
        self.direction = 1

        with open(filename, "r") as file:
            self.lines = file.readlines()
        
        self.h = 0;
        for line in self.lines:
            self.w = len(line) - 1
            if "^" in line:
                self.x = line.index("^")
                self.y = self.h

            self.h += 1

        self.visit()
        self.startx = self.x
        self.starty =  self.y


    def getVisited(self):
        return len(self.visited)


    def visit(self):

        if (self.x, self.y) not in self.visited:
            self.visited.append((self.x, self.y))


    def print(self):
        for line in self.lines:
            print(line.rstrip())

        print(self.x, self.y)
        print(self.visited)
        print(len(self.visited))


    def peek(self, x, y):
        if x >= 0 and x < self.w and y >= 0 and y < self.h:
            return self.lines[y][x]
        else:
            return 0


    def step(self):
        match self.direction:
            case 1:
                x1 = self.x
                y1 = self.y - 1
                dest = self.peek(x1, y1)
                if dest == 0:
                    return True
                elif dest == "#":
                    self.direction = 2
                else:
                    self.y -= 1
                    self.visit()
                return
            case 2:
                x1 = self.x + 1
                y1 = self.y
                dest = self.peek(x1, y1)
                if dest == 0:
                    return True
                elif dest == "#":
                    self.direction = 3
                else:
                    self.x += 1
                    self.visit()
                return
            case 3:
                x1 = self.x
                y1 = self.y + 1
                dest = self.peek(x1, y1)
                if dest == 0:
                    return True
                elif dest == "#":
                    self.direction = 4
                else:
                    self.y += 1
                    self.visit()
                return
            case 4:
                x1 = self.x - 1
                y1 = self.y
                dest = self.peek(x1, y1)
                if dest == 0:
                    return True
                elif dest == "#":
                    self.direction = 1
                else:
                    self.x -= 1
                    self.visit()
                return
            case _:
                return

    def walk(self):
        found = False
        while not found:
            found = self.step()

        return len(self.visited)

class Part2(Part1):

    def __init__(self, filename):
        super().__init__(filename)
        self.trace = []
        self.obstruction = (-1 , -1)

    def traceGuard(self):
        trace = (self.x, self.y, self.direction)
        if trace in self.trace:
            return True

        self.trace.append(trace)
        return False

    def peek(self, x, y):
        if x >= 0 and x < self.w and y >= 0 and y < self.h:
            if x == self.obstruction[0] and y == self.obstruction[1]:
                return "#"

            return self.lines[y][x]
        else:
            return 0

    def setObstruction(self, obstruction):
        if self.lines[obstruction[1]][obstruction[0]] != "#":
            self.obstruction = obstruction;
            return True
        return False

    def walk(self):
        found = False
        while not found:
            found = self.step()
            if not found and self.traceGuard():
                return 1
        return 0

    def reset(self):
        self.trace = []
        self.visited = []
        self.x = self.startx 
        self.y = self.starty
        self.direction = 1


    def iterateWalks(self):
        self.walk() # do the initial walk to get all possible locations
        obstacles = self.visited.copy()
        self.reset()
        loops = 0
        for obstacle in obstacles:
            if self.setObstruction(obstacle):
                loops += self.walk()
            self.reset()

        return loops

g = Part1("day06.test")
assert g.walk() == 41

g = Part1("day06.txt")
print("Part 1:", g.walk())

guard = Part2("day06.test")
assert guard.iterateWalks() == 6

guard = Part2("day06.txt")
print("Part 2:", guard.iterateWalks())


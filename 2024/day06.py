
class Part1:

    def __init__(self, filename):
        self.lines = []

        with open(filename, "r") as file:
            self.lines = file.readlines()
        
        self.h = 0;
        for line in self.lines:
            self.w = len(line) - 1
            if "^" in line:
                self.startx = line.index("^")
                self.starty = self.h

            self.h += 1

        self.reset()
        self.visit()

    def reset(self):
        """bring all to initial stage"""
        self.visited = []
        self.x = self.startx 
        self.y = self.starty
        self.direction = 1

    def visit(self):
        """add location to visited locations, skip duplicates"""
        if (self.x, self.y) not in self.visited:
            self.visited.append((self.x, self.y))


    def print(self):
        """show maze"""
        for line in self.lines:
            print(line.rstrip())


    def peek(self, x, y):
        """look into location, return what's there. 0 if outsde maze"""
        if x >= 0 and x < self.w and y >= 0 and y < self.h:
            return self.lines[y][x]
        else:
            return 0


    def step(self):
        """ walk in 1 = N, 2 = E, 3 = S, 4 = W direction."""
        match self.direction:
            case 1:
                x1 = self.x
                y1 = self.y - 1
                dest = self.peek(x1, y1)
                if dest == 0:         # next step is out of maze
                    return True
                elif dest == "#":     # change dir 90 deg right
                    self.direction = 2
                else:
                    self.y -= 1       # walk ahead
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
                print("Something wrong with directions")
                exit()
                return


    def walk(self):
        """Walk until exits maze"""
        found = False
        while not found:
            found = self.step()

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
        """add location to visited locations, skip duplicates"""
        trace = (self.x, self.y, self.direction)
        if trace in self.visited:
            self.isLoop = True
            return

        self.visited.append(trace)
        

    def peek(self, x, y):
        """look into location, consider obstacles as #. 0 if outsde maze"""
        if x >= 0 and x < self.w and y >= 0 and y < self.h:
            if (x, y) == (self.obstruction[0], self.obstruction[1]):
                return "#"

            return self.lines[y][x]
        else:
            return 0


    def walk(self):
        """walk until exits maze or steps on own tracks"""
        found = False
        while not found:
            found = self.step()
            if not found and self.isLoop:
                return 1
                
        return 0


    def iterateWalks(self):
        """do walks iterating through all possible obstacles"""
        obstacles = []
        self.walk() # do the initial walk to get all possible locations
        # it does not make sense to put obstacles anywhere outside initial walk
        for (x, y, _) in self.visited:
            if (x, y) not in obstacles:
                obstacles.append((x, y))

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


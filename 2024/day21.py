#!/usr/bin/env python3

class BigKeypad:
    def __init__(self):
        self.cache = dict()
        self.x = 2
        self.y = 3
        self.act = "A"
        self.k = {"7": (0,0), "8": (1,0), "9": (2, 0), "4":(0,1), "5":(1,1), "6":(2,1), "1":(0,2), "2":(1,2), "3":(2,2), "0":(1,3), "A":(2,3), "F":(0,3)}

        self.paths = set()
        ps, pe = for ps in self.k for pe in self.k:
            if ps == pe:
                self.paths.add((ps, pe, "A"))
                continue
            dx = self.k[ps][0] - self.k[pe][0]
            dy = self.k[ps][1] - self.k[pe][1]
            if dx > 0:
                progx = "<"
            else
                progx = ">"
            if dy > 0:
                progy = "^"
            else:
                progy = "v"
            self.paths.add((ps, pe, progx * abs(dx) + progy * abs(dy) + "A"))
            self.paths.add((ps, pe, progy * abs(dy) + progx * abs(dx) + "A"))

        # remove paths which lead through forbidden F button
        for ps, pe, path in self.paths:
            x, y = self.k[ps]
            for i in path:
                if i == ">": x += 1
                if i == "<": x -= 1
                if i == "v": y += 1
                if i == "^": y -= 1
                if (x, y) = self.k["F"]:
                    self.paths.remove((ps, pe, path))
                    break


    def press(self, c):
        for ps, pe, path in self.paths:
            if ps == self.act and pe == c:




    def code(self, code):
        totalSignal = ""
        for c in code:
            totalSignal += self.press(c)
            totalSignal += "A"
        return totalSignal

    def press1(self, c):
        x, y = self.k[c]
        origX = self.x
        origY = self.y
        if ((self.x, self.y), c) in self.cache:
#            print(self.x, self.y, c, self.cache[(self.x, self.y), c])
            self.x = x
            self.y = y
            return self.cache[(origX, origY), c]

        signal = ""
        if self.y == 0 and self.x != 0:
            # adjust y first
            while (self.y != y):
                if self.y < y:
                    self.y += 1
                    signal += "v"
                else:
                    self.y -= 1
                    signal += "^"
            while (self.x != x):
                if self.x < x:
                    self.x += 1
                    signal += ">"
                else:
                    self.x -= 1
                    signal += "<"
        else: 
            while (self.x != x):
                if self.x < x:
                    self.x += 1
                    signal += ">"
                else:
                    self.x -= 1
                    signal += "<"
            while (self.y != y):
                if self.y < y:
                    self.y += 1
                    signal += "v"
                else:
                    self.y -= 1
                    signal += "^"

        self.cache[(origX, origY), c] = signal
        return signal

class SmallKeypad(BigKeypad):
    def __init__(self):
        self.cache = dict()
        self.x = 2
        self.y = 0
        self.k = {"^": (1, 0), "A":(2,0), "<":(0,1), "v":(1,1), ">":(2,1)}
        
#codes = ["029A"]
#codes = ["029A", "980A", "179A", "456A", "379A"]
codes = ["670A","974A","638A","319A","508A"]

score = 0
for code in codes:
    numeric = BigKeypad()
    dir1 = SmallKeypad()
    myKeyboard = SmallKeypad()

    code2 = numeric.code(code)
    print(code2)
    code3 = dir1.code(code2)
    print(code3)
    final = myKeyboard.code(code3)
    print(final)
    print(len(final))

    score += int(code[0:3]) * len(final)

print("Part 1:", score)


score = 0
for code in codes:

    numeric = BigKeypad()
    robots = [SmallKeypad() for i in range(22)]
    myKeyboard = SmallKeypad()

    codePrev = numeric.code(code)

    for robot in robots:
        code_r = robot.code(codePrev)
        codePrev = code_r

    final = myKeyboard.code(codePrev)
#    print(final)
#    print(len(final))

    score += int(code[0:3]) * len(final)

print("Part 2:", score)

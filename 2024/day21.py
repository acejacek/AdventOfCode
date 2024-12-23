#!/usr/bin/env python3

class BigKeypad:
    def __init__(self):
        self.x = 2
        self.y = 3
        self.k = {"7": (0,0), "8": (1,0), "9": (2, 0), "4":(0,1), "5":(1,1), "6":(2,1), "1":(0,2), "2":(1,2), "3":(2,2), "0":(1,3), "A":(2,3)}

    def code(self, code):
        totalSignal = ""
        for c in code:
            totalSignal += self.press(c)
            totalSignal += "A"
        return totalSignal

    def press(self, c):
        x, y = self.k[c]
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

        return signal

class SmallKeypad(BigKeypad):
    def __init__(self):
        self.x = 2
        self.y = 0
        self.k = {"^": (1, 0), "A":(2,0), "<":(0,1), "v":(1,1), ">":(2,1)}

#codes = ["029A", "980A", "179A", "456A", "379A"]
codes = ["670A","974A","638A","319A","508A"]

score = 0
for code in codes:
    numeric = BigKeypad()
    dir1 = SmallKeypad()
    dir2 = SmallKeypad()
    myKeyboard = SmallKeypad()

    code2 = numeric.code(code)
    code3 = dir1.code(code2)
    final = myKeyboard.code(code3)

    score += int(code[0:3]) * len(final)

print("Part 1:", score)

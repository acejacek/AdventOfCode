#!/usr/bin/env python3

from parse import parse, compile as comp

class Machine:

    def __init__(self, a, b, prize):
        self.a = a
        self.b = b
        self.prize = tuple(prize)

    def add(self, a, b):
        return (a[0] + b[0], a[1] + b[1])

    def mul(self, a, b):
        return (a[0] * b, a[1] * b)

    def find(self):
        cost = []
        combinations = [(pressA, pressB) for pressA in range(100) for pressB in range(100)]
        for c in combinations:
            endPoint = self.add(self.mul(self.a, c[0]), self.mul(self.b, c[1]))
            if endPoint == self.prize:
                cost += [c[0] * 3 + c[1]]
        return min(cost, default = 0)

def calculate(filename):

    buttonAPattern=comp("Button A: X{:d}, Y{:d}\n")
    buttonBPattern=comp("Button B: X{:d}, Y{:d}\n")
    prizePattern=comp("Prize: X={:d}, Y={:d}\n")

    cost = 0
    with open(filename, "r") as file:
        while line := file.readline():
            if line == "\n":
                continue
            a = buttonAPattern.parse(line)
            b = buttonBPattern.parse(file.readline())
            p = prizePattern.parse(file.readline())

            m = Machine(a, b, p)
            cost += m.find()

    return cost

assert calculate("day13.test") == 480

a = calculate("day13.txt")
print("Part 1:", a)


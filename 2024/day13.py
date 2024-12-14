#!/usr/bin/env python3

from parse import parse, compile as comp
from sympy import Eq, solve, symbols

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
        """naive method, iterating all possible moves"""
        cost = []
        combinations = [(pressA, pressB) for pressA in range(100) for pressB in range(100)]
        for c in combinations:
            endPoint = self.add(self.mul(self.a, c[0]), self.mul(self.b, c[1]))
            if endPoint == self.prize:
                cost += [c[0] * 3 + c[1]]
        return min(cost, default = 0)

    def useEq(self):
        """ solve equation:
           A * x_buttonA + B * x_buttonB = prize_x
           A * y_buttonA + B * y_buttonB = prize_y

           search for A, B
        """
        (A, B) = symbols("A B")
        eq1 = Eq((A * self.a[0] + B * self.b[0]), self.prize[0])
        eq2 = Eq((A * self.a[1] + B * self.b[1]), self.prize[1])
        solution = solve((eq1, eq2), (A, B))

        if int(solution[A]) == solution[A] and int(solution[B]) == solution[B]:
            return solution[A] * 3 + solution[B]
        else:
            # there was fractional result, no hot on target
            return 0

def calculate(filename, part = 1):

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

            if part == 2:
                m.prize = m.add(m.prize, (10000000000000, 10000000000000))

#            cost += m.find()
            cost += m.useEq()
    return cost

assert calculate("day13.test") == 480

a = calculate("day13.txt")
print("Part 1:", a)

a = calculate("day13.txt", part = 2)
print("Part 2:", a)

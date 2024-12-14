#!/usr/bin/env python3

from parse import parse
import matplotlib.pyplot as plt

class Robot:
    def __init__(self, x, y, vx, vy, w, h):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.w = w
        self.h = h

    def move(self):
        self.x = (self.x + self.vx) % self.w
        self.y = (self.y + self.vy) % self.h

    def quart(self):
        splitX = self.w // 2
        splitY = self.h // 2
        if self.x < splitX and self.y < splitY: return 1
        if self.x > splitX and self.y < splitY: return 2
        if self.x < splitX and self.y > splitY: return 3
        if self.x > splitX and self.y > splitY: return 4
        return 0

def calculate(filename, part = 1):

    robots = []
    if part == 0:
        w, h = 11, 7
    else:
        w, h = 101, 103

    with open(filename, "r") as file:
        while line := file.readline():
            (x, y, vx, vy) = parse("p={:d},{:d} v={:d},{:d}\n", line)
            robots += [Robot(x, y, vx, vy, w, h)]

    if part != 2:
        for i in range(100):
            for robot in robots:
                robot.move()

        q1 = len([robot.quart() for robot in robots if robot.quart() == 1])
        q2 = len([robot.quart() for robot in robots if robot.quart() == 2])
        q3 = len([robot.quart() for robot in robots if robot.quart() == 3])
        q4 = len([robot.quart() for robot in robots if robot.quart() == 4])
    
        return q1 * q2 * q3 * q4

    else:
        i = 0
        while True:
            i +=1
            points = set()
            for robot in robots:
                robot.move()
                points.add((robot.x, robot.y))

            # idea is that there will be number of points in middle of width that represent trunk of tree
            trunk = len([point for point in points if point[0] == w // 2])
            if trunk > 18:
                print("Seconds from start:", i)
                plt.title(i)
                graph = plt.scatter(*zip(*points))
                axes = graph.axes
                axes.invert_yaxis()
                #display the graph, wait for user to close the window
                plt.show()
                # there will be many false positives, but eventually the Christmas tree will be visible

assert calculate("day14.test", part = 0) == 12
a = calculate("day14.txt")
print("Part 1:", a)

a = calculate("day14.txt", part = 2)


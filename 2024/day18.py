#!/usr/bin/env python3
from collections import deque

def calculate(filename, part = 1):
    fallingBytes = deque()

    with open(filename, "r") as file:
        while line := file.readline():
            x, y = map(int, line.split(","))
            fallingBytes.append((x, y))

    size = 6

    start = (0, 0)
    end = (size, size)

    maze = set()
    for i in range(12):
        b = fallingBytes.popleft()
        print(b)
        maze.add(b)

    print()
    for i in maze:
        print(i)



calculate("day18.test")

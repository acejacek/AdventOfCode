#!/usr/bin/env python3

def calculate1(filename):

    visited = set()
    
    def peek(x, y):
        if x >=0 and x < w and y >= 0 and y < h:
            return eval(lines[y][x])

        return -1

    def walk(x, y, step):
        myHeight = peek(x, y)
        step += 1

        if myHeight == 9:
            visited.add(((x,y), step))
            return

        if peek(x - 1, y) == myHeight + 1:
            walk(x - 1, y, step)

        if peek(x + 1, y) == myHeight + 1:
            walk(x + 1, y, step)
        
        if peek(x, y - 1) == myHeight + 1:
            walk(x, y - 1, step)

        if peek(x, y + 1) == myHeight + 1:
            walk(x, y + 1, step)

        return

    with open(filename, "r") as file:
        lines = file.readlines()
    
    h = len(lines)
    w = len(lines[0]) - 1
    score = 0

    for y, line in enumerate(lines):
        for x, height in enumerate(line):
            if height == '\n':
                continue
            if int(height) == 0:
                walk(x, y, 0)
                score += len(visited)
                visited = set()
                 
    return score

a = calculate1("day10.test")
assert a == 36, "Error in score calculation"

a = calculate1("day10.txt")
print("Part 1:", a)

#!/usr/bin/env python3

def calculate(filename, part = 1):

    visited = set()
    possible = []

    def peek(x, y):
        if x >=0 and x < w and y >= 0 and y < h:
            if lines[y][x] != ".":
                return eval(lines[y][x])

        return -1

    def walk(x, y, step):
        myHeight = peek(x, y)
        step += 1

        if myHeight == 9:
            if part == 1:
                visited.add(((x,y), step))
            else:
                nonlocal possible
                possible += [1]
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
            if height == '\n' or height == '.':
                continue
            if int(height) == 0:
                walk(x, y, 0)
                if part == 1:
                    # for part 1 use set, to eliminate duplicates
                    score += len(visited)
                    visited = set()
                if part == 2:
                    # here use list, to catch all possible trails
                    score += len(possible)
                    possible = []
                 
    return score

assert calculate("day10.test") == 36, "Error in score calculation"
a = calculate("day10.txt")
print("Part 1:", a)

assert calculate("day10.test2", part = 2) == 13
assert calculate("day10.test3", part = 2) == 227

a = calculate("day10.txt", part = 2)
print("Part 2:", a)

#!/usr/bin/env python3

import heapdict as hd
from collections import deque

def calc1(filename, finish, amount):

    notvisited = hd.heapdict()
    visited = dict()

    for x in range(finish[0] + 1):
        for y in range(finish[0] + 1):
            notvisited[(x, y)] = float("inf")

    with open(filename, "r") as file:
        fall = 0
        while line := file.readline():
            x, y = map(int, line.split(","))
            notvisited.pop((x, y))
            fall += 1
            if fall == amount: break

    notvisited[(0, 0)] = 0
    while len(notvisited) > 0:

        # find smallest distance node:
        (x, y), weight = notvisited.popitem()
        visited[(x, y)] = weight

        arround = [(x + dx, y + dy) for dx, dy in [[-1, 0], [1, 0], [0, -1], [0, 1]]]
        neighbours = [node for node in arround if node in notvisited]
        for n in neighbours:
            if  notvisited[n] > weight + 1:
                notvisited[n] = weight + 1

    return visited[finish]

def calc2(filename, finish):

    bytestable = []

    with open(filename, "r") as file:
        fall = 0
        while line := file.readline():
            x, y = map(int, line.split(","))
            bytestable += [(x, y)]

    f = 1024
    blocked = False
    while not blocked:

        notvisited = hd.heapdict()
        visited = dict()

        for x in range(finish[0] + 1):
            for y in range(finish[0] + 1):
                if (x, y) not in bytestable[0:f]:
                    notvisited[(x, y)] = float("inf")

        notvisited[(0, 0)] = 0
        while len(notvisited) > 0:

            # find smallest distance node:
            (x, y), weight = notvisited.popitem()
            visited[(x, y)] = weight

            arround = [(x + dx, y + dy) for dx, dy in [[-1, 0], [1, 0], [0, -1], [0, 1]]]
            neighbours = [node for node in arround if node in notvisited]
            for n in neighbours:
                if  notvisited[n] > weight + 1:
                    notvisited[n] = weight + 1
        
        f += 1
        if visited[finish] == float("inf"):
            blocked = True

    print(bytestable[f - 2])


finish = (6,6)
assert calc1("day18.test", finish, 12) == 22

finish = (70, 70)
a = calc1("day18.txt", finish, 1024)
print("Part 1:", a)

a = calc2("day18.txt", finish)
exit()

for f in range(1024, 3451):
    if calc1("day18.txt", finish, f) == float("inf"):
        print("Part 2:", f)
        break


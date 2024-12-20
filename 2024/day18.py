#!/usr/bin/env python3

import heapdict as hd

def calc(filename, finish, amount, part = 1):

    nodes = hd.heapdict()
    visited = dict()

    for x in range(finish[0] + 1):
        for y in range(finish[0] + 1):
            nodes[(x, y)] = float("inf")

    with open(filename, "r") as file:
        fall = 0
        while line := file.readline():
            x, y = map(int, line.split(","))
            nodes.pop((x, y))
            fall += 1
            if fall == amount: break

    nodes[(0, 0)] = 0
    while len([node for node in nodes if node not in visited]) != 0:

        # find smallest distance node:
        (x, y), weight = nodes.popitem()
        visited[(x, y)] = weight

        arround = [(x + dx, y + dy) for dx, dy in [[-1, 0], [1, 0], [0, -1], [0, 1]]]
        neighbours = [node for node in arround if node in nodes]
        for n in neighbours:
            if  nodes[n] > weight + 1:
                nodes[n] = weight + 1

    return visited[finish]


finish = (6,6)
assert calc("day18.test", finish, 12) == 22

finish = (70, 70)
a = calc("day18.txt", finish, 1024)
print("Part 1:", a)


#!/usr/bin/env python3

import heapdict as hd

def calc(filename, finish, amount):

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

    return (visited[finish], line)


finish = (6,6)
a, _ = calc("day18.test", finish, 12)
assert a == 22

finish = (70, 70)
a, _ = calc("day18.txt", finish, 1024)
print("Part 1:", a)

minimum = 1024
maximum = 3451

while True:
    f = (maximum - minimum) // 2 + minimum
    (a, b) = calc("day18.txt", finish, f)
    if a == float("inf"):
        if minimum == f - 1:
            print("Part 2:", f, b)
            break
        maximum = f
    else:
        minimum = f
    


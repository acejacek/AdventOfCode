#!/usr/bin/env python3

import heapdict as hd

def calc(filename):

    nodes = set()
    walls = set()
    
    y = 0
    with open(filename, "r") as file:
        while line := file.readline():
        
            for x, elem in enumerate(line):
                if elem == "#":
                    walls.add((x, y))
                if elem == "S":
                    start = (x, y)
                    nodes.add(start)
                if elem == "E":
                    end = (x, y)
                    nodes.add(end)
                if elem == ".":
                    nodes.add((x, y))
            y += 1

    notvisited = hd.heapdict()
    for node in nodes:
        notvisited[(node)] = float("inf")
    notvisited[start] = 0
    visited = dict()
    while len(notvisited) > 0:

        # find smallest distance node:
        (x, y), weight = notvisited.popitem()
        visited[(x, y)] = weight

        arround = [(x + dx, y + dy) for dx, dy in [[-1, 0], [1, 0], [0, -1], [0, 1]]]
        neighbours = [node for node in arround if node in notvisited]
        for n in neighbours:
            if  notvisited[n] > weight + 1:
                notvisited[n] = weight + 1

    baseTime = visited[end]
    scores = dict()

    for x, y in walls:
        # find walls neighbours
        arround = [(x + dx, y + dy) for dx, dy in [[-1, 0], [1, 0], [0, -1], [0, 1]]]
        valid = [node for node in arround if node in visited]
        #check distances at neighbours
        localWeights = [weight for node, weight in visited.items() if node in valid]
        if len(localWeights) != 0:
            minimum = min(localWeights)
            maximum = max(localWeights)
            # save means shortcut between locations + cost of walking through wall
            save = maximum - minimum - 2
            if save > 0:
                soFarSaved = scores.get(save, 0)
                scores[save] = soFarSaved + 1

    return sum([qty for score, qty in scores.items() if score >= 100])

a = calc("day20.txt")
print("part 1:", a)

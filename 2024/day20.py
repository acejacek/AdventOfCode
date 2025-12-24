#!/usr/bin/env python3

import heapdict as hd

def calc1(filename):

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

def calc2(filename):

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

    scores = dict()

    def walk(x, y, minimum, step):

        # too far
        if step == 21: return 0
        # ended up at the path
        if (x, y) in visited:
            # save means shortcut between locations + cost of walking through wall
            save = visited[(x, y)] - minimum - 2
            if save > 0:
                soFarSaved = scores.get(save, 0)
                scores[save] = soFarSaved + 1
            return

        arround = [(x + dx, y + dy) for dx, dy in [[-1, 0], [1, 0], [0, -1], [0, 1]]]
        for nx, ny in arround:
            walk(nx, ny, minimum, step + 1)

    for x, y in walls:
        # find walls neighbours
        arround = [(x + dx, y + dy) for dx, dy in [[-1, 0], [1, 0], [0, -1], [0, 1]]]
        valid = [node for node in arround if node in visited]
        #check distances at neighbours
        localWeights = [weight for node, weight in visited.items() if node in valid]
        if len(localWeights) != 0:
            minimum = min(localWeights)
            walk(x, y, minimum, 0)


    print([qty for score, qty in scores.items() if score >= 50])
    return sum([qty for score, qty in scores.items() if score >= 50])

#a = calc1("day20.txt")
#print("part 1:", a)

a = calc2("day20.test")
print("part 2:", a)

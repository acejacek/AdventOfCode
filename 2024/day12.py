#!/usr/bin/env python3
from uuid import uuid1

def calculate(filename):

    def increasePlot(key, newFence):
        newArea = 1
        if key in plots:
            area, fence = plots[key]
            newArea += area
            newFence += fence
        plots[key] = (newArea, newFence)

    def peek(x, y):
        if x >=0 and x < w and y >= 0 and y < h:
            return garden[y][x][0]

        return '\0'

    def betterPeek(x, y):
        if x >=0 and x < w and y >= 0 and y < h:
            return garden[y][x]

        return ('\0', '\0')

    def visit(x, y, plantID = 0):
        plant = peek(x, y)
        # outside bounds
        if plant == '\0':
            return
        # this plot is not visited yet
        if garden[y][x][1] == 0:
            if plantID == 0:
                plantID = uuid1()
            garden[y][x][1] = plantID # put plantID into visited field
            # this plant is first discovered
            fence = 0
            
            if peek(x - 1, y) != plant:
                fence += 1
            else:
                visit(x - 1, y, plantID)

            if peek(x + 1, y) != plant:
                fence += 1
            else:
                visit(x + 1, y, plantID)
            
            if peek(x, y - 1) != plant:
                fence += 1
            else:
                visit(x, y - 1, plantID)

            if peek(x, y + 1) != plant:
                fence += 1
            else:
                visit(x, y + 1, plantID)

            increasePlot(plantID, fence)

    def countSides(plantID):
        # scan horizontally
        sides = 0
        aPrev = bPrev = ('\0', '\0')
        for y in range(h + 1):
            lineInProgress = False
            for x in range(w):
                a = betterPeek(x, y)
                b = betterPeek(x, y - 1)
                if lineInProgress == False:
                    if (a != aPrev or b != bPrev):
                        if a != b:
                            if a[1] == plantID or b[1] == plantID:
                                sides += 1
                                lineInProgress = True
                else:
                    lineInProgress = not (a[1] == b[1] == plantID)

                aPrev = a
                bPrev = b
        print("horiz:", sides)
        # scan vertically
        aPrev = bPrev = ('\0', '\0')
        for x in range(w + 1):
            lineInProgress = False
            for y in range(h):
                a = betterPeek(x, y)
                b = betterPeek(x - 1, y)
                if lineInProgress == False:
                    if (a != aPrev or b != bPrev):
                        if a != b:
                            if a[1] == plantID or b[1] == plantID:
                                sides += 1
                                lineInProgress = True
                else:
                    lineInProgress = not (a[1] == b[1] == plantID)

                aPrev = a
                bPrev = b

        print("vert:", sides)
        return sides

    garden = []
    plots = {}

    with open(filename, "r") as file:
        while line := file.readline():
            garden.append([[plot, 0] for plot in line if plot != "\n"])

    h = len(garden)
    w = len(garden[0])
    for y, line in enumerate(garden):
        for x, height in enumerate(garden):
            visit(x, y)
    
#    print(plots)
    sides = 1
    price = sum([area * fence for area, fence in plots.values()])
    print([(countSides(areaID), area, countSides(areaID) * area) for (areaID, (area, _)) in plots.items()])


#    sides = sum([countSides(areaID) * (area) for (areaID, (area, _)) in plots.items()])

    return (price, sides)

#assert calculate("day12.test") == 1930
#a = calculate("day12.txt")
#print("Part 1:", a)

print(calculate("day12.test3"))

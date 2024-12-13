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

    def visit(x, y, plantID = 0):
        """ idea behind this one is to visit each cell, and then do a flood untill all cells are explored"""
        plant = peek(x, y)
        # outside bounds
        if plant == '\0': return
        # this plot is not visited yet
        if garden[y][x][1] == 0:
            if plantID == 0:
                plantID = uuid1()
            garden[y][x][1] = plantID # put plantID into visited field
            # this plant is first discovered
            fence = 0
            # check left/right/up/down
            for cx, cy in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
                if peek(cx, cy) != plant:
                    # not my cell, put a fence there
                    fence += 1
                else:
                    # go and visit
                    visit(cx, cy, plantID)
            # store score in dictionary
            increasePlot(plantID, fence)

    def createRegions():
        """list of sets, each set are coords of one closed region"""
        ar = []
        for plantID in plots:
            elements = set()
            for y in range(h):
                for x in range(w):
                    if plantID == garden[y][x][1]:
                        elements.add((x, y))
            ar += [elements]
        return ar

    def countCorners():
        regions = createRegions()
        price = 0
        for region in regions:
            corners = set()
            for x, y in region:
                for cx, cy in [(x - 0.5, y - 0.5),(x - 0.5, y + 0.5), (x + 0.5, y + 0.5), (x + 0.5, y - 0.5)]:
                    """ corners are 0.5 away in all directiond from cell
                        x     x
                          ___
                          | |
                          ---
                        x     x
                    """
                    # this is a lost of all possible corners, at the corner of each cell inside region
                    corners.add((cx, cy))

            cornersCount = 0
            for cx, cy in corners:
                # go through all corners and check, their surroundings, where are cells belonging to the region
                surround = [(x, y) in region for x, y in [(cx - 0.5, cy - 0.5),(cx - 0.5, cy + 0.5), (cx + 0.5, cy + 0.5), (cx + 0.5, cy - 0.5)]]
                # surronud is a bool list, like [True, False, True, False]
                count = sum(surround)
                # if there is one or 3 ajacted cells, there is one corner
                if count == 1 or count == 3:
                    cornersCount += 1
                # if there are two cells, but oposit to each other, there are 2 corners 
                elif count == 2:
                    if surround == [True, False, True, False] or surround == [False, True, False, True]:
                        cornersCount += 2

            # price is area (count of all cells in region) * number of corners
            price += len(region) * cornersCount
        return price

    def countSides():
        """ count sides is equal to counting corners """
        countCorners()

    garden = []
    plots = {}

    with open(filename, "r") as file:
        while line := file.readline():
            garden.append([[plot, 0] for plot in line if plot != "\n"])

    h = len(garden)
    w = len(garden[0])
    for y in range(h):
        for x in range(w):
            visit(x, y)
    
    price_part1 = sum([area * fence for area, fence in plots.values()])
    price_part2 = countCorners()
    return (price_part1, price_part2)

assert calculate("day12.test") == (1930, 1206)
a, b = calculate("day12.txt")
print("Part 1:", a)
print("Part 2:", b)


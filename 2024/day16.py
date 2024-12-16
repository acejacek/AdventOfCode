#!/usr/bin/env python3

import sys

sys.setrecursionlimit(10000)

class Reindeer:

    def __init__(self, finish, freeWay):
       # self.pos = pos
        self.finish = finish
        self.dir = "E"
        self.visited = set()
        self.score = 0
        self.bestscore = 0
        self.freeWay = freeWay

    def N(self):
        return (self.pos[0], self.pos[1] - 1)
    def E(self):
        return (self.pos[0] + 1, self.pos[1])
    def S(self):
        return (self.pos[0], self.pos[1] + 1)
    def W(self):
        return (self.pos[0] - 1, self.pos[1])

    def look(self):
        exits = []
        """
        if  self.N() not in walls and self.N() not in self.visited:
            exits += [("N", self.N())]
        if  self.E() not in walls and self.E() not in self.visited:
            exits += [("E", self.E())]
        if  self.S() not in walls and self.S() not in self.visited:
            exits += [("S", self.S())]
        if  self.W() not in walls and self.W() not in self.visited:
            exits += [("W", self.W())]
        """
        if  self.N() in self.freeWay:
                if self.freeWay[self.N()] == 0 or self.freeWay[self.N()] > self.score:
                    exits += [("N", self.N())]
        if  self.E() in self.freeWay:
                if self.freeWay[self.E()] == 0 or self.freeWay[self.E()] > self.score:
                    exits += [("E", self.E())]
        if  self.S() in self.freeWay:
                if self.freeWay[self.S()] == 0 or self.freeWay[self.S()] > self.score:
                    exits += [("S", self.S())]
        if  self.W() in self.freeWay:
                if self.freeWay[self.W()] == 0 or self.freeWay[self.W()] > self.score:
                    exits += [("W", self.W())]

        return exits

    def walk(self, pos, rec = 1):
        if self.bestscore != 0 and self.score == self.bestscore:
            return
        if pos == self.finish:
            if self.bestscore == 0 or self.bestscore >= self.score:
                self.bestscore = self.score
            return

        self.freeWay[pos] = self.score
        self.pos = pos
        # self.visited.add(pos)
        exits = self.look()
        if len(exits) != 0:
            for e in exits:
                #print("at:",pos,"sc:",self.score, "go:",e, freeWay[e[1]])
                #input()
                scoreInc = 1
                if e[0] != self.dir:
                    scoreInc = 1001

                self.score += scoreInc
                prevDir = self.dir
                self.dir = e[0]
                self.walk(e[1])
                self.score -= scoreInc
                self.dir = prevDir

        #self.visited.remove(pos)


def calculate(filename, part = 1):
    freeWay = dict()

    with open(filename, "r") as file:
        y = 0
        while line := file.readline():
            for x, elem in enumerate(line):
                if elem == "S":
                    start = (x, y)
                    freeWay[(x, y)] = 0
                if elem == "E":
                    finish = (x, y)
                    freeWay[(x, y)] = 0
                if elem == ".":
                    freeWay[(x, y)] = 0
            y += 1

    r = Reindeer(finish, freeWay)

    r.walk(start)
    print(r.bestscore)

a = calculate("day16.test")
a = calculate("day16.test2")
a = calculate("day16.txt")

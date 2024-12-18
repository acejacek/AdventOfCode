#!/usr/bin/env python3

#import sys
#sys.setrecursionlimit(10000)

class Reindeer:

    def __init__(self, finish, freeWay):
        self.finish = finish
        self.dir = "E"
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
        if  self.N() in self.freeWay:
            exits += [("N", self.N())]
        if  self.E() in self.freeWay:
            exits += [("E", self.E())]
        if  self.S() in self.freeWay:
            exits += [("S", self.S())]
        if  self.W() in self.freeWay:
            exits += [("W", self.W())]
        return exits

    def walk(self, pos):
        if self.bestscore != 0 and self.score >= self.bestscore:
            return

        if pos == self.finish:
            if self.bestscore == 0 or self.bestscore >= self.score:
                self.bestscore = self.score
            return

        self.freeWay[pos] = self.score
        self.pos = pos
        exits = self.look()
        for e in exits:
            if e[0] != self.dir:
                if self.freeWay[e[1]] == 0 or self.freeWay[e[1]] >= self.score + 1001:
                    self.score += 1001
                    prevDir = self.dir
                    self.dir = e[0]
                    self.walk(e[1])
                    self.score -= 1001
                    self.dir = prevDir
            else:
                if self.freeWay[e[1]] == 0 or self.freeWay[e[1]] >= self.score + 1:
                    self.score += 1
                    self.walk(e[1])
                    self.score -= 1

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

a = calculate("day16.test3")
#a = calculate("day16.test")
#a = calculate("day16.test2")
#a = calculate("day16.txt")

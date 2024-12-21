#!/usr/bin/env python3

from functools import lru_cache


def reduce(design, towels):
    if len(design) == 0:
        return True

    for towel in towels:
        if design[0:len(towel)] == towel:
            if reduce(design[len(towel):], towels) == True:
                return True

    return False

# Custom Decorator function
def list_to_tuple(function):
    def wrapper(*args):
        args = [tuple(x) if isinstance(x, list) else x for x in args]
        result = function(*args)
        result = tuple(result) if isinstance(result, list) else result
        return result
    return wrapper

@list_to_tuple
@lru_cache(maxsize=200)
def reduceAndCalc(pattern, towels):
    if len(pattern) == 0:
        return 1
    
    score = 0
    for towel in towels:
        if pattern[0:len(towel)] == towel:
            newPattern = pattern[len(towel):]
#            matchingTowels = [towel for towel in towels if towel in newPattern]
#            score += reduceAndCalc(newPattern, matchingTowels)
            score += reduceAndCalc(newPattern, towels)

    return score

def calc(filename):

    towels = []
    patterns = []

    with open(filename, "r") as file:

        lines = file.read().splitlines()
        loadTowels = True
        for line in lines:
            if loadTowels:
                if line == "":
                    loadTowels = False
                    continue
                towels.extend(line.split(", "))
            else:
                patterns += [line]

    possible = 0
    for pattern in patterns:
        if reduce(pattern, towels) == True:
            possible += 1

    allarrangements = 0
    for pattern in patterns:
        #matchingTowels = [towel for towel in towels if towel in pattern]
        #allarrangements += reduceAndCalc(pattern, matchingTowels)
        allarrangements += reduceAndCalc(pattern, towels)

    return (possible, allarrangements)

a, b = calc("day19.test")
print(a, b)
a, b = calc("day19.txt")
print(a, b)

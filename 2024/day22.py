#!/usr/bin/env python3


def calculateNext(secret):
    result = secret << 6  # * 64
    #mix
    secret ^= result
    #prune
    secret %= 16777216

    result = secret >> 5 # // 32
    secret ^= result
    secret %= 16777216

    result = secret << 11 # * 2048
    secret ^= result
    secret %= 16777216

    return secret

def calc(filename):

    total = 0

    with open(filename, "r") as file:
        while line := file.readline():
            secret = int(line)
            for i in range(2000):
                secret = calculateNext(secret)
            total += secret

    return total

def calc2(filename):

    buyers = []

    with open(filename, "r") as file:
        while line := file.readline():
            secret = int(line)
            prices = [secret % 10]
            for i in range(2000):
                secret = calculateNext(secret)
                prices += [secret % 10]
            buyers += [prices]

    print(buyers)

    for buyer in buyers:
        changes = []
        matches = []
        for i, price in enumerate(buyer):
            if i > 0:
                changes += [price - buyer[i - 1]]
        for i, change in enumerate(changes):
            if i < len(changes) - 4:
                matches += [[(changes[i], changes[i + 1], changes[i + 2], changes[i + 3]), buyer[i + 4]]]

        for match in matches:
            if match[0] == (-2, 1, -1, 3):
                print(match)


#assert calc("day22.test") == 37327623
#a = calc("day22.txt")
#print("Part 1:", a)

calc2("day22.test2")

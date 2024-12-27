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

assert calc("day22.test") == 37327623

a = calc("day22.txt")
print("Part 1:", a)

#!/usr/bin/env python3

def calculate2(filename, steps):
    """faster method, with dictionary holding counter of stones with the same
    number"""

    def increase(key, val = 1):
        if key in newStones:
            val += newStones[key]
        newStones[key] = val

    with open(filename, "r") as file:
        line = file.readline()

    stones = {int(words):1 for words in line.split()}
    newStones = {}

    for step in range(steps):
        newStones.clear()
        for stone, qty in stones.items():
            if stone == 0:
                increase(1, qty)

            elif len(str(stone)) % 2 == 0:
                split = len(str(stone)) // 2
                left = str(stone)[0:split]
                right = str(stone)[split:]
                increase(int(left), qty)

                # truncate all trailing zeros
                while len(right) > 1 and right[0] == "0":
                    right = right[1:]
                increase(int(right), qty)

            else:
                increase(stone * 2024, qty)                

        stones.clear()
        stones.update(newStones)

    return sum([qty for qty in stones.values()])

def calculate(filename, steps):
    """naive method, good for short number of iterations"""

    with open(filename, "r") as file:
        line = file.readline()

    stones = [int(words) for words in line.split()]

    for step in range(steps):
        newStones = []
        for stone in stones:
            if stone == 0:
                newStones += [1]

            elif len(str(stone)) % 2 == 0:
                split = len(str(stone)) // 2
                left = str(stone)[0:split]
                right = str(stone)[split:]
                newStones += [int(left)]
                # truncate all trailing zeros
                while len(right) > 1 and right[0] == "0":
                    right = right[1:]
                newStones += [int(right)]

            else:
                newStones += [stone * 2024]
                
        stones = newStones
    return len(stones)

assert calculate("day11.test", 25) == 55312
a = calculate("day11.txt", 25)
print("Part 1:", a)

assert calculate2("day11.test", 25) == 55312
a = calculate2("day11.txt", 75)
print("Part 2:", a)



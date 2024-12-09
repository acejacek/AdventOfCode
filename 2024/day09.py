#!/usr/bin/env python3

def decompress(diskmap):
    diskblock = []
    fileID = 0

    for i, val in enumerate(diskmap):
        if i % 2 == 0:
            diskblock.extend([fileID] * val)
            fileID += 1
        else:
            diskblock.extend(["."] * val)

    return diskblock

def compactBlocks(diskblock):
    for i, val in enumerate(diskblock):
        if val == ".":
            for j in range(len(diskblock) - 1 , i, -1):
                if diskblock[j] != ".":
                    diskblock[i] = diskblock[j]
                    diskblock[j] = "."
                    break

    return(diskblock)


def checksum(diskblock):
    return sum([ i * val for i, val in enumerate(diskblock) if val != "." ])

def load(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
    
    return [int(elem) for elem in lines[0] if elem != "\n"]


assert checksum(compactBlocks(decompress(load("day09.test")))) == 1928

raw = load("day09.txt")
disk = decompress(raw)
compact = compactBlocks(disk)
print("Part 1:", checksum(compact))

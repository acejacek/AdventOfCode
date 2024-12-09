#!/usr/bin/env python3

from collections import deque

def buildQ(raw):
    q = []
    fileID = 0
    for i, val in enumerate(raw):
        if i % 2 == 0:
            q.append((fileID,  val))
            fileID += 1
        else:
            q.append((".",  val))

    return q

def compresQ(queue):
    done = False
    while not done:
        done = True
        try:
            for k, file in reversed(list(enumerate(queue))):
                if file[0] != ".":
                    for i, loc in enumerate(queue):
                        if i < k:
                            if loc[0] == "." and loc[1] >= file[1]:
                                done = False
                                left = loc[1] - file[1]
                                queue[i] = (file[0], file[1])
                                queue[k] = (".", file[1])
                                if left > 0:
                                    queue.insert(i+1, (".", left))
                                raise(StopIteration)
        except StopIteration:
            pass

    return queue

def serialize(queue):
    diskblock = []
    for (val, l) in queue:
        diskblock.extend([val] * l)

    return diskblock

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

raw = load("day09.test")
queue = buildQ(raw)
compressed = compresQ(queue)
serial = serialize(compressed)
assert checksum(serial) == 2858

raw = load("day09.txt")
queue = buildQ(raw)
compressed = compresQ(queue)
serial = serialize(compressed)
print("Part 2:", checksum(serial))


#!/usr/bin/env python3

def buildList(raw):
    q = []
    fileID = 0
    for i, val in enumerate(raw):
        if i % 2 == 0:
            q.append((fileID,  val))
            fileID += 1
        else:
            q.append((".",  val))

    return q

"""
This proc has potential bug. can lead to censequent locations with free spaces,
which are never merged into one chink of free space. Howewer, it works
flawlesly with my data
"""
def compressList(fileList):
    """simple insertion"""
    done = False
    while not done:
        done = True
        try:
            # walking from back, find a file
            for k, file in reversed(list(enumerate(fileList))):
                if file[0] != ".":
                    # now walking form front find space for it
                    for i, loc in enumerate(fileList):
                        # make sure free space is before file location
                        if i < k and loc[0] == "." and loc[1] >= file[1]:
                            # how much space left after file will be moved here
                            left = loc[1] - file[1]
                            # do the swap
                            fileList[i] = (file[0], file[1])
                            fileList[k] = (".", file[1])
                            done = False
                            if left > 0:
                                # don't forget to insert free space, if any
                                # remains
                                fileList.insert(i + 1, (".", left))
                                # now I need to leave both "for" loops, because
                                # order of files changed
                                raise(StopIteration)
                            # replacement done, go for next file
                            break
        except StopIteration:
            pass

    return fileList

def serialize(fileList):
    """translate fileList to form readeable by checksum() from part 1"""
    diskblock = []
    for (val, l) in fileList:
        diskblock.extend([val] * l)

    return diskblock

def decompress(diskmap):
    """translate diskmap to file layout"""
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
    """fond first free spot and bring last file into this space"""
    # keep track on position of last file in diskblocks
    lastIndex = len(diskblock) - 1 
    for i, val in enumerate(diskblock):
        if val == ".":
            for j in range(lastIndex , i, -1):
                if diskblock[j] != ".":
                    diskblock[i] = diskblock[j]
                    diskblock[j] = "."
                    lastIndex = j - 1 # no need to scan all blocks next time
                    break

    return diskblock

def checksum(diskblock):
    """calculate checkum from flat list of files"""
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
fileList = buildList(raw)
compressed = compressList(fileList)
serial = serialize(compressed)
assert checksum(serial) == 2858

raw = load("day09.txt")
fileList = buildList(raw)
compressed = compressList(fileList)
compact = serialize(compressed)
print("Part 2:", checksum(compact))


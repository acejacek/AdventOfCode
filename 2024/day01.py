#!/bin/python3

def load_lists(filename):
    file = open(filename, "r");
    list_a = []
    list_b = []
    for line in file.readlines():
        tmp = line.split("  ")
        try:
            list_a.append(eval(tmp[0]))
            list_b.append(eval(tmp[1]))
        except:
            pass

    list_a.sort()
    list_b.sort()
    return list_a, list_b


def calculate_sum(list_a, list_b):
    list_sum = 0
    for a, b in zip(list_a, list_b):
        list_sum += abs(a - b)

    return list_sum


def calculate_similarity(list_a, list_b):
    list_similarity_score = 0
    for elem in list_a:
        list_similarity_score += elem * list_b.count(elem)

    return list_similarity_score


l1, l2 = load_lists("day01.test")
assert calculate_sum(l1, l2) == 11, "Wromg sum"
assert calculate_similarity(l1, l2) == 31, "Wrong similarity"

l1, l2 = load_lists("day01.txt")
print("Part 1: sum of differences is", calculate_sum(l1, l2))
print("Part 2: similarity score is", calculate_similarity(l1, l2))


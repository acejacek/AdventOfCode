def testing(numbers, test):
    for i in range(len(numbers) - 1):
        if test(numbers[i], numbers[i + 1]):
            return False

    return True

def increasing(numbers):
    return testing(numbers, lambda a, b: a >= b)

def decreasing(numbers):
    return testing(numbers, lambda a, b: a <= b)

def good_levels(numbers):
    test = lambda a, b: abs(a - b) > 3
    return testing(numbers, test)

def is_safe(numbers):
    return (increasing(numbers) or \
            decreasing(numbers)) and \
            good_levels(numbers)

def count_safe(filename, part = 1):
    safe = 0
    with open(filename, "r") as file:
        lines = file.readlines()
        for line in lines:
            words = line.split()
            numbers = [eval(w) for w in words]

            if is_safe(numbers):
                safe += 1

            elif part == 2:
                for i in range(len(numbers)):
                    copy = numbers.copy()
                    copy.pop(i);
                    if is_safe(copy):
                        safe += 1
                        break
    return safe

assert count_safe("day02.test") == 2
assert count_safe("day02.test", 2) == 4

print("Part 1: safe reports:", count_safe("day02.txt"))
print("Part 2: safe reports:", count_safe("day02.txt", 2))

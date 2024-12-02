def increasing(numbers):
    for i in range(len(numbers) - 1):
        if numbers[i] >= numbers[i + 1]:
            return False

    return True;

def decreasing(numbers):
    for i in range(len(numbers) - 1):
        if numbers[i] <= numbers[i + 1]:
            return False

    return True;

def good_levels(numbers):
    for i in range(len(numbers) - 1):
        if abs(numbers[i] - numbers[i + 1]) > 3:
            return False

    return True;

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

def multiply_or_add(target, numbers, prev):
    """recursively add/multiple consequect elements, testing if reaches target"""
    # did we already overshoot the target?
    if prev > target:
        return False

    # end reached; do we have a match?
    if len(numbers) == 0:
        return prev == target

    return multiply_or_add(target, numbers[1:], prev + numbers[0]) or \
           multiply_or_add(target, numbers[1:], prev * numbers[0])

def multiply_or_add_or_merge(target, numbers, prev):
    """recursively add/multiple/merge consequect elements, testing if reaches target"""
    def merge(a, b):
        return int(str(a) + str(b))

    if prev > target:
        return False

    if len(numbers) == 0:
        return prev == target

    return multiply_or_add_or_merge(target, numbers[1:], prev + numbers[0]) or \
           multiply_or_add_or_merge(target, numbers[1:], prev * numbers[0]) or \
           multiply_or_add_or_merge(target, numbers[1:], merge(prev, numbers[0]))

def calculate(filename, part = 1):
    with open(filename, "r") as file:
        lines = file.readlines()

    totalResult = 0
    for line in lines:
        testValue = int(line.split(":")[0])
        numbersStr = line.split(":")[1]
        numbers = list(map(int, numbersStr.split()))

        if part == 1 and multiply_or_add(testValue, numbers[1:], numbers[0]):
            totalResult += testValue

        if part == 2 and multiply_or_add_or_merge(testValue, numbers[1:], numbers[0]):
            totalResult += testValue

    return totalResult

assert calculate("day07.test") == 3749
print("Part 1:", calculate("day07.txt"))

assert calculate("day07.test", part = 2) == 11387
print("Part 2:", calculate("day07.txt", part = 2))

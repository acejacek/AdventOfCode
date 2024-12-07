
def multiply_or_plus(value, numbers, prev):
    if len(numbers) == 0:
        return False
    # if tested all numbers and reach the value -> success
    if len(numbers) == 1 and \
       (prev + numbers[0] == value or \
        prev * numbers[0] == value):
        return True

    return multiply_or_plus(value, numbers[1:], prev + numbers[0]) or \
           multiply_or_plus(value, numbers[1:], prev * numbers[0])

def calculate(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    totalResult = 0
    for line in lines:
        testValue = int(line.split(":")[0])
        numbersStr = line.split(":")[1]
        numbers = list(map(int, numbersStr.split()))

        if multiply_or_plus(testValue, numbers[1:], numbers[0]) == True:
            totalResult += testValue

    return totalResult

assert calculate("day07.test") == 3749
print("Part 1:", calculate("day07.txt"))


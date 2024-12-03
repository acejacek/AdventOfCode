from re import findall, sub, DOTALL

testData1 = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
testData2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"


def calculate(data):
    muls = findall(r"mul\([0-9]+,[0-9]+\)", data)

    sum = 0
    for x in muls:
        [a, b] = findall("[0-9]+", x)
        sum += eval(a) * eval(b)

    return sum


def filter_donts(data):
    return sub(r"don't\(\).*?(?:do\(\))","", data, flags = DOTALL) 


assert calculate(testData1) == 161

filtered = filter_donts(testData2)
assert calculate(filtered) == 48


with open("day03.txt", "r") as file:
    lines = file.readlines()

inputData = "".join(lines)

print("Part 1:", calculate(inputData))

filtered = filter_donts(inputData)
print("Part 2:", calculate(filtered))

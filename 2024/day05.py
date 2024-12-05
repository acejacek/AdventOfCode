from parse import parse

def createChecklist(lines):
    checklist = []
    for line in lines:
        a = parse("{:d}|{:d}\n", line)
        if a:
            checklist.append((a[0], a[1]))

    return checklist


def createPages(lines):
    pages = []
    ignore = True   # ignore everything until empty line

    for line in lines:
        if not ignore:
            pages.append([int(s) for s in line.rstrip().split(",")])
        if line == "\n":
            ignore = False

    return pages


def pageIsCorrect(page, checklist):
    for check in checklist:
        if (check[0] in page) and (check[1] in page):
            if page.index(check[0]) > page.index(check[1]):
                return False  # this pages order is damaged

    return True


def returnMiddlePages(page):
    i = len(page) // 2   # middle element. no modulo, rows are odd in size
    return page[i]


def calculate_part1(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    manual = createPages(lines)
    checklist = createChecklist(lines)
    sumOfPages = 0

    for page in manual:
        if pageIsCorrect(page, checklist):
            sumOfPages += returnMiddlePages(page)

    return sumOfPages


def fixWrongPage(page, checklist):
    
    if not pageIsCorrect(page, checklist):
        # check what's wrong
        for check in checklist:
            if (check[0] in page) and (check[1] in page):
                i1 = page.index(check[0])
                i2 = page.index(check[1])
                if i1 > i2:
                    page[i1], page[i2] = page[i2], page[i1] # swap
                    page = fixWrongPage(page, checklist) # recurrence

    return page


def filterWrongPage(page, checklist):
    if pageIsCorrect(page, checklist):
        return 0 # page is already OK, nothing to do here, ignore this one

    fixed = fixWrongPage(page, checklist)
    return returnMiddlePages(fixed)


def calculate_part2(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    manual = createPages(lines)
    checklist = createChecklist(lines)
    sumOfPages = 0

    for page in manual:
        sumOfPages += filterWrongPage(page, checklist)

    return sumOfPages


assert calculate_part1("day05.test") == 143
print("Part 1:", calculate_part1("day05.txt"))

assert calculate_part2("day05.test") == 123
print("Part 2:", calculate_part2("day05.txt"))

#!/usr/bin/env python3

def computer(prog, A = 0, B = 0, C = 0):
    pointer = 0
    out = []
    outIdx = 0

    # instructions math is simplified to limits of my knowlegde
    # instead of operand proc, here is this simple lookuptable [0,1,2,3,A,B,C]
    while pointer < len(prog):
        operand = prog[pointer + 1]
        match prog[pointer]:
            case 0:  # adv
                A >>= [0,1,2,3,A,B,C][operand]
            case 1:  # bxl
                B ^= operand
            case 2:  # bst
                B = [0,1,2,3,A,B,C][operand] & 7
            case 3:  # jnz
                if A != 0:
                    pointer = operand - 2
            case 4:  # bxc
                B ^= C
            case 5:  # out
                out += [[0,1,2,3,A,B,C][operand] & 7]
            case 6:  # bdv
                B = A >> [0,1,2,3,A,B,C][operand]
            case 7:
                C = A >> [0,1,2,3,A,B,C][operand]
        pointer += 2

    return out

program = [0,1,5,4,3,0]
a = computer(program, A = 729)
print("Test 1:")
print(*a, sep=",")

program = [2,4,1,5,7,5,0,3,1,6,4,3,5,5,3,0]
a = computer(program, A = 59590048)
print("Part 1:")
print(*a, sep=",")

# this works, but only for short programs. Otherwise it escalates quickly
program = [0,3,5,4,3,0]
for a in range(99999999):    # bruteforce run
    if a & 7 == 0:

        if program == computer(program, A = a):
            print("Test 2:", a)
            break

# I've noticed, that to generate just last element of program,  A = 3
# to generate 2 elements, A = 24 (which is prev A * 8)
# to generate 3 elements, A = 192 (which is prev A * 8)
# to generate 4 elements, A = 1538 (which is _almost_ prev A * 8)
# so I'm searching for A finding last element, then multiply A by 8,
# and continue search for longer and loger part of program, each time
# increasing A eight times

program = [2,4,1,5,7,5,0,3,1,6,4,3,5,5,3,0]

idx = 1 
a = 0
target = program[len(program) - idx:]
while True:
    if target == computer(program, A = a):
        idx += 1
        if idx > len(program): break
        target = program[len(program) - idx:]
        #a *= 8
        a <<= 3  # faster * 8
    else:
        a += 1

print("Part 2:", a)


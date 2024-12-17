#!/usr/bin/env python3

def computer2(prog, A):
    pointer = 0
    B = 0
    C = 0
    out = []
    outIdx = 0

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
                if out[outIdx] != prog[outIdx]: return
                outIdx += 1
            case 6:  # bdv
                B = A >> [0,1,2,3,A,B,C][operand]
            case 7:
                C = A >> [0,1,2,3,A,B,C][operand]
        pointer += 2

    return out

def computer(prog, A = 0, B = 0, C = 0):
    pointer = 0
    outOnce = False

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
                if outOnce:
                    out += "," + str([0,1,2,3,A,B,C][operand] & 7)
                else:
                    out = str([0,1,2,3,A,B,C][operand] & 7)
                    outOnce = True
            case 6:  # bdv
                B = A >> [0,1,2,3,A,B,C][operand]
            case 7:
                C = A >> [0,1,2,3,A,B,C][operand]
        pointer += 2

    return out

program = [2,4,1,5,7,5,0,3,1,6,4,3,5,5,3,0]
a = computer(program, A=59590048)
print("Part 1:", a)

program = [0,3,5,4,3,0]
for a in range(500048):
    if a & 7 == 0:
        if program == computer2(program, a):
            print("117440 ==",a)
            break
#exit()

program = [2,4,1,5,7,5,0,3,1,6,4,3,5,5,3,0]
for a in range(1000000000,9000000000):
    if program == computer2(program, a):
        print("Part 2:", a)
        break
print("Not found")


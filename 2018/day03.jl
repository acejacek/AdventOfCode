#!/usr/bin/env julia

function calculate1(filename)
    input = readlines(filename)

    fabric = Dict();
    
    for line in input
        id, a ,b ,c ,d = split(line, ('#',' ','@', ':', ',', 'x'), keepempty=false) 
        # I have no idea how to smartly convert procucts of split() to Int
        A = parse(Int, a)
        B = parse(Int, b)
        C = parse(Int, c) - 1
        D = parse(Int, d) - 1
        for x = A:A + C
            for y = B:B + D
                claimCount = get(fabric, (x, y), 0)
                claimCount += 1
                fabric[(x, y)] = claimCount
            end
        end
    end
    part1 = length([loc for (loc, claimCount) in fabric if claimCount > 1])

    part2 = 0
    return (part1, part2)
end

@assert calculate1("day03.test") == (4, 0)
(a, b) = calculate1("day03.txt")
println("Part 1 :", a)

#!/usr/bin/env julia

function calculate1(filename)
    input = readlines(filename)

    fabric = Dict();
    claims = []

    for line in input
        id, a ,b ,c ,d = split(line, ('#',' ','@', ':', ',', 'x'), keepempty=false) 
        # I have no idea how to smartly convert procucts of split() to Int
        A = parse(Int, a)
        B = parse(Int, b)
        C = parse(Int, c) - 1
        D = parse(Int, d) - 1
        push!(claims, (id, A, B, C, D))
        # put all claimed locations to the dictionary, with counter
        for x = A:A + C
            for y = B:B + D
                claimCount = get(fabric, (x, y), 0)
                claimCount += 1
                fabric[(x, y)] = claimCount
            end
        end
    end
    # count all locations claimed more that once
    part1 = length([loc for (loc, claimCount) in fabric if claimCount > 1]) 

    part2::String = ""
    # scan all claims
    for (id, A, B, C, D) in claims
        overlap = false
        for x = A:A + C
            for y = B:B + D
                claimCount = get(fabric, (x, y), 0)
                if claimCount > 1
                    overlap = true
                    break
                end
            end
        end
        # answer is claims without overlap
        if !overlap
            part2 = id
            break
        end
    end
        
    (part1, part2)
end

@assert calculate1("day03.test") == (4, "3")
(a, b) = calculate1("day03.txt")
println("Part 1: ", a)
println("Part 2: ", b)


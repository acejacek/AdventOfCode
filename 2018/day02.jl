#!/usr/bin/env julia

function calculate1(filename)
    input = readlines(filename)

    pairs = 0
    triplets = 0
    for line in input
        count = Dict{Char, Int}()
        for letter in line
            freq = get(count, letter, 0)
            freq += 1
            count[letter] = freq
        end
        addPair = false
        addTriplet = false
        for (letter, freq) in count
            if freq == 2 addPair = true end
            if freq == 3 addTriplet = true end
        end
        if addPair pairs += 1 end
        if addTriplet triplets += 1 end
    end
    pairs * triplets
end

@assert calculate1("day02.test") == 12 "Wrong test result"
#exit()
p1 = calculate1("day02.txt")
println("Part 1: ", p1)

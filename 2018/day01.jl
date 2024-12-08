#!/usr/bin/env julia
function calculate()
    prev = Set()
    freq = 0
    while true
        a = parse.(Int, readlines("day01.txt"))
        for f in a
            if freq in prev
                return freq
            end
            push!(prev, freq)
            freq += f
        end
    end
end

a = parse.(Int, readlines("day01.txt"))
println("Part 1: ", sum(a))

println("Part 2: ", calculate())

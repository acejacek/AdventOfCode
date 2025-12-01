#!/usr/bin/env julia

using Dates

function calculate1(filename)
    input = readlines(filename)
    records = []
    format = DateFormat("yyyy-mm-dd HH:MM")

    for line in input
        m = match(r"((?<=\[).+(?=\])).*((?<=#)([0-9]+)|(wakes)|(falls))", line)
        timestamp = DateTime(m[1], format)
        # println(timestamp," ", m[2])
        state = 0
        if m[2] == "falls"
            state = 1
        #elseif m[2] == "wakes"
        #    state = 2
        end

        push!(records, (timestamp, tryparse(Int, m[2]), state))
    end
    # sort by time
    sort!(records, by=x->x[1])

    states = []
    guard = -1
    for r in records
        if r[2] != nothing
            guard = r[2]
        end
        push!(states, (r[1], guard, r[3]))
    end

    #println([r for r in states if r[2] ==99])
    #println(states)
    for i in eachindex([state for state in states if state[2] == 10])
        if states[i][3] == 1
            println(states[i])
        end
    end
end

a = calculate1("day04.test")
println(a)

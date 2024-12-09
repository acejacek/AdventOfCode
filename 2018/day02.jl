#!/usr/bin/env julia

function calculate1(filename)
    input = readlines(filename)

    pairs = 0
    triplets = 0
    for line in input
        count = Dict{Char, Int}()
        # build dictionary of letters frequency
        for letter in line
            freq = get(count, letter, 0)
            freq += 1
            count[letter] = freq
        end
        addPair = false
        addTriplet = false
        # check if in dictionalry are any pairs or triplets
        for (letter, freq) in count
            if freq == 2 addPair = true end
            if freq == 3 addTriplet = true end
        end
        # add score if pair and/or triplet found
        if addPair pairs += 1 end
        if addTriplet triplets += 1 end
    end
    pairs * triplets
end

function calculate2(filename)
    input = readlines(filename)

    for line in input
        for other in input
            if line != other
                # substract one line from another
                diff = map(-, line, other)
                # after filtering 0
                withoutZeros = filter(x -> x != 0, diff)
                # there should be only one difference
                if length(withoutZeros) == 1
                    # find position of the difference
                    for (i, val) in enumerate(diff)
                        if val != 0
                            # compose result, cutting out wrong letter
                            return line[1:i - 1] * line[i + 1:end]
                            # end here, otherwise there will be second identical hit
                        end
                    end
                end
            end
        end
    end
end

@assert calculate1("day02.test") == 12 "Wrong test result"
p1 = calculate1("day02.txt")
println("Part 1: ", p1)

@assert calculate2("day02.test2") == "fgij" "Wrong test result for part 2"
p2 = calculate2("day02.txt")
println("Part 2: ", p2)


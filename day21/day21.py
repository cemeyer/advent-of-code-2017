import os
import sys

import numpy

sys.path.append(os.getcwd() + "/..")
import aocd


def numpify(left):
    foos = left.split("/")
    if len(foos) == 2:
        ary = numpy.full((2,2), 0)
    elif len(foos) == 3:
        ary = numpy.full((3,3), 0)
    elif len(foos) == 4:
        ary = numpy.full((4,4), 0)

    print foos
    for idy, y in enumerate(foos):
        for idx, x in enumerate(y):
            if x == '#':
                ary[idy][idx] = 1
    return ary


def tuplify(ary):
    return tuple([tuple(xs) for xs in ary])


def combos(ary):
    yield ary
    yield numpy.flip(ary, 0)
    yield numpy.flip(ary, 1)
    for i in range(3):
        ary = numpy.rot90(ary)
        yield ary
        yield numpy.flip(ary, 0)
        yield numpy.flip(ary, 1)


def replace(pattern, x,y,res):
    for iy in range(len(res)):
        for ix in range(len(res)):
            pattern[y+iy][x+ix] = res[iy][ix]


def enhance(sz, pattern, size, matches):
    match = False
    for y in range(0, size, sz):
        for x in range(0, size, sz):
            t = tuplify(pattern[y:y+size,x:x+size])
            if t in matches:
                match = True
                break
        if match:
            break
    
    pattern_new = numpy.full(((size//sz)*(sz+1),(size//sz)*(sz+1)), 0)
    for y in range(0, size, sz):
        for x in range(0, size, sz):
            t = tuplify(pattern[y:y+sz,x:x+sz])
            print y,x,t
            if t in matches:
                r = matches[t]
                replace(pattern_new, (x//sz) * (sz+1), (y//sz) * (sz+1), r)

    return (pattern_new, (size//sz)*(sz+1))


def solve():
    pattern = numpy.full((3, 3), 0)
    pattern[0][:3] = [0,1,0]
    pattern[1][:3] = [0,0,1]
    pattern[2][:3] = [1,1,1]

    size = 3
    matches = {}

    for line in lines:
        if line.strip() == "":
            continue
        left, right = line.strip().split(" => ")

        match = numpify(left)
        res = numpify(right)

        for m in combos(match):
            #print "match"
            t = tuplify(m)
            #print t
            matches[t] = res


    for itr in xrange(18):
        print "Iteration", itr
        if (size % 2) == 0:
            pattern, size = enhance(2, pattern, size, matches)
        elif (size % 3) == 0:
            pattern, size = enhance(3, pattern, size, matches)

        print pattern

    
    print "Part 1", sum([sum(xs) for xs in pattern])


if __name__ == "__main__":
    agent = aocd.Data(year=2017, day=21)
    data = agent.get_data()
    lines = data.split("\n")
    #lines = """../.# => ##./#../...
    #.#./..#/### => #..#/..../..../#..#""".split("\n")

    solve()

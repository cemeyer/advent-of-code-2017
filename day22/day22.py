from copy import deepcopy
import os
import sys

if sys.subversion[0] != "PyPy":
    print("USE PYPY")

sys.path.append(os.getcwd() + "/..")
import aocd


DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT = 0,1,2,3

rights = {DIR_UP: DIR_RIGHT, DIR_DOWN: DIR_LEFT, DIR_LEFT: DIR_UP, DIR_RIGHT: DIR_DOWN }
lefts = {DIR_UP: DIR_LEFT, DIR_DOWN: DIR_RIGHT, DIR_LEFT: DIR_DOWN, DIR_RIGHT: DIR_UP }
reverses = {DIR_UP: DIR_DOWN, DIR_DOWN: DIR_UP, DIR_LEFT: DIR_RIGHT, DIR_RIGHT: DIR_LEFT }
vecs = {DIR_UP: (-1, 0), DIR_DOWN: (1,0), DIR_LEFT: (0,-1), DIR_RIGHT: (0,1) }
names = {DIR_UP:"UP", DIR_DOWN:"DOWN", DIR_LEFT:"LEFT", DIR_RIGHT:"RIGHT"}

# Example of using complex numbers for x,y position and direction instead:
#
# UP = -1 + 0j  (real component is y, imaginary is x)
#
# Turn left: dir *= 1j
# Turn right: dir *= -1j
# Reverse: dir *= -1
#
# Moving forward one square is just addition of dir to pos.


def solve1():
    height, width = len(lines), len(lines[0])

    ary = {}

    for j,line in enumerate(lines):
        for i, c in enumerate(line):
            if c == '#':
                ary[(j,i)] = 1

    orig = deepcopy(ary)

    posx = width // 2
    posy = height // 2
    dir_ = DIR_UP

    bursts = 0

    for i in xrange(10000):
        # do a burst
        if (posy,posx) in ary:
            #print "dirty", names[dir_], "->", names[rights[dir_]], "pos", posy, posx
            dir_ = rights[dir_]
            del ary[(posy,posx)]
        else:
            #print "clean", names[dir_], "->", names[lefts[dir_]], "pos", posy, posx
            dir_ = lefts[dir_]
            ary[(posy,posx)] = 1

            # "Do not count nodes that begin infected." FUCK OFF
            #if (posy,posx) not in orig:
            bursts += 1

        vec = vecs[dir_]
        posy += vec[0]
        posx += vec[1]


    print "Part 1", bursts


def solve2():
    height, width = len(lines), len(lines[0])

    ary = {}

    for j,line in enumerate(lines):
        for i, c in enumerate(line):
            if c == '#':
                ary[(j,i)] = 2

    orig = deepcopy(ary)

    posx = width // 2
    posy = height // 2
    dir_ = DIR_UP

    bursts = 0

    for i in xrange(10000000):
        # do a burst

        # Clean
        if ary.get((posy,posx), 0) == 0:
            dir_ = lefts[dir_]
            ary[(posy,posx)] = 1

        # Weak
        elif ary.get((posy,posx), 0) == 1:
            ary[(posy,posx)] = 2

            # "Do not count nodes that begin infected." FUCK OFF
            #if (posy,posx) not in orig:
            bursts += 1

        # Infected
        elif ary.get((posy,posx), 0) == 2:
            dir_ = rights[dir_]
            ary[(posy,posx)] = 3

        # Flagged
        elif ary.get((posy,posx), 0) == 3:
            dir_ = reverses[dir_]
            del ary[(posy,posx)]

        vec = vecs[dir_]
        posy += vec[0]
        posx += vec[1]


    print "Part 2", bursts


if __name__ == "__main__":
    agent = aocd.Data(year=2017, day=22)
    data = agent.get_data()
    lines = data.strip().split("\n")
#    lines = """..#
##..
#...""".strip().split("\n")

    solve1()
    solve2()

import os
import sys

sys.path.append(os.getcwd() + "/..")
import aocd


agent = aocd.Data(year=2017, day=9)
data = agent.get_data().strip()


def solve(inp):
    root = []
    count = 0

    i = 0
    scorestack = []
    not_ = False
    garbage = False

    scorestack.append(0)

    gcount = 0
    gtot = 0

    for i, c in enumerate(inp):
        if not_:
            not_ = False
            continue

        not_ = False

        if garbage:
            if c == ">":
                gtot += gcount
                garbage = False
                continue
            elif c == "!":
                not_ = True
                continue
            else:
                gcount += 1

        else:
            if c == "{":
                scorestack.append(scorestack[-1] + 1)
            elif c == "}":
                count += scorestack.pop()
            elif c == "<":
                garbage = True
                gcount = 0
                continue
            elif c == ",":
                continue



    print "Part 1", count
    print "Part 2", gtot


#solve("{}")
#solve("{{{}}}")
#solve("{{},{}}")
#solve("{{{},{},{{}}}}")
#solve("{<a>,<a>,<a>,<a>}")
#solve("{{<ab>},{<ab>},{<ab>},{<ab>}}")
#solve("{{<!!>},{<!!>},{<!!>},{<!!>}}")
#solve("{{<a!>},{<a!>},{<a!>},{<ab>}}")
solve(data)

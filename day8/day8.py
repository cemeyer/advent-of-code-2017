import os
import sys

sys.path.append(os.getcwd() + "/..")
import aocd


def isint(foo):
    return foo.lstrip("-").isdigit()


agent = aocd.Data(year=2017, day=8)
data = agent.get_data()
lines = data.split("\n")


def getval(regval, regs):
    if isint(regval):
        return int(regval)
    return regs.get(regval, 0)


def solve():
    maxv = float("-inf")

    regs = {}
    for line in lines:
        words = line.split()
        dreg, op, amt, if_, cndreg, cnd, cndval = words

        cndregv = getval(cndreg, regs)
        cndcmpv = getval(cndval, regs)

        doit = False
        if cnd == ">" and cndregv > cndcmpv:
            doit = True
        elif cnd == "<" and cndregv < cndcmpv:
            doit = True
        elif cnd == ">=" and cndregv >= cndcmpv:
            doit = True
        elif cnd == "<=" and cndregv <= cndcmpv:
            doit = True
        elif cnd == "==" and cndregv == cndcmpv:
            doit = True
        elif cnd == "!=" and cndregv != cndcmpv:
            doit = True

        if not doit:
            continue

        if op == "inc":
            regs[dreg] = getval(dreg, regs) + int(amt)
        elif op == "dec":
            regs[dreg] = getval(dreg, regs) - int(amt)

        if getval(dreg, regs) > maxv:
            maxv = getval(dreg, regs)


    print "part1", max(regs.values())
    print "part2", maxv


solve()

import os
import sys

sys.path.append(os.getcwd() + "/..")
import aocd


def isint(foo):
    return foo.lstrip("-").isdigit()


class Day8VM(object):
    def __init__(self):
        self.regs = {}

    def getval(self, regval):
        if isint(regval):
            return int(regval)
        return self.regs.get(regval, 0)

    def execute_line(self, line):
        words = line.split()
        dreg, op, amt, if_, cndreg, cnd, cndval = words

        cndregv = self.getval(cndreg)
        cndcmpv = self.getval(cndval)

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
            return

        if op == "inc":
            self.regs[dreg] = self.getval(dreg) + int(amt)
        elif op == "dec":
            self.regs[dreg] = self.getval(dreg) - int(amt)


def solve():
    agent = aocd.Data(year=2017, day=8)
    data = agent.get_data()
    lines = data.split("\n")

    vm = Day8VM()
    maxv = None

    for line in lines:
        vm.execute_line(line)
        maxv = max(maxv, *vm.regs.values())

    print "part1", max(vm.regs.values())
    print "part2", maxv


if __name__ == "__main__":
    solve()

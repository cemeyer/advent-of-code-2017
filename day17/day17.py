import os
import sys

sys.path.append(os.getcwd() + "/..")
import aocd


def part1():
    buf = [0]
    pos = 0

    for i in range(2017):
        times = data % len(buf)
        pos += times
        pos %= len(buf)
        buf.insert(pos + 1, i + 1)
        #print buf
        pos = pos + 1

    dx = buf.index(2017)
    return buf[dx+1]


def part2():
    pos = 0
    out = 0
    for i in xrange(50000000):
        pos = ((pos + data) % (1 + i)) + 1
        if pos == 1:
            out = i + 1
    return out


if __name__ == "__main__":
    agent = aocd.Data(year=2017, day=17)
    data = int(agent.get_data())

    print "Part 1", part1()
    print "Part 2", part2()

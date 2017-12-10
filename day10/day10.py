import os
import sys

sys.path.append(os.getcwd() + "/..")
import aocd


def reverse(lnums, pos, ll):
    normal = min(len(lnums) - pos, ll)
    wrapped = ll - normal

    seq = lnums[pos:pos+normal] + lnums[:wrapped]
    seq.reverse()

    lnums[pos:pos+normal] = seq[:normal]
    lnums[:wrapped] = seq[normal:normal+wrapped]


def round_(lens, lnums, pos, skipsize):
    for l in lens:
        assert l <= 256

        reverse(lnums, pos, l)
        pos += l + skipsize
        pos = pos % len(lnums)
        skipsize += 1

    return (pos, skipsize)


def part1(lens1):
    lnums = range(256)
    round_(lens1, lnums, 0, 0)

    res = lnums[0] * lnums[1]
    print "part 1", res
    #agent.solve(1, str(res))


def part2(lens2):
    pos = 0
    skipsize = 0
    lnums = range(256)

    for i in range(64):
        pos, skipsize = round_(lens2, lnums, pos, skipsize)

    dhash = ""
    for i in range(16):
        r = 0
        for x in lnums[i*16:i*16+16]:
            r ^= x
        dhash += ("%02x" % r)
    print "part 2", dhash
    #agent.solve(2, dhash)


if __name__ == "__main__":
    agent = aocd.Data(year=2017, day=10)
    data = agent.get_data()

    lens1 = map(int, list(data.split(",")))
    part1(lens1)

    lens2 = map(ord, data.strip()) + [17, 31, 73, 47, 23]
    part2(lens2)

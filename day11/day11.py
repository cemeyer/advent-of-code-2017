import os
import sys

sys.path.append(os.getcwd() + "/..")
import aocd


def solve():
    pos = [0, 0, 0]
    maxdist = None
    for dir_ in data.split(","):
        dpos = {
                "n": (1,0,0),
                "s": (-1,0,0),
                "nw": (0,1,0),
                "se": (0,-1,0),
                "ne": (0,0,1),
                "sw": (0,0,-1),
                }[dir_]

        for i, dx in enumerate(dpos):
            pos[i] += dx

        tot = map(abs, pos)
        dist = sum(tot) - min(tot)
        maxdist = max(dist, maxdist)

    print "part 1", dist
    print "part 2", maxdist


if __name__ == "__main__":
    agent = aocd.Data(year=2017, day=11)
    data = agent.get_data()

    solve()

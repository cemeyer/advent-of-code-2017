import os
import sys

import networkx as nx
import numpy

sys.path.append(os.getcwd() + "/..")
import aocd


agent = aocd.Data(year=2017, day=6)
data = agent.get_data()
#lines = data.split("\n")

#data = "0 2 7 0"
ibanks = map(int, data.split())


def solve(ibanks, part2=False):
    count = 1

    seen = set()
    banks = ibanks

    seen.add( tuple(banks) )

    while True:
        mems, idx = sorted( map(lambda x: (x[1], -x[0]), list(enumerate(banks))) )[-1]
        idx = -idx

        banks[idx] = 0
        j = (idx + 1) % len(ibanks)
        while mems > 0:
            banks[j] += 1
            j = (j + 1) % len(ibanks)
            mems -= 1

        #print banks
        #print tuple(banks)
        #if count > 3:
        #    break

        t = tuple(banks)
        if t in seen:
            break

        seen.add(t)

        count += 1


    if part2:
        return solve(banks)
    else:
        print count
        return count


agent.solve(1, str(solve(ibanks)))
agent.solve(2, str(solve(ibanks, part2=True)))

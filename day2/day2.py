import os
import re
import sys

import networkx as nx

sys.path.append(os.getcwd() + "/..")
import aocd


agent = aocd.Data(year=2017, day=2)
data = agent.get_data()
lines = data.split("\n")


def solve1():
    count = 0
    for line in lines:
        nums = map(int, re.findall(r'\d+', line ))

        minn = 9999999999
        maxn = -9999999999

        for n in nums:
            if n < minn:
                minn = n
            if n > maxn:
                maxn = n

        count += (maxn - minn)

    print count
    agent.solve(1, str(count))


def solve2():
    count = 0
    for line in lines:
        nums = map(int, re.findall(r'\d+', line ))

        for n in nums:
            for m in nums:
                if (m % n) == 0 and m != n:
                    count += (m / n)
                    break

    print count
    agent.solve(2, str(count))

solve1()
solve2()

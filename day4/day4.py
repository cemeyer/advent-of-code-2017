import os
import sys

sys.path.append(os.getcwd() + "/..")
import aocd


agent = aocd.Data(year=2017, day=4)
data = agent.get_data()
lines = data.split("\n")


def solve():
    count = 0
    count2 = 0
    for line in lines:
        words = line.split()
        if len(words) == len(set(words)):
            count += 1

            if len(words) == len(set([frozenset(x) for x in words])):
                count2 += 1

    print count, count2
    agent.solve(1, str(count))
    agent.solve(2, str(count2))


solve()

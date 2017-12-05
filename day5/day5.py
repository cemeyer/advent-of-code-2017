import os
import sys

sys.path.append(os.getcwd() + "/..")
import aocd


agent = aocd.Data(year=2017, day=5)
data = agent.get_data()
lines = data.split("\n")

jumps = map(int, lines)


def solve(part):
    idx = 0
    count = 0

    while idx >= 0 and idx < len(jumps):
        nidx = idx + jumps[idx]
        if part == 2 and jumps[idx] >= 3:
            jumps[idx] -= 1
        else:
            jumps[idx] += 1
        idx = nidx

        count += 1

    print count
    agent.solve(part, str(count))


solve(1)
jumps = map(int, lines)
solve(2)

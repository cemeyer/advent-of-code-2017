import os
import re
import sys

sys.path.append(os.getcwd() + "/..")
import aocd


def step_i(state, dirs, ranges, i):
    if state[i] == (ranges[i] - 1) and dirs[i] == 1:
        dirs[i] = -1
    elif state[i] == 0 and dirs[i] == -1:
        dirs[i] = 1

    state[i] += dirs[i]


def solve():
    ranges = []
    for line in lines:
        nums = map(int, re.findall(r'\d+', line ))
        d,r = nums
        while len(ranges) < d:
            ranges.append(0)
        ranges.append(r)

    #print ranges

    state = [0] * len(ranges)
    dirs = [1] * len(ranges)
    #print state

    for i in range(len(ranges)):
        if ranges[i] <= 1:
            continue

        # Walk each clock forwards until it matches the time where our
        # packet encounters it.
        for j in range(i):
            step_i(state, dirs, ranges, i)
    #print state

    # Count collisions at start time = 0
    sev = 0
    for i in range(len(ranges)):
        if ranges[i] == 0:
            continue

        if state[i] == 0:
            #print "caught",i
            sev += (i * ranges[i])

    print "Part 1", sev

    # Exhaustively search for a starting time when we won't collide:
    ps = 0
    while True:
        ok = True
        for idx, x in enumerate(state):
            if x != 0 or ranges[idx] == 0:
                continue
            ok = False
            break
        
        if ok:
            print "Part 2", ps
            break

        for i in range(len(ranges)):
            if ranges[i] <= 1:
                continue

            step_i(state, dirs, ranges, i)
        ps += 1


if __name__ == "__main__":
    agent = aocd.Data(year=2017, day=13)
    data = agent.get_data()
    #data = """0: 3
    #1: 2
    #4: 4
    #6: 4"""
    lines = data.split("\n")

    solve()

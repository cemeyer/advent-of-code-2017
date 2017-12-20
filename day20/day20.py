import collections
import os
import re
import sys

if sys.subversion[0] == "PyPy":
    sys.path.append("/usr/lib/python2.7/site-packages")
else:
    print("USE PYPY")


sys.path.append(os.getcwd() + "/..")
import aocd


def solve():
    particles = {}
    psort = []

    idx = 0
    for line in lines:
        if line.strip() == "":
            continue
        nums = map(int, re.findall(r'-?\d+', line ))
        part = [nums[:3], nums[3:6], nums[6:9]]
        psort.append((sum(map(abs, part[2])), sum(map(abs, part[1])), sum(map(abs, part[0])), idx))
        particles[idx] = part
        idx += 1

    psort.sort()
    print "Part 1", psort[0][3]


    # Part 2:
    # Brute force simulation for a while to spot collisions.
    for it in xrange(1000):

        # Track collisions
        seen = {}
        remove = collections.defaultdict(set)

        # Update particle positions
        for idx, part in particles.iteritems():
            for j in range(3):
                part[1][j] += part[2][j]
            for j in range(3):
                part[0][j] += part[1][j]

            # Check for collisions
            t = tuple(part[0])
            if t in seen:
                remove[t].add(seen[t])
                remove[t].add(idx)
            else:
                seen[t] = idx

        # Remove any collided particles at the time of collision
        for k, v in remove.iteritems():
            for i in v:
                del particles[i]

        #print idx, part[0], dist(part)

    print "Part 2", len(particles)


if __name__ == "__main__":
    agent = aocd.Data(year=2017, day=20)
    data = agent.get_data()
    lines = data.split("\n")
    #lines = """p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
    #p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>
    #""".split("\n")

    solve()

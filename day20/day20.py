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


def solve(part2=False):
    particles = {}

    for idx, line in enumerate(lines):
        if line.strip() == "":
            continue

        app, avv, aaa, _ = line.strip().split(">")

        pnums = map(int, re.findall(r'-?\d+', app ))
        vnums = map(int, re.findall(r'-?\d+', avv ))
        anums = map(int, re.findall(r'-?\d+', aaa ))

        particles[idx] = [pnums, vnums, anums]


    closestdist = None
    closest = None

    def dist(part):
        return sum(map(abs, part[0]))

    # Brute force simulation for a while.  I suppose equivalently, you could
    # sort by absolute acceleration, then absolute velocity, then absolute
    # starting position.  But whatever, simulation was quick enough.
    for it in xrange(1000):
        seen = {}
        remove = collections.defaultdict(set)

        for idx, part in particles.iteritems():
            for j in range(3):
                part[1][j] += part[2][j]
            for j in range(3):
                part[0][j] += part[1][j]

            if part2:
                t = tuple(part[0])
                if t in seen:
                    remove[t].add(seen[t])
                    remove[t].add(idx)
                else:
                    seen[t] = idx

        if part2:
            for k, v in remove.iteritems():
                for i in v:
                    del particles[i]

            #print idx, part[0], dist(part)

    if not part2:
        for idx, part in particles.iteritems():
            if closestdist is None or dist(part) < closestdist:
                #print idx, closestdist, dist(part)
                closestdist = dist(part)
                closest = idx

        print "Part 1", closest
    else:
        print "Part 2", len(particles)


if __name__ == "__main__":
    agent = aocd.Data(year=2017, day=20)
    data = agent.get_data()
    lines = data.split("\n")
    #lines = """p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
    #p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>
    #""".split("\n")

    solve()
    solve(part2=True)

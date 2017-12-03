import os
import re
import sys

import networkx as nx

sys.path.append(os.getcwd() + "/..")
import aocd


agent = aocd.Data(year=2017, day=3)
data = agent.get_data()


def solve():
    puzzle = int(data)

    halfsq = 0
    area = 0
    while area < puzzle:
        dim = (halfsq * 2) + 1
        area = dim * dim
        halfsq += 1

    halfsq -= 1

    diff = area - puzzle

    print "dim", dim
    G = nx.generators.classic.grid_2d_graph(dim, dim)
    corner_distance = nx.shortest_path_length(G, (halfsq, halfsq), (0, 0))

    print "corner distance", corner_distance

    # Corner to corner doesn't change the distance.
    while diff > (dim - 1):
        diff -= (dim - 1)
        print "moved a corner"

    # Going towards the middle of a row/col, reduce distance
    if diff <= halfsq:
        part1 = corner_distance - diff
        print "short case"
    else:
        # Going back towards the corner, increase distance
        part1 = corner_distance - halfsq + (diff - halfsq)
        print "long case"

    print "part1", part1
    agent.solve(1, str(part1))
    #agent.solve(2, str(count))



solve()

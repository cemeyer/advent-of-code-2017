import binascii
import os
import sys

if sys.subversion[0] == "PyPy":
    sys.path.append("/usr/lib/python2.7/site-packages")

import networkx as nx

sys.path.append(os.getcwd() + "/..")
import aocd

sys.path.append(os.getcwd() + "/../day10")
import day10


def solve():
    count = 0
    inregion = False

    G = nx.generators.classic.grid_2d_graph(128, 128)

    for i in range(128):
        rowh = day10.knothash(data + "-%d" % i)

        rowb = binascii.unhexlify(rowh)
        for idx, b in enumerate(rowb):
            d = ord(b)
            for j in range(7, -1, -1):
                if (d & (1 << j)) != 0:
                    count += 1
                else:
                    G.remove_node( (i, idx * 8 + (7 - j)) )

    print "Part 1", count
    print "Part 2", len(list(nx.connected_components(G)))


if __name__ == "__main__":
    agent = aocd.Data(year=2017, day=14)
    data = agent.get_data().strip()

    solve()

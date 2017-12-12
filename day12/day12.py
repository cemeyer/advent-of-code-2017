import os
import sys

import networkx as nx

sys.path.append(os.getcwd() + "/..")
import aocd


def solve():
    G = nx.Graph()

    for line in lines:
        words = line.split()
        left = words[0]
        right = words[2:]

        G.add_node(left)
        for x in right:
            G.add_edge(left, x.rstrip(","))

    groups = list(nx.connected_components(G))
    for c in groups:
        if "0" in c:
            print "Part 1", len(c)
            break

    print "Part 2", len(groups)


if __name__ == "__main__":
    agent = aocd.Data(year=2017, day=12)
    data = agent.get_data()
    lines = data.split("\n")

    solve()

from copy import deepcopy
import os
import re
import sys

sys.path.append(os.getcwd() + "/..")
import aocd


agent = aocd.Data(year=2017, day=7)
data = agent.get_data()
lines = data.split("\n")

weights = {}
outrefs = {}
inrefs = {}

cumweights = {}


def solve():
    # Part 1 - Construct a graph representation of the input data
    count = 0
    for line in lines:
        name = line.split(" ")[0]
        weight = map(int, re.findall(r'\d+', line ))[0]

        weights[name] = weight
        if name not in inrefs:
            inrefs[name] = set()
        if name not in outrefs:
            outrefs[name] = set()

        if "->" in line:
            thalf = line.split("->")[1]
            refs = re.findall(r'\w+', thalf)
            for ref in refs:
                outrefs[name].add(ref)
                if ref not in inrefs:
                    inrefs[ref] = set()
                inrefs[ref].add(name)


    # Find the element with zero in-degree (tree root)
    for x, refs in inrefs.items():
        if len(refs) == 0:
            print "part1", x

    # Part 2: Calculate cumulative weights in topological order
    for x,y in weights.items():
        cumweights[x] = y

    remnames = set(weights.keys())
    
    ooutrefs = deepcopy(outrefs)

    # This part is the topo-sort / cumulative weight calculation
    while len(remnames) > 0:
        for x in remnames:
            if len(outrefs[x]) == 0:
                remnames.remove(x)
                assert len(inrefs[x]) <= 1
                for y in inrefs[x]:
                    outrefs[y].remove(x)
                    cumweights[y] += cumweights[x]
                break

    # Now that we have cumulative weight data, search for the node with unbalanced children
    res = []
    for x,y in ooutrefs.items():
        first = True
        val = None

        if len(set([cumweights[z] for z in y])) > 1:
            pop = {}
            for z in y:
                k = cumweights[z]
                pop[k] = (pop.get(k, (0, None))[0] + 1, z)

            # Compute a histogram to vote for which weight is correct.  For the
            # leaderboard, I just did this by hand rather than writing a
            # program.
            ((_, wrongname), wrong), (_, right) = sorted([(yy,xx) for (xx,yy) in pop.items()])
            diff = wrong - right

            # Multiple nodes can be unbalanced down-tree; we only care about
            # the leafiest one since we know only one can be out of balance.
            res.append((right, diff, wrongname))

    res = sorted(res)

    _, diff, nam = res[0]
    print "part2", weights[nam] - diff



solve()

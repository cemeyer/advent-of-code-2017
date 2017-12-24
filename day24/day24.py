import collections
import heapq
import os
import sys

if sys.subversion[0] != "PyPy":
    print("USE PYPY")

sys.path.append(os.getcwd() + "/..")
import aocd


# General library code
class HeapQ(list):
    def __init__(self, *args):
        list.__init__(self, *args)
        heapq.heapify(self)

    def heappush(self, itm):
        heapq.heappush(self, itm)

    def heappop(self):
        return heapq.heappop(self)


def bestfs(istate, score, validmoves, firstonly=False, part2=False):
    best = 999999999999999999
    bestsc = 999999999999999999
    queue = HeapQ()
    queue.heappush((0, 0, istate))

    while len(queue) > 0:
        _, _, state = queue.heappop()
        sc_len, sc_tot = score(state)
        if part2:
            if sc_len < best:
                best = sc_len
                bestsc = sc_tot
            elif sc_len == best and sc_tot < bestsc:
                bestsc = sc_tot
        else:
            if sc_tot < bestsc:
                bestsc = sc_tot

        # validmoves() responsible for generating directly adjacent
        # state.
        for move in validmoves(state):
            # Score is responsible for prioritizing states.  Lower is
            # better.
            sc_len, sc_tot = score(move)
            queue.heappush((sc_len, sc_tot, move))

    return bestsc


def score(st):
    seq, _, _ = st

    return (-len(seq), -sum(map(sum, seq)))


def validmoves(st):
    seq, free, rem = st

    for id_, x in enumerate(rem):
        if free == x[0]:
            yield (seq + [x], x[1], rem[:id_] + rem[id_+1:])
        elif free == x[1]:
            yield (seq + [x], x[0], rem[:id_] + rem[id_+1:])


def solve():
    P = []
    for line in lines:
        x = map(int, line.split("/"))
        P.append(x)

    x = bestfs( ([], 0, P), score, validmoves )
    print "Part 1", -x
    x = bestfs( ([], 0, P), score, validmoves, part2=True )
    print "Part 2", -x


if __name__ == "__main__":
    agent = aocd.Data(year=2017, day=24)
    data = agent.get_data()
    lines = data.strip().split("\n")

    solve()

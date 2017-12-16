import os
import sys

sys.path.append(os.getcwd() + "/..")
import aocd

def solve():
    seen = {}
    state = [chr(ord('a') + x) for x in range(16)]
    #print state
    seen["".join(state)] = 0
    state = solve1(state)
    seen["".join(state)] = 1
    print "Part 1", "".join(state)


    for i in xrange(1000*1000*1000 - 1):
        state = solve1(state)
        st = "".join(state)
        if st in seen:
            #print "Seen", st, seen[st], i + 2
            break
        else:
            seen[st] = i + 2

    cyclelen = len(seen)

    mod = (1000*1000*1000) % cyclelen
    for k, v in seen.iteritems():
        if v == mod:
            print "Part 2", k
            break


def solve1(state):
    for mov in moves:
        if mov.startswith("s"):
            n = int(mov[1:])
            tail = state[len(state) - n:]
            head = state[:len(state) - n]
            state = tail + head
            assert len(state) == 16

        elif mov.startswith("p"):
            A, B = mov[1:].split("/")
            pA = state.index(A)
            pB = state.index(B)

            state[pA] = B
            state[pB] = A

        elif mov.startswith("x"):
            pA, pB = map(int, mov[1:].split("/"))

            t = state[pB]
            state[pB] = state[pA]
            state[pA] = t
    return state


if __name__ == "__main__":
    agent = aocd.Data(year=2017, day=16)
    data = agent.get_data()
    moves = data.strip().split(",")

    solve()

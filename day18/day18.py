import collections
import os
import sys
import threading
import Queue as q

sys.path.append(os.getcwd() + "/..")
import aocd


def isint(foo):
    return foo.lstrip("-").isdigit()


def get(regs, x):
    if isint(x):
        return int(x)
    else:
        return regs[x]


def solve(inq, outq, pid, part=2):
    regs = collections.defaultdict(int)
    regs['p'] = pid
    lastsnd = None
    pc = 0
    count = 0

    while pc < len(lines):
        line = lines[pc]

        words = line.split()

        verb = words[0]
        if verb == "set":
            regs[words[1]] = get(regs, words[2])
        elif verb == "add":
            regs[words[1]] += get(regs, words[2])
        elif verb == "mul":
            regs[words[1]] *= get(regs, words[2])
        elif verb == "mod":
            regs[words[1]] = regs[words[1]] % get(regs, words[2])
        elif verb == "rcv":
            if part == 1:
                if get(regs, words[1]) != 0:
                    print "Part 1", lastsnd
                    break
            else:
                regs[words[1]] = inq.get(True)
        elif verb == "snd":
            if part == 1:
                lastsnd = get(regs, words[1])
            else:
                if pid == 1:
                    count += 1
                    print "Part 2", count
                outq.put(get(regs, words[1]), True)
        elif verb == "jgz":
            if get(regs, words[1]) > 0:
                pc = pc + get(regs, words[2]) - 1
        else:
            assert False, line

        pc += 1


if __name__ == "__main__":
    agent = aocd.Data(year=2017, day=18)
    data = agent.get_data()
    lines = data.split("\n")

    solve(None, None, 0, part=1)

    a = q.Queue(999999)
    b = q.Queue(999999)
    c = threading.Thread(target=solve, args=(a, b, 0, 2))
    d = threading.Thread(target=solve, args=(b, a, 1, 2))
    c.start()
    d.start()
    c.join()
    d.join()

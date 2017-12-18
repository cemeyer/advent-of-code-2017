import collections
import os
import sys

sys.path.append(os.getcwd() + "/..")
import aocd


def isint(foo):
    return foo.lstrip("-").isdigit()


def get(regs, x):
    if isint(x):
        return int(x)
    else:
        return regs[x]


def runmachine(inq, pid, part=2, state=None):
    if state is None:
        regs = collections.defaultdict(int)
        regs['p'] = pid
        pc = 0
    else:
        regs, pc = state

    lastsnd = None
    outq = []

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
                if len(inq) > 0:
                    regs[words[1]] = inq.pop(0)
                else:
                    return (False, outq, (regs, pc))

        elif verb == "snd":
            if part == 1:
                lastsnd = get(regs, words[1])
            else:
                outq.append(get(regs, words[1]))

        elif verb == "jgz":
            if get(regs, words[1]) > 0:
                pc = pc + get(regs, words[2]) - 1

        else:
            assert False, line

        pc += 1

    return (True, outq, (regs, pc))


def solve2():
    ins = [[], []]
    states = [None, None]
    exited = [False, False]
    stuck = [False, False]

    count = 0

    pid = 0
    while True:
        opid = int(not pid)

        if exited[pid] and exited[opid]:
            print "Both exited"
            break
        if exited[opid] and stuck[pid] and len(ins[pid]) == 0:
            print "Stuck and the other guy is gone"
            break
        if stuck[pid] and stuck[opid] and len(ins[pid]) == 0 and len(ins[opid]) == 0:
            print "Deadlock"
            break

        if not exited[pid]:
            #print "Running", pid
            exit_, outs, state = runmachine(ins[pid], pid, state=states[pid])
            #print "Clean exit?", exit_, "Outputs:", len(outs)

            if pid == 1:
                count += len(outs)

            states[pid] = state
            if exit_:
                exited[pid] = True
            else:
                stuck[pid] = True

            ins[opid].extend(outs)

        pid = opid

    print "Part 2", count



if __name__ == "__main__":
    agent = aocd.Data(year=2017, day=18)
    data = agent.get_data()
    lines = data.split("\n")

    # Part 1
    runmachine(None, 0, part=1)

    # Part 2
    solve2()

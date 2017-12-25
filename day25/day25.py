import collections
import sys


if sys.subversion[0] != "PyPy":
    print("USE PYPY")


def solve():
    state = None
    curval = None
    begin = None
    nsteps = None

    statem = collections.defaultdict(list)

    # Parsing the state machine was totally stupid given the size of it :-(.
    # Should have just hand-transcribed it.  This would work nicely on a much
    # larger input state machine description, though.

    for line in lines:
        if line.startswith("Begin in"):
            begin = line.split()[-1].rstrip(".")
            #print "begin", begin
        elif line.startswith("Perform a diagnost"):
            nsteps = int(line.split()[-2])
            #print "nsteps", nsteps
        elif line.startswith("In state"):
            state = line.split()[-1].rstrip(":")
            #print "in state", state

        elif line.lstrip(" ").startswith("If the current"):
            curval = int(line.split()[-1].rstrip(":"))
            #print "curval", curval

        elif "Write the value" in line:
            xxx = line.split()[-1].rstrip(".")
            #print state, curval, "write", xxx
            statem[(state, curval)].append(("write", int(xxx)))

        elif "Move one slot" in line:
            xxx = line.split()[-1].rstrip(".")
            #print state, curval, "move", xxx
            statem[(state, curval)].append(("move", xxx))

        elif "Continue with" in line:
            xxx = line.split()[-1].rstrip(".")
            #print state, curval, "continue", xxx
            statem[(state, curval)].append(("continue", xxx))

        elif line.strip() == "":
            continue

        else:
            assert "Parse error", line

    # Run the state machine for a while
    cursor = 0
    ones = 0
    state = begin
    tape = collections.defaultdict(int)

    for i in xrange(nsteps):
        curval = tape[cursor]
        #print repr((state, curval))
        instr = statem[(state, curval)]
        #print instr
        for j in instr:
            mn, op = j
            if mn == "write":
                #print cursor, tape[cursor], repr(op)
                if tape[cursor] == 0 and op == 1:
                    ones += 1
                elif tape[cursor] == 1 and op == 0:
                    ones -= 1
                tape[cursor] = op
            elif mn == "move":
                if op == "left":
                    cursor -= 1
                elif op == "right":
                    cursor += 1
                else:
                    assert False, "move " + op
            elif mn == "continue":
                state = op

    print "Part 1", ones


if __name__ == "__main__":
    data = open("input.txt", "rb").read()
    lines = data.strip().split("\n")

    solve()

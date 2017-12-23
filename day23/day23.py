import collections
import math
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

def factors(n):
    step = 2 if n%2 else 1
    result = set()

    for i in xrange(1, int(math.sqrt(n)) + 1, step):
        if n % i == 0:
            result.add(i)
            result.add(n // i)
    return result


def runmachine(part2=False, limit=None):
    regs = collections.defaultdict(int)
    pc = 0

    f = None
    if part2:
        f = open("trace.log", "wb")
        regs['a'] = 1

        # a = 1 leads to b starting 100x larger

        # LINE 11-19 inner loop META
        # do {

        # 11: set g d [g = -107880 -> 2]
        # 12: mul g e [g = 2 -> 40]
        # 13: sub g b [g = 40 -> -107860]

        # g = d * e - b

        # 14: jnz g 2 [g = -107860]

        # if (g != 0)  // mostly false

        # 15: set f 0

        #     f = 0;

        # 16: sub e -1 [e = 20 -> 21]
        # 17: set g e [g = -107860 -> 21]
        # 18: sub g b [g = 21 -> -107879]

        # g = ++e - b;

        # 19: jnz g -8 [g = -107879]

        # } while (++e - b != 0)

        # End result of this loop:
        # e == b (107900)
        # if d * e == b, for any e in [initial, b] f is zero
        #   aka, does d divide b.
        # g is zero

        # Or:
        # for e in [e, b]:
        #   if b % d == 0:
        #     f = 0


        # LINE 10-23 Outer loop META

        # do {

        #10: set e 2 [e = 107900 -> 2]
        #11: META: e := b (107900); g := 0; pc := 20

        #     e = 2;
        #     loop11_19();

        #20: sub d -1 [d = 107893 -> 107894]
        #21: set g d [g = 0 -> 107894]
        #22: sub g b [g = 107894 -> -6]
        #23: jnz g -13 [g = -6]

        # } while (++d != b);

        # Or:
        # Does any number in d == [2, b) factor b? 


        # LINE 8-31 Outer Outer loop META:

        # do {

        # 8: set f 1 [f = 0 -> 1]
        # 9: set d 2 [d = 0 -> 2]
        # 10: META: d, e := b (107900); f := 0 (b is factorable); g := 0; pc := 24
        # 24: jnz f 2 [f = 0]
        # 25: sub h -1 [h = 0 -> 1]

        # if (factorable(b))
        #     h++;

        # 26: set g b [g = 0 -> 107900]
        # 27: sub g c [g = 107900 -> -17000]
        # 28: jnz g 2 [g = -17000]
        # 29: jnz 1 3

        # if (b == c)
        #     exit();

        # 30: sub b -17 [b = 107900 -> 107917]

        # b += 17;

        # 31: jnz 1 -23
        # } while (true);


        # LINE 0-31 Whole program META:
        # 
        # b = 79
        # c = b
        # if (debug mode) {
        #   b = b * 100 + 100000;
        #   c = b + 17000
        # }
        #
        # for (; b < c; b += 17) {
        #   if (factorable(b))
        #     h++;
        # }


    count = 0

    while pc < len(lines) and (limit is None or limit > 0):
        line = lines[pc]
        words = line.split()
        set_ = False

        # Meta emu:
        if part2:

            # Innermost loop
            if pc == 11:
                regs['e'] = regs['b']

                if f:
                    f.write("%d: META: e := b (%s);" % (pc, regs['b']))

                if (regs['b'] % regs['d']) == 0:
                    regs['f'] = 0

                    if f:
                        f.write(" f := 0 (b %% d (%s) == 0);" % (regs['d']))

                regs['g'] = 0
                pc = 20

                if f:
                    f.write(" g := 0; pc := 20\n")

                if limit is not None:
                    limit -= 1
                continue

            # 2ndmost inner loop
            elif pc == 10:
                regs['d'] = regs['b']
                regs['e'] = regs['b']

                fs = factors(regs['b'])
                foundfact = False
                # print "Factors of", regs['b'], fs
                for fact in fs:
                    if fact >= 2 and fact < regs['b']:
                        foundfact = True
                        regs['f'] = 0
                        break

                regs['g'] = 0
                pc = 24

                if f:
                    f.write("10: META: d, e := b (%s);" % (regs['b'],))
                    if foundfact:
                        f.write(" f := 0 (b is factorable);")
                    f.write(" g := 0; pc := 24\n")

                if limit is not None:
                    limit -= 1
                continue


        if f:
            f.write("%d: %s" % (pc, line))
            if not isint(words[1]):
                f.write(" [%s = %s" % (words[1], regs[words[1]]))

        verb = words[0]

        if verb == "set":
            regs[words[1]] = get(regs, words[2])
            set_ = True

        elif verb == "sub":
            regs[words[1]] -= get(regs, words[2])
            set_ = True

        elif verb == "mul":
            count += 1
            regs[words[1]] *= get(regs, words[2])
            set_ = True

        elif verb == "jnz":
            if get(regs, words[1]) != 0:
                pc = pc + get(regs, words[2]) - 1

        else:
            assert False, line

        if f:
            if not isint(words[1]):
                if set_:
                    f.write(" -> %s" % regs[words[1]])
                f.write("]")
            f.write("\n")

        pc += 1
        if limit is not None:
            limit -= 1

    if part2 and limit is not None and limit != 0:
        print "Part 2", regs['h']
    return count


def solve():
    print "Part 1", runmachine()
    runmachine(part2=True, limit=1000 * 1000)


if __name__ == "__main__":
    agent = aocd.Data(year=2017, day=23)
    data = agent.get_data()
    lines = data.strip().split("\n")

    solve()

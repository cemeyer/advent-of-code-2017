import gmpy2
import itertools
import os
import sys

if sys.subversion[0] == "PyPy":
    sys.path.append("/usr/lib/python2.7/site-packages")
else:
    # This one runs in 4.1 seconds in Pypy, 22.2 seconds in CPython
    print("USE PYPY")


sys.path.append(os.getcwd() + "/..")
import aocd


def gen(start, factor, mod):
    a = start
    while True:
        a = (factor * a ) % 2147483647
        if (a % mod) == 0:
            yield a


def countsimilarseq(a, b, limit):
    count = 0

    c = itertools.izip(a, b)

    for i, (x, y) in enumerate(c):
        if i >= limit:
            break
        if (x & 0xffff) == (y & 0xffff):
            count += 1

    return count


def reverse_lcg(output, n, factor, mod):
    # factor^n * x = output mod mod

    mult = gmpy2.powmod(factor, n, mod)
    x = gmpy2.divm(output, mult, mod)
    return int(x)


def solve():
    a = gen(A, 16807, 1)
    b = gen(B, 48271, 1)
    print "Part 1", countsimilarseq(a, b, 40 * 1000 * 1000)

    a = gen(A, 16807, 4)
    b = gen(B, 48271, 8)
    print "Part 2", countsimilarseq(a, b, 5 * 1000 * 1000)

    #a = gen(A, 16807, 1)
    #for idx in xrange(40 * 1000 * 1000):
    #    assert reverse_lcg(next(a), idx + 1, 16807, 2147483647) == A
    #b = gen(B, 48271, 1)
    #for idx in xrange(40 * 1000 * 1000):
    #    assert reverse_lcg(next(b), idx + 1, 48271, 2147483647) == B


if __name__ == "__main__":
    agent = aocd.Data(year=2017, day=15)
    A = 618
    B = 814

    solve()

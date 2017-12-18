import z3

# Proof mode is slower, so disable it by default.
#z3.set_param(proof=True)

mod = (1<<31) - 1
mult = 8505 * 129749
add = 12345
outmod = 10000

lcg_verbose = True
def day18_lcg(seed):
    if lcg_verbose:
        print "Seed", seed

    n = seed
    i = 1
    while True:
        n = ((n * mult) + add) % mod
        if lcg_verbose:
            print "State", i, "=", n
            i += 1
        yield (n % outmod)


# Mersenne mod trick
# Vastly (~4x) faster than z3.URem for Mersenne modulus.
# Precondition: n < 2**62
def m31_mod(n):
    x = (n & mod)
    y = n >> 31
    n = x + y
    x = (n & mod)
    y = n >> 31
    n = x + y
    return n


lcg = day18_lcg(680)
s = z3.Solver()

# Any value >= the modulus is equivalent, so rule out large values to narrow
# solution space.  Proof takes about 40s on my Haswell-era Xeon.
seed = z3.BitVec('seed', 66)
s.add(seed >= 0, seed < mod)
#s.add(seed >= 0, seed < 1000)

# Start adding constraints to find the seed from a series of outputs.  In my
# testing, only two observed outputs were necessary to find the correct seed.
num_outputs = 2
states = {0: seed}
for i in range(1, num_outputs + 1):
    # Each intermediary state is a function of the previous state (doesn't need
    # an independent z3 variable):
    states[i] = m31_mod((states[i - 1] * mult) + add)

    # Add constraint based on observed output:
    s.add(z3.URem(states[i], outmod) == next(lcg))

# Run the solver!
if s.check() == z3.unsat:
    print "If this happens, enable proof mode w/ z3.set_param above and re-run."
    print s.proof()
    exit()

res = s.model()
print "Solved model:", res

# Test our model:
lcg_verbose = False
# Couldn't find a better way to extract an integer from a z3 BitVec ...
test_model = day18_lcg(int(str( res[seed] )))
test_lcg = day18_lcg(680)

ok = True
for i in range(10):
    a, b = next(test_model), next(test_lcg)
    if a != b:
        ok = False
        print "Difference at #", i, ":", a, "!=", b

if ok:
    print "Model matches ok!"

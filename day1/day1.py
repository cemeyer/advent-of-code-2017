import os
import sys

sys.path.append(os.getcwd() + "/..")
import aocd

foo = aocd.get_data(year=2017, day=1)

total = 0
for i, j in enumerate(foo):
    nexti = (i + (len(foo) / 2)) % len(foo)
    if (j == foo[nexti]):
        total += int(j)

print total

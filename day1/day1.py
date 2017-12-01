import os
import sys

sys.path.append(os.getcwd() + "/..")
import aocd

agent = aocd.Data(year=2017, day=1)
foo = agent.get_data()

def part1():
    total = 0
    for i, j in enumerate(foo):
        nexti = (i + 1) % len(foo)
        if (j == foo[nexti]):
            total += int(j)

    print total
    agent.solve(1, str(total))

def part2():
    total = 0
    for i, j in enumerate(foo):
        nexti = (i + (len(foo) / 2)) % len(foo)
        if (j == foo[nexti]):
            total += int(j)

    print total
    agent.solve(2, str(total))

#part1()
#part2()

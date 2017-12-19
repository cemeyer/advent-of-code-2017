import os
import sys

sys.path.append(os.getcwd() + "/..")
import aocd


def solve():
    seen = []

    pos = None
    for x, c in enumerate(lines[0]):
        if c == '|':
            pos = (x, 0)

    #print pos

    dir_ = (0, 1)
    steps = 0
    while True:

        pos = (pos[0] + dir_[0], pos[1] + dir_[1])
        steps += 1

        c = lines[pos[1]][pos[0]]

        #print pos, c

        if c.isupper():
            seen.append(c)
            continue

        # End
        if c == ' ':
            break

        if c == '|' or c == '-':
            continue

        if c == '+':
            found = False
            for dx in [-1,0,1]:
                if found:
                    break
                for dy in [-1,0,1]:

                    if dx == -dir_[0] and dy == -dir_[1]:
                        continue

                    nx = pos[0] + dx
                    ny = pos[1] + dy

                    if nx < 0 or nx >= len(lines[0]):
                        continue
                    if ny < 0 or ny >= len(lines):
                        continue

                    if nx == pos[0] and ny == pos[1]:
                        continue

                    if lines[ny][nx] == ' ':
                        continue
                    
                    dir_ = (dx, dy)
                    #pos = (nx, ny)
                    found = True
                    break

            if found:
                continue
            else:
                assert False

        else:
            print "Unexpected", c

    print "Part 1", "".join(seen)
    print "Part 2", steps


#lines = \
#"""     |          
#     |  +--+    
#     A  |  C    
# F---|----E|--+ 
#     |  |  |  D 
#     +B-+  +--+""".split("\n")
if __name__ == "__main__":
    agent = aocd.Data(year=2017, day=19)
    data = agent.get_data()
    lines = data.split("\n")

    solve()

foo = open("input.txt", "rb").read().strip()

total = 0
for i, j in enumerate(foo):
    if (i == (len(foo) - 1) and j == foo[0]) or (j == foo[i+1]):
        total += int(j)

print total

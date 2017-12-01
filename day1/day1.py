foo = open("input.txt", "rb").read().strip()

total = 0
for i, j in enumerate(foo):
    nexti = (i + (len(foo) / 2)) % len(foo)
    if (j == foo[nexti]):
        total += int(j)

print total

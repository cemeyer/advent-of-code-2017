import os
import sys

sys.path.append(os.getcwd() + "/..")
import aocd


# cc -Wall -Wextra -Wno-unused-label -O3 -g ./day23_xlate.c
# ./a.out

# The naive approach takes longer than a few seconds.  Not tractable.  The
# compiler is unable to optimize out any of the three levels of loop.

# Optimizing just the inner loop makes it very tractable:
# h: 907
# ./a.out  0.91s user 0.00s system 99% cpu 0.913 total
#
# With Python, I have to optimize both inner loops before it becomes tractable.
# Advantage, optimizing compiler + amd64.


def xlate():
    f = open("day23_xlate.c", "wb")

    f.write("#include <stdint.h>\n")
    f.write("#include <stdio.h>\n")
    f.write("\n")

    f.write("int64_t a,b,c,d,e,f,g,h;\n")
    f.write("\n")

    f.write("int main(int argc, char **argv) {\n")
    f.write("(void)argc; (void)argv;\n")
    f.write("a = 1;\n");

    for i, line in enumerate(lines):
        words = line.split()
        verb = words[0]

        # Skip inner loop
        if i > 11 and i < 20:
            continue

        f.write("L%d:\n" % i)

        # Optimize inner loop
        if i == 11:
            f.write("// L11-19 loop\n")
            f.write("e = b;\n")
            f.write("g = 0;\n")
            f.write("if ((b % d) == 0)\n")
            f.write("\tf = 0;\n")
            f.write("goto L20;\n")
            continue

        if verb == "set":
            f.write("%s = %s;\n" % (words[1], words[2]))
            if i == 15:
                f.write("goto L20;\t// found factor\n")

        elif verb == "sub":
            f.write("%s -= %s;\n" % (words[1], words[2]))

        elif verb == "mul":
            f.write("%s *= %s;\n" % (words[1], words[2]))

        elif verb == "jnz":
            f.write("if (%s != 0)\n" % words[1])
            f.write("\tgoto L%d;\n" % (i + int(words[2])))

        else:
            assert False, line

    f.write("\n")
    f.write("L32:\n")
    f.write("printf(\"h: %jd\\n\", (intmax_t)h);\n")
    f.write("return 0;\n")
    f.write("}\n")
    f.flush()
    f.close()


if __name__ == "__main__":
    agent = aocd.Data(year=2017, day=23)
    data = agent.get_data()
    lines = data.strip().split("\n")

    xlate()

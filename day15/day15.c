#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

unsigned
next(unsigned prev, unsigned factor, unsigned mod)
{
	uint64_t a = prev;

	while (true) {
		a = (factor * a) % 2147483647;
		if ((a % mod) == 0)
			return (a);
	}
}

unsigned
countsimilar(unsigned a, unsigned b, unsigned limit, unsigned amod, unsigned bmod)
{
	unsigned i, count;
	count = 0;
	for (i = 0; i < limit; i++) {
		a = next(a, 16807, amod);
		b = next(b, 48271, bmod);

		if ((a & 0xffff) == (b & 0xffff))
		       count++;	
	}
	return (count);
}

int
main(int argc, char **argv)
{
	unsigned A = 618, B = 814;

	printf("Part 1 %u\n", countsimilar(A, B, 40*1000*1000, 1, 1));
	printf("Part 2 %u\n", countsimilar(A, B, 5*1000*1000, 4, 8));
	return (0);
}

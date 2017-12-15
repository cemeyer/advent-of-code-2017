#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

unsigned
mod_mersenne(uint64_t n, unsigned bits, unsigned mers)
{
	unsigned x, y;

	//assert(mers == ((1<<bits) - 1));

	/*
	 * The general purpose algorithm here repeats the loop until n < mers.
	 * However, given 'factor' is smaller than mers, the product must be
	 * fewer than '2 * bits' bits, 'x + y' after the first loop is at most
	 * 'bits + 1' bits, and thus we require at most two loops.
	 */

	x = n & mers;
	y = n >> bits;
	n = x + y;

	x = n & mers;
	y = n >> bits;
	n = x + y;

	//assert(n < mers);

	return ((unsigned)n);
}

unsigned
next(unsigned prev, unsigned factor, unsigned mask)
{
	uint64_t a = prev;

	while (true) {
		a = mod_mersenne(factor * a, 31, 2147483647);
		if ((a & mask) == 0)
			return (a);
	}
}

unsigned
countsimilar(unsigned a, unsigned b, unsigned limit, unsigned amask, unsigned bmask)
{
	unsigned i, count;
	count = 0;
	for (i = 0; i < limit; i++) {
		a = next(a, 16807, amask);
		b = next(b, 48271, bmask);

		if ((a & 0xffff) == (b & 0xffff))
		       count++;	
	}
	return (count);
}

int
main(int argc, char **argv)
{
	unsigned A = 618, B = 814;

	printf("Part 1 %u\n", countsimilar(A, B, 40*1000*1000, 0, 0));
	printf("Part 2 %u\n", countsimilar(A, B, 5*1000*1000, 3, 7));
	return (0);
}

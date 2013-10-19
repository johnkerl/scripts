#include "gcd.h"

// ----------------------------------------------------------------
unsigned gcd(unsigned m, unsigned n)
{
	unsigned r;

	if (m == 0)
		return 0;
	if (n == 0)
		return 0;

	while (1) {
		r = m % n;
		if (r == 0)
			break;
		m = n;
		n = r;
	}

	return n;
}

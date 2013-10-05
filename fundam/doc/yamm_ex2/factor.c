#include <stdio.h>
#include "factor.h"

// ----------------------------------------------------------------
void factor(unsigned n)
{
	unsigned i;
	unsigned power;

	printf("%u: ", n);
	if (n <= 1) {
		printf("%u\n", n);
		return;
	}

	for (i = 2; n > 1; i++) {

		//if ((i & 0x3fff) == 0) {
			//printf(".");
			//fflush(stdout);
		//}

		power = 0;
		while ((n % i) == 0) {
			power++;
			n /= i;
		}
		if (power > 1)
			printf(" %u^%u", i, power);
		else if (power == 1)
			printf(" %u", i);
	}
	printf("\n");
}

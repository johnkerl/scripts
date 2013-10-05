#include <stdio.h>
#include "cmdgcd.h"
#include "gcd.h"

static void execute_gcd(
	int argc, char ** argv, char * long_help, void * pvparams)
{
	unsigned m, n, g;

	if (argc != 3) {
		printf("%s\n", long_help);
		return;
	}
	if (sscanf(argv[1], "%u", &m) != 1) {
		printf("%s\n", long_help);
		return;
	}
	if (sscanf(argv[2], "%u", &n) != 1) {
		printf("%s\n", long_help);
		return;
	}

	g = gcd(m, n);
	printf("GCD(%u, %u) = %u\n", m, n, g);
}

cmd_info_t gcd_info = {
	"gcd",
	"Print the Euclidean GCD of two specified numbers.",
	"gcd {m} {n}:  Print the Euclidean GCD of m and n.",
	execute_gcd
};

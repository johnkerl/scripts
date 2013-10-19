#include <stdio.h>
#include "cmdfactor.h"
#include "factor.h"

static void execute_factor(
	int argc, char ** argv, char * long_help, void * pvparams)
{
	int argi;
	unsigned n;

	if (argc < 2) {
		printf("%s\n", long_help);
		return;
	}
	for (argi = 1; argi < argc; argi++) {
		if (sscanf(argv[argi], "%u", &n) != 1) {
			printf("%s\n", long_help);
		}
		else {
			factor(n);
		}
	}
}

cmd_info_t factor_info = {
	"factor",
	"Print the prime factors of a specified number.",
	"factor {n}:  Print the prime factors of a specified number.",
	execute_factor
};

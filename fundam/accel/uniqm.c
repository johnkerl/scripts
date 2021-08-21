/*
Build instructions: see Makefile
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "lib/util.h"
#include "lib/hss.h"

#include "argf.h"

#define MYBUFSIZ 2048
static char line[MYBUFSIZ];

int main(int argc, char** argv) {
	argf_t* pargf = argf_alloc(argv[0], argv+1, argc-1);
	int error = 0;
	hss_t* pset = hss_alloc();

	while (argf_fgets(pargf, line, MYBUFSIZ, &error) != NULL) {
		if (!hss_has(pset, line)) {
			fputs(line, stdout);
			hss_add(pset, strdup(line));
		}
	}
	argf_free(pargf);
	if (error) {
		return 1;
	}

	return 0;
}

/*
Build instructions:
gcc -std=c99 -O3 -I $mlc $mlc/lib/mlr_globals.c $mlc/lib/mlrutil.c $mlc/containers/hss.c argf.c uniqm.c -o uniqm
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "lib/mlrutil.h"
#include "lib/mlr_globals.h"
#include "containers/hss.h"

#include "argf.h"

#define MYBUFSIZ 2048
static char line[MYBUFSIZ];

int main(int argc, char** argv) {
	mlr_global_init(argv[0], NULL);
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

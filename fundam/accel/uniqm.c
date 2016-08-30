// Build instructions:
// gcc -std=c99 -O3 -I $mlc $mlc/lib/mlr_globals.c $mlc/lib/mlrutil.c $mlc/containers/hss.c uniqm.c -o uniqm

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "lib/mlrutil.h"
#include "lib/mlr_globals.h"
#include "containers/hss.h"

#define MYBUFSIZ 2048
static char buf[MYBUFSIZ];

int main(int argc, char** argv) {
	mlr_global_init(argv[0], NULL);

	hss_t* pset = hss_alloc();

	if (argc == 1) {
		while (fgets(buf, MYBUFSIZ, stdin)) {
			if (!hss_has(pset, buf)) {
				fputs(buf, stdout);
				hss_add(pset, strdup(buf));
			}
		}
	} else {
		for (int argi = 1; argi < argc; argi++) {
			char* filename = argv[argi];
			FILE* fp = fopen(filename, "r");
			if (fp == NULL) {
				fprintf(stderr, "%s: Couldn't open \"%s\" for read.\n",
					argv[0], filename);
				exit(1);
			}
			while (fgets(buf, MYBUFSIZ, fp)) {
				if (!hss_has(pset, buf)) {
					fputs(buf, stdout);
					hss_add(pset, strdup(buf));
				}
			}
			fclose(fp);
		}
	}

	return 0;
}

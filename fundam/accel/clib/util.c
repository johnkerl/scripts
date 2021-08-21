#include <stdio.h>
#include <stdlib.h>
#include "util.h"

// ----------------------------------------------------------------
void* mlr_malloc_or_die(size_t size) {
	void* p = malloc(size);
	if (p == NULL) {
		fprintf(stderr, "malloc(%lu) failed.\n", (unsigned long)size);
		exit(1);
	}
	return p;
}

// ----------------------------------------------------------------
// This is djb2.
int mlr_string_hash_func(char *str) {
	unsigned long hash = 5381;
	int c;

	while ((c = *str++) != 0)
		hash = ((hash << 5) + hash) + c; /* hash * 33 + c */

	return (int)hash;
}

// ----------------------------------------------------------------
void mlr_internal_coding_error(char* file, int line) {
	fprintf(stderr, "internal coding error detected in file %s at line %d.\n",
		file, line);
	exit(1);
}

void mlr_internal_coding_error_if(int v, char* file, int line) {
	if (v) {
		mlr_internal_coding_error(file, line);
	}
}

void mlr_internal_coding_error_unless(int v, char* file, int line) {
	if (!v) {
		mlr_internal_coding_error(file, line);
	}
}


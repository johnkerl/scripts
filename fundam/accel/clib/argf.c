/*
Build instructions: see Makefile
*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "argf.h"

static char* files_fgetter(argf_t* pargf, char * restrict str, int size, int* perr);
static char* stdin_fgetter(argf_t* pargf, char * restrict str, int size, int* perr);
static char* err_fgetter(argf_t* pargf, char * restrict str, int size, int* perr);
static char* eof_fgetter(argf_t* pargf, char * restrict str, int size, int* perr);

static void* malloc_or_die(size_t size);
static char * strdup_or_die(const char *s1);

// ----------------------------------------------------------------
argf_t* argf_alloc(char* argv0, char** filenames, int num_filenames) {
	argf_t* pargf = malloc_or_die(sizeof(argf_t));
	pargf->argv0 = strdup_or_die(argv0);
	if (num_filenames == 0) {
		pargf->filenames = NULL;
		pargf->num_filenames = 0;
		pargf->fidx = 0;
		pargf->fp = stdin;
		pargf->pfgetter = stdin_fgetter;
	} else {
		pargf->filenames = malloc_or_die(num_filenames * sizeof(char*));
		for (int i = 0; i < num_filenames; i++)
			pargf->filenames[i] = strdup_or_die(filenames[i]);
		pargf->num_filenames = num_filenames;
		pargf->fidx = 0;
		pargf->fp = fopen(pargf->filenames[pargf->fidx], "r");
		if (pargf->fp == NULL) {
			perror("fopen");
			fprintf(stderr, "%s: could not open \"%s\" for read.\n",
				pargf->argv0, pargf->filenames[pargf->fidx]);
			pargf->pfgetter = err_fgetter;
		} else {
		pargf->pfgetter = files_fgetter;
		}
	}
	return pargf;
}

// ----------------------------------------------------------------
void argf_free(argf_t* pargf) {
	free(pargf->argv0);
	for (int i = 0; i < pargf->num_filenames; i++)
		free(pargf->filenames[i]);
	free(pargf->filenames);
	free(pargf);
}

// ----------------------------------------------------------------
// Returns NULL on EOF or first file-open error
char* argf_fgets(argf_t* pargf, char * restrict str, int size, int* perr) {
	return (pargf->pfgetter(pargf, str, size, perr));
}

// ----------------------------------------------------------------
static char* files_fgetter(argf_t* pargf, char * restrict str, int size, int* perr) {
	char* ptr = fgets(str, size, pargf->fp);
	if (ptr != NULL) {
		return ptr;
	}
	fclose(pargf->fp);
	pargf->fidx++;
	if (pargf->fidx >= pargf->num_filenames) {
		pargf->pfgetter = eof_fgetter;
		return NULL;
	}
	pargf->fp = fopen(pargf->filenames[pargf->fidx], "r");
	if (pargf->fp == NULL) {
		*perr = 1;
		perror("fopen");
		fprintf(stderr, "%s: could not open \"%s\" for read.\n",
			pargf->argv0, pargf->filenames[pargf->fidx]);
		pargf->pfgetter = eof_fgetter;
		return NULL;
	}

	return files_fgetter(pargf, str, size, perr);
}

static char* stdin_fgetter(argf_t* pargf, char * restrict str, int size, int* perr) {
	char* ptr = fgets(str, size, pargf->fp);
	if (ptr == NULL)
		pargf->pfgetter = eof_fgetter;
	return ptr;
}

static char* err_fgetter(argf_t* pargf, char * restrict str, int size, int* perr) {
	*perr = 1;
	return NULL;
}

static char* eof_fgetter(argf_t* pargf, char * restrict str, int size, int* perr) {
	return NULL;
}

// ----------------------------------------------------------------
static void* malloc_or_die(size_t size) {
	void* p = malloc(size);
	if (p == NULL) {
		fprintf(stderr, "malloc(%lu) failed.\n", (unsigned long)size);
		exit(1);
	}
	return p;
}

static char * strdup_or_die(const char *s1) {
	char* s2 = strdup(s1);
	if (s2 == NULL) {
		fprintf(stderr, "malloc/strdup failed\n");
		exit(1);
	}
	return s2;
}

// ================================================================
// This is a line-oriented cat.
#ifdef ARGF_TEST_MAIN
#define MYBUFSIZ 2048
static char line[MYBUFSIZ];
int main(int argc, char** argv) {
	argf_t* pargf = argf_alloc(argv[0], argv+1, argc-1);
	int error = 0;

	while (argf_fgets(pargf, line, MYBUFSIZ, &error) != NULL) {
		printf("%s", line);
	}
	argf_free(pargf);
	if (error) {
		return 1;
	}

	return 0;
}
#endif // ARGF_TEST_MAIN

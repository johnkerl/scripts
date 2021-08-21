// Similar to ARGF in Ruby, <> in Perl, etc.
// See at the end of argf.c for a usage example.

#ifndef ARGF_H
#define ARGF_H

#include <stdio.h>

// ----------------------------------------------------------------
struct _argf_t; // forward reference
typedef char* argf_fgetter_t(struct _argf_t* pargf, char * restrict str, int size, int* perr);

typedef struct _argf_t {
	char* argv0;
	char** filenames;
	int num_filenames;
	int fidx;
	FILE* fp;
	argf_fgetter_t* pfgetter;
} argf_t;

// ----------------------------------------------------------------
// The argv0 is for printing error messages.
argf_t* argf_alloc(char* argv0, char** filenames, int num_filenames);
void argf_free(argf_t* pargf);

// Returns NULL on EOF or first file-open error; sets *perr to 1 in the latter case.
char* argf_fgets(argf_t* pargf, char * restrict str, int size, int* perr);

#endif // ARGF_H

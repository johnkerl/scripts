#ifndef UTIL_H
#define UTIL_H

#define TRUE  1
#define FALSE 0

// ----------------------------------------------------------------
void* mlr_malloc_or_die(size_t size);

int mlr_string_hash_func(char *str);

// ----------------------------------------------------------------
static inline int mlr_canonical_mod(int a, int n) {
	int r = a % n;
	if (r >= 0)
		return r;
	else
		return r+n;
}

// '!strcmp(a,b)' computes signs; we don't need that -- only equality or inequality.
static inline int streq(char* a, char* b) {
	while (*a && *b) {
		if (*a != *b)
			return FALSE;
		a++;
		b++;
	}
	if (*a || *b)
		return FALSE;
	return TRUE;
}

// ----------------------------------------------------------------
#define MLR_INTERNAL_CODING_ERROR() mlr_internal_coding_error(__FILE__, __LINE__)
#define MLR_INTERNAL_CODING_ERROR_IF(v) mlr_internal_coding_error_if(v, __FILE__, __LINE__)
#define MLR_INTERNAL_CODING_ERROR_UNLESS(v) mlr_internal_coding_error_unless(v, __FILE__, __LINE__)
void mlr_internal_coding_error(char* file, int line);
void mlr_internal_coding_error_if(int v, char* file, int line);
void mlr_internal_coding_error_unless(int v, char* file, int line);

#endif // UTIL_H

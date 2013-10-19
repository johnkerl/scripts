#include "tokenize.h"

// ----------------------------------------------------------------
// Breaks a single character string into an array of tokens.
//
// The logic is straightforward:  A token is a sequence of non-whitespace
// characters.  A token is delimited by the beginning of the input string, a
// whitespace character, or the end of the string.

// Returns argc
int tokenize(
	char    * line,
	char   ** argv,
	int       max_arguments)
{
	char * readp;
	int    inside_token = 0;
	int    argc = 0;

	for (readp = line; *readp; readp++) {

		if ((*readp == ' ') || (*readp == '\t')) {
			if (inside_token) {
				inside_token = 0;
				*readp = 0;
			}
			//else, whitespace is not copied.
		}
		else { // Not whitespace
			if (!inside_token) { // Start of token
				inside_token = 1;
				if (argc >= max_arguments)
					break;
				argv[argc] = readp;
				argc++;
			}
			// else, continuation of token
		}
	}

	if (inside_token) { // End of input line terminates a token.
		*readp = 0;
		readp++;
	}
	return argc;
}

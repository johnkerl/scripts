// ================================================================
// tokenize.h
//
// Routines for splitting a command line into an argv-style array
// of tokens.  E.g. with the following input ('#' representing a
// null character):
//
//   +---------------------------------------------------------+
//   |The quick brown fox jumped over the lazy dogs.#          | <- command_line
//   +---------------------------------------------------------+
//
// the string will be modified after return to look like this:
//
//   +---------------------------------------------------------+
//   |The#quick#brown#fox#jumped#over#the#lazy#dogs.#          | <- command_line
//   +---------------------------------------------------------+
//    ^   ^     ^     ^   ^      ^    ^   ^    ^
//    |   |     |     |   |      |    |   |    |    argv[9] = NULL
//    |   |     |     |   |      |    |   |    argv[8]
//    |   |     |     |   |      |    |   argv[7]
//    |   |     |     |   |      |    argv[6]
//    |   |     |     |   |      argv[5]
//    |   |     |     |   argv[4]
//    |   |     |     argv[3]
//    |   |     argv[2]
//    |   argv[1]
//    argv[0]
//
// with argc set to 9.
//
// The input *WILL* be overwritten.  You may wish to copy the original
// using ut_strcpy().
//
// Having argv[argc] pointing to null is a historical convention which some
// programmers might expect.
// ================================================================

#ifndef TOKENIZE_H
#define TOKENIZE_H

#include "types.h"

int tokenize(
	char  * line,
	char ** argv,
	int     max_arguments);

#endif // TOKENIZE_H

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

static void usage() {
	fprintf(stderr, "Usage goes here\n");
	exit(1);
}
int main(int argc, char **argv) {
	int aflag = 0, boolv = 0, ch;

	while ((ch = getopt(argc, argv, "ab:h")) != -1) {
		switch (ch) {
		case 'a':
			aflag = 1;
			printf("got aflag=%d\n", aflag);
			break;
		case 'b':
			if (sscanf(optarg, "%d", &boolv) != 1)
				usage();
			printf("got boolv=%d\n", boolv);
			break;
		case 'h':
		case '?':
		default:
			usage();
		}
	}
	argc -= optind;
	argv += optind;
	printf("argc=%d\n", argc);
	for (int argi = 0; argi < argc; argi++)
		printf("argv[%d]=%s\n", argi, argv[argi]);


	return 0;
}

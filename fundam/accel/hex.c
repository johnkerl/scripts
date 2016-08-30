// ================================================================
// Copyright (c) 1998 John Kerl.
// ================================================================
// This is a simple hex dump with hex offsets to the left, hex data in the
// middle, and ASCII at the right.  This is a subset of the functionality of
// Unix od; I wrote it in my NT days.
//
// Example:
//
// $ d2h $(jot 0 128) | unhex | hex
// 00000000: 00 01 02 03  04 05 06 07  08 09 0a 0b  0c 0d 0e 0f |................|
// 00000010: 10 11 12 13  14 15 16 17  18 19 1a 1b  1c 1d 1e 1f |................|
// 00000020: 20 21 22 23  24 25 26 27  28 29 2a 2b  2c 2d 2e 2f | !"#$%&'()*+,-./|
// 00000030: 30 31 32 33  34 35 36 37  38 39 3a 3b  3c 3d 3e 3f |0123456789:;<=>?|
// 00000040: 40 41 42 43  44 45 46 47  48 49 4a 4b  4c 4d 4e 4f |@ABCDEFGHIJKLMNO|
// 00000050: 50 51 52 53  54 55 56 57  58 59 5a 5b  5c 5d 5e 5f |PQRSTUVWXYZ[\]^_|
// 00000060: 60 61 62 63  64 65 66 67  68 69 6a 6b  6c 6d 6e 6f |`abcdefghijklmno|
// 00000070: 70 71 72 73  74 75 76 77  78 79 7a 7b  7c 7d 7e 7f |pqrstuvwxyz{|}~.|
// ================================================================

// Build instructions: gcc -O3 -Wall hex.c -o hex

#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <fcntl.h>

#define LINE_LENGTH_MAX 8192

void hex_dump_fp(FILE *in_fp, FILE *out_fp, int do_raw);

//----------------------------------------------------------------------
int main(int argc, char **argv)
{
	char * filename;
	FILE * in_fp;
	FILE * out_fp;
	int do_raw = 0;
	int argi = 1;

	if (argc >= 2 && strcmp(argv[1], "-r") == 0) {
		do_raw = 1;
		argi++;
	}

	int num_file_names = argc - argi;

	if (num_file_names == 0) {
#ifdef WINDOWS
		setmode(fileno(stdin), O_BINARY);
#endif //WINDOWS
		hex_dump_fp(stdin, stdout, do_raw);
	} else {
		for ( ; argi < argc; argi++) {
			if (!do_raw) {
				if (num_file_names > 1)
					printf("%s:\n", argv[argi]);
			}
			filename = argv[argi];
			in_fp    = fopen(filename, "rb");
			out_fp   = stdout;
			if (in_fp == NULL) {
				fprintf(stderr, "Couldn't open \"%s\"; skipping.\n",
					filename);
			}
			else {
				hex_dump_fp(in_fp, out_fp, do_raw);
				fclose(in_fp);
				if (out_fp != stdout)
					fclose(out_fp);

			}
			if (!do_raw) {
				if (num_file_names > 1)
					printf("\n");
			}
		}
	}

	return 0;
}

//----------------------------------------------------------------------
#define bytes_per_clump  4
#define clumps_per_line  4
#define buffer_size     (bytes_per_clump * clumps_per_line)

void hex_dump_fp(FILE *in_fp, FILE *out_fp, int do_raw)
{
	unsigned char buf[buffer_size];
	long num_bytes_read;
	long num_bytes_total = 0;
	int byteno;

	while ((num_bytes_read=fread(buf, sizeof(unsigned char),
		buffer_size, in_fp)) > 0)
	{
		if (!do_raw) {
			printf("%08lx: ", num_bytes_total);
		}

		for (byteno = 0; byteno < num_bytes_read; byteno++) {
			unsigned int temp = buf[byteno];
			printf("%02x ", temp);
			if ((byteno % bytes_per_clump) ==
			(bytes_per_clump - 1))
			{
				if ((byteno > 0) && (byteno < buffer_size-1))
					printf(" ");
			}
		}
		for (byteno = num_bytes_read; byteno < buffer_size; byteno++) {
			printf("   ");
			if ((byteno % bytes_per_clump) ==
			(bytes_per_clump - 1))
			{
				if ((byteno > 0) && (byteno < buffer_size-1))
					printf(" ");
			}
		}

		if (!do_raw) {
			printf("|");
			for (byteno = 0; byteno < num_bytes_read; byteno++) {
				unsigned char temp = buf[byteno];
				if (!isprint(temp))
					temp = '.';
				printf("%c", temp);
			}

			printf("|");
		}

		printf("\n");
		num_bytes_total += num_bytes_read;
	}
}

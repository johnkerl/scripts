#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "tokenize.h"
#include "cmd.h"

#include "cmdfactor.h"
#include "cmdgcd.h"

#define PROMPT "sample> "

// ----------------------------------------------------------------
static void quit_hdlr(int cargc, char ** cargv, char * long_help,
	void * not_used)
{
	exit(0);
}

static cmd_info_t quit_info = {
	"quit",
	"Exit this program",
	"Usage: quit {quit args here}.",
	quit_hdlr
};

// ----------------------------------------------------------------
static void cls_hdlr(int cargc, char ** cargv, char * long_help,
	void * not_used)
{
	printf("\033[H\033[J");
}

static cmd_info_t cls_info = {
	"cls",
	"Clear the screen",
	"Usage: cls with no arguments.",
	cls_hdlr
};

// ----------------------------------------------------------------
static void help_hdlr(int cargc, char ** cargv, char * long_help,
	void * not_used);
extern cmd_info_t help_info;

// ================================================================
static cmd_info_t * pcmd_infos[] = {

	&factor_info,
	&gcd_info,

	&cls_info,
	&quit_info,
	&help_info,
	0
};

//// ----------------------------------------------------------------
//static void main_usage(char * prog_name)
//{
//	printf("Usage: %s mem  {nbytes}\n", prog_name);
//	printf("Or:    %s file {path on host} {nbytes}\n", prog_name);
//}

// ----------------------------------------------------------------
static void help_hdlr(int cargc, char ** cargv, char * long_help,
	void * not_used)
{
	int cargi;
	cmd_info_t * pcmd;

	if (cargc == 1) {
		cmd_show_names(pcmd_infos);
	}
	else {
		for (cargi = 1; cargi < cargc; cargi++) {
			pcmd = cmd_find(pcmd_infos, cargv[cargi]);
			if (pcmd) {
				printf("%s\n", pcmd->short_help);
				printf("%s\n", pcmd->long_help);
			}
			else {
				printf("Couldn't find command \"%s\".\n",
					cargv[cargi]);
			}
			printf("\n");
		}
	}
}

static cmd_info_t help_info = {
	"help",
	"Provide on-line help",
	"Usage: help {help args here}.",
	help_hdlr
};

// ----------------------------------------------------------------
#define MAX_CARGC 16
int main(int argc, char ** argv)
{
	int    cargc;
	char * cargv[MAX_CARGC];
	char   line[256];
	cmd_info_t * pcmd;

	//if (!init_hdlr(argc, argv)) {
		//main_usage(argv[0]);
		//exit(1);
	//}

	printf(PROMPT);
	fflush(stdout);
	while (fgets(line, sizeof(line), stdin)) {
		int len = strlen(line);
		if (line[len-1] == '\n')
			line[len-1] = 0;

		cargc = tokenize(line, cargv, MAX_CARGC);

		if (cargc == 0) {
			printf(PROMPT);
			fflush(stdout);
			continue;
		}

		pcmd = cmd_find(pcmd_infos, cargv[0]);
		if (pcmd) {
			pcmd->phdlr_func(cargc, cargv, pcmd->long_help, 0);
		}
		else {
			printf("Couldn't find command \"%s\".\n",
				cargv[0]);
		}

		printf(PROMPT);
		fflush(stdout);
	}
	return 0;
}

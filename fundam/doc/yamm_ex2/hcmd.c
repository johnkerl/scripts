#include <stdio.h>
#include <string.h>
#include "hcmd.h"

static int cmd_find_max_len(
	cmd_info_t * pcmd_infos[]);

static int ut_strncmp(
	char   * p1,
	char   * p2,
	unsigned num_bytes);

// ----------------------------------------------------------------
void cmd_run(
	cmd_info_t * pcmd_infos[],
	int          cargc,
	char      ** cargv,
	void       * parg)
{
	cmd_info_t * pcmd;

	pcmd = cmd_find(pcmd_infos, cargv[0]);
	if (pcmd)
		pcmd->phdlr_func(cargc, cargv, pcmd->long_help, parg);
	else
		printf("Couldn't find command \"%s\".\n", cargv[0]);
}

// ----------------------------------------------------------------
cmd_info_t * cmd_find(
	cmd_info_t * pcmd_infos[],
	char       * cmd_name)
{
	int i;
	int input_len;
	int max_len;
	int cmp_len;
	int num_found;
	cmd_info_t * pcmd = 0;

	max_len = cmd_find_max_len(pcmd_infos);
	input_len = strlen(cmd_name);

	for (cmp_len = 1; cmp_len <= max_len; cmp_len++) {

		num_found = 0;
		for (i = 0; pcmd_infos[i]; i++) {
			if (strcmp(pcmd_infos[i]->cmd_name, cmd_name) == 0) {
				return pcmd_infos[i];
			}

			if (ut_strncmp(pcmd_infos[i]->cmd_name, cmd_name,
			cmp_len) == 0)
			{
				pcmd = pcmd_infos[i];
				num_found++;
			}
		}

		if (num_found == 0) {
			break;
		}
		else if (num_found == 1) {
			if (input_len > (int)strlen(pcmd->cmd_name))
				break;
			else if (ut_strncmp(cmd_name, pcmd->cmd_name,
			input_len) != 0)
				break;
			else
				return pcmd;
		}
		else if (cmp_len >= input_len) {
			printf("%d commands match \"%s\".\n",
				num_found, cmd_name);
			return 0;
		}
	}
	printf("\n");
	printf("Couldn't find command \"%s\".\n",
		cmd_name);
	return 0;
}

// ----------------------------------------------------------------
void cmd_show_names(
	cmd_info_t * pcmd_infos[]) // Must be null-terminated.
{
	int i;
	for (i = 0; pcmd_infos[i]; i++)
		printf("  %s\n", pcmd_infos[i]->cmd_name);
}

// ----------------------------------------------------------------
void cmd_show_summaries(
	cmd_info_t * pcmd_infos[]) // Must be null-terminated.
{
	int i;
	int max_len = cmd_find_max_len(pcmd_infos);

	for (i = 0; pcmd_infos[i]; i++)
		printf("%*s: %s\n",
			max_len,
			pcmd_infos[i]->cmd_name,
			pcmd_infos[i]->short_help);
}

// ----------------------------------------------------------------
static int cmd_find_max_len(
	cmd_info_t * pcmd_infos[])
{
	int max_len = 0;
	int i;

	for (i = 0; pcmd_infos[i]; i++) {
		int cur_len = strlen(pcmd_infos[i]->cmd_name);
		if (cur_len > max_len)
			max_len = cur_len;
	}
	return max_len;
}

// ----------------------------------------------------------------
static int ut_strncmp(
	char   * p1,
	char   * p2,
	unsigned num_bytes)
{
	char c1;
	char c2;
	unsigned i;

	for (i =0; i < num_bytes; i++) {
		c1 = *p1;
		c2 = *p2;

		if ((c1 == 0) && (c2 == 0))
			return 0;
		else if (c1 == 0)
			return -1;
		else if (c2 == 0)
			return 1;
		else if (c1 < c2)
			return -1;
		else if (c1 > c2)
			return 1;
		else {
			p1++;
			p2++;
		}
	}

	return 0;
}

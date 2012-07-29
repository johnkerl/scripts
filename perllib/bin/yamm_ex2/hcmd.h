#ifndef CMD_H
#define CMD_H

typedef void cmd_hdlr_func_t(
	int     cargc,
	char ** cargv,
	char  * long_help,
	void  * parg);

typedef struct _cmd_info_t
{
    char * cmd_name;
    char * short_help;
    char * long_help;
    cmd_hdlr_func_t  * phdlr_func;
} cmd_info_t;

cmd_info_t * cmd_find(
	cmd_info_t * pcmd_infos[], // Must be null-terminated.
	char       * cmd_name);

void cmd_run(
	cmd_info_t * pcmd_infos[], // Must be null-terminated.
	int          cargc,
	char **      cargv,
	void  *      parg);

void cmd_show_names(
	cmd_info_t * pcmd_infos[]); // Must be null-terminated.

void cmd_show_summaries(
	cmd_info_t * pcmd_infos[]); // Must be null-terminated.

#endif // CMD_H

#!/usr/bin/python -Wall

# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

import ispec_tm
import ispec_tbl
import re
import sys

# I have a *global* for ispec.tbl. This makes it non re-entrant.
# In particular I won't be able to form, say, the direct product of two
# different user-specified groups without a redesign.

def get_elements_str(params_string):
	file_name = params_string
	matrix = []

	if (file_name == "-"):
		file_handle = sys.stdin
	else:
		try:
			file_handle = open(file_name, 'r')
		except:
			print "Couldn't open \"" + file_name + "\" for read."
			sys.exit(1)

	lno = 0
	for line in file_handle:
		lno += 1

		# Chomp trailing newline, if any.
		if (line[-1] == '\n'):
			line = line[0:-1]

		# Strip leading and trailing whitespace.
		line = re.sub(r"^\s+", r"", line)
		line = re.sub(r"\s+$", r"", line)

		code_strings = re.split('\s+', line)
		row = []
		colno = 0
		for cs in code_strings:
			colno += 1
			try:
				row.append(int(cs))
			except:
				print "Scan error on \"%s\", column %d, line %d, file %s" % (cs,colno,lno,file_name)
				sys.exit(1)
		matrix.append(row)
	if (file_name != "-"):
		file_handle.close()

	ispec_tm.install_table(matrix)

	n=len(matrix)
	elts = range(0, n)
	for i in range(0, n):
		elts[i] = ispec_tm.ispec_t(i)
	return elts

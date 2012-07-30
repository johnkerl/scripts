#!/usr/bin/python -Wall

# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

import spec_tm
import spec_tables
import re
import copy
import sys

# I have globals for the spec tables. This makes it non re-entrant.
# In particular I won't be able to form, say, the direct product of two
# different user-specified groups without a redesign.

def get_elements_str(params_string):
	file_name = params_string
	cayley_table_with_names = []

	if (file_name == "-"):
		file_handle = sys.stdin
	else:
		try:
			file_handle = open(file_name, 'r')
		except:
			print "Couldn't open \"" + file_name + "\" for read."
			sys.exit(1)

	for line in file_handle:

		# Chomp trailing newline, if any.
		if (line[-1] == '\n'):
			line = line[0:-1]

		# Strip leading and trailing whitespace.
		line = re.sub(r"^\s+", r"", line)
		line = re.sub(r"\s+$", r"", line)

		row_names = re.split('\s+', line)
		cayley_table_with_names.append(copy.copy(row_names))

	if (file_name != "-"):
		file_handle.close()

	spec_tm.install_table(cayley_table_with_names)

	n = len(cayley_table_with_names)
	elts = range(0, n)
	for i in range(0, n):
		elts[i] = spec_tm.spec_t(i)
	return elts

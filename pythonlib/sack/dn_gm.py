#!/usr/bin/python -Wall

# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

import dih_tm

def get_elements_str(params_string):
	n = dih_tm.params_from_string(params_string)
	elts = []
	for i in range(0, n):
		for j in range(0, 2):
			elt = dih_tm.dih_t(i, j, n)
			elts.append(elt)
	return elts

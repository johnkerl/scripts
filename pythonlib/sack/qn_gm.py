#!/usr/bin/python -Wall

# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

import genquat_tm

def get_elements_str(params_string):
	n = genquat_tm.params_from_string(params_string)
	fourn = n + n + n + n
	elts = range(0, fourn)
	k = 0
	for i in range(0, n):
		for j in range(0, 4):
			elts[k] = genquat_tm.genquat_t(i, j, n)
			k += 1
	return elts

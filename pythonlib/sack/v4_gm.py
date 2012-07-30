#!/usr/bin/python -Wall

# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

import v4_tm

def get_elements_str(params_string):
	not_used = v4_tm.params_from_string(params_string)
	elts = range(0, 4)
	for i in range(0, 4):
		elts[i] = v4_tm.v4_t(i)
	return elts

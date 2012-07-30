#!/usr/bin/python -Wall

# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

import pmti_tm
import sackint

def get_elements(n):
	sn_size = sackint.factorial(n)
	elts = []
	for k in range(0, sn_size):
		elt = pmti_tm.kth_pmti(k, n, sn_size)
		if (elt.parity() == 0):
			elts.append(elt)
	pmti_tm.sort_pmtis(elts)
	return elts

def get_elements_str(params_string):
	n = pmti_tm.params_from_string(params_string)
	return get_elements(n)

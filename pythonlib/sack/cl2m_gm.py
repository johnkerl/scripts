#!/usr/bin/python -Wall

# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

import cl2m_tm

def get_elements_str(params_string):
	n = cl2m_tm.params_from_string(params_string)
	two_n = 1 << n
	elts = []
	#for bits in range(0, two_n):
		#for sign in [1, -1]:
	for sign in [1, -1]:
		for bits in range(0, two_n):
			elts.append(cl2m_tm.cl2m_t(sign, bits, n))
	return elts

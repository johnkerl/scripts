#!/usr/bin/python -Wall

# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

import modadd_tm

def get_elements_str_aux(mod_array):
	group_size = 1
	for m in mod_array:
		group_size *= m
	elts = []
	k = 0
	n = len(mod_array)
	for i in range(0, group_size):
		elt = []
		a = k
		for j in range(0, n):
			elt.append(a % mod_array[j])
			a /= mod_array[j]
		elts.append(modadd_tm.modadd_t(elt, mod_array))
		k += 1
	return elts

def get_elements_str(params_string):
	mod_array = modadd_tm.params_from_string(params_string)
	return get_elements_str_aux(mod_array)


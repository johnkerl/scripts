#!/usr/bin/python -Wall

# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

import modmul_tm
import modadd_gm
import sackint

# ----------------------------------------------------------------
# Example:
# Mods = 4,5
# Phis = 2, 4
# Multiplicative groups = {1, 3} {1, 2, 3, 4}
# Desired elements:  1,1 1,2 1,3 1,4 3,1 3,2 3,3 3,4
# First compute indices into the multiplicative groups:
#   0,0 0,1 0,2 0,3 1,0 1,1 1,2 1,3
# Then, for each position, convert indices into group elements:
#
#   k = 0:
#   0,0 -> 1,0
#   0,1 -> 1,1
#   0,2 -> 1,2
#   0,3 -> 1,3
#   1,0 -> 3,0
#   1,1 -> 3,1
#   1,2 -> 3,2
#   1,3 -> 3,3
#
#   k = 1:
#   0,0 -> 1,1
#   0,1 -> 1,2
#   0,2 -> 1,3
#   0,3 -> 1,4
#   1,0 -> 3,1
#   1,1 -> 3,2
#   1,2 -> 3,3
#   1,3 -> 3,4

def get_elements_str(params_string):
	mod_array = modmul_tm.params_from_string(params_string)
	num_moduli = len(mod_array)

	phi_array = []
	group_size = 1
	for m in mod_array:
		phi = sackint.eulerphi(m)
		phi_array.append(phi)
		group_size *= phi

	indices = modadd_gm.get_elements_str_aux(phi_array)

	phi_groups = []
	for m in mod_array:
		phi_group = []
		for k in range (0, m):
			if (sackint.gcd(k, m) == 1):
				phi_group.append(k)
		phi_groups.append(phi_group)

	elts = []
	for index in indices:
		resarray = []
		for i in range(0, len(index.residues)):
			j = index.residues[i]
			resarray.append(phi_groups[i][j])
		elt = modmul_tm.modmul_t(resarray, mod_array)
		elts.append(elt)
	return elts

#!/usr/bin/python -Wall

# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

import pauli_tm
import sackgrp

def get_elements_str(params_string):
	elts = []
	elts.append(pauli_tm.from_string("sx",""))
	elts.append(pauli_tm.from_string("sy",""))
	elts.append(pauli_tm.from_string("sz",""))
	sackgrp.close_group(elts)
	return elts

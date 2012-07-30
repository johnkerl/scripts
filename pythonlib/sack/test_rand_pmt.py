#!/usr/bin/python -Wall

# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

import pmtc_tm
import pmti_tm
import copy

#count=80000
count=10000
N=100
#N=6
for i in range(0, count):
	pi = pmtc_tm.rand_pmtc(N)
	ct = pi.cycle_type()
	print ct
	#print pi

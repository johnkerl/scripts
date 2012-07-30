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

# ----------------------------------------------------------------
s = pmtc_tm.from_cycles([[1,2,3],[4,5]], 6)
print s
s = pmtc_tm.from_cycle([1,2,3], 6)
print s

s = pmti_tm.from_cycles([[1,2,3],[4,5]], 6)
print s
s = pmti_tm.from_cycle([1,2,3], 6)
print s

# ----------------------------------------------------------------
s = pmtc_tm.from_cycle([1,2,3], 6); ct = s.cycle_type(); print s, ct
s = pmtc_tm.from_cycles([[1,2,3],[4,5]], 6); ct = s.cycle_type(); print s, ct
s = pmtc_tm.from_cycles([[1,2],[3],[4,5]], 6); ct = s.cycle_type(); print s, ct
print

print "random pmtcs:"
for i in range(0, 10):
	pi = pmtc_tm.rand_pmtc(4)
	print pi
print

print "random pmtis:"
for i in range(0, 10):
	pi = pmti_tm.rand_pmti(4)
	print pi
print


print "random pmtcs:"
for i in range(0, 10):
	pi = pmtc_tm.rand_pmtc(20)
	ct = pi.cycle_type()
	print pi, ct
print

print "random pmtis:"
for i in range(0, 10):
	pi = pmti_tm.rand_pmti(20)
	ct = pi.cycle_type()
	print pi, ct
print

print "random pmtcs:"
for i in range(0, 10):
	pi = pmtc_tm.rand_pmtc(100)
	ct = pi.cycle_type()
	print ct
print

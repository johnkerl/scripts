#!/usr/bin/python -Wall

# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

import pmtc_tm
import snc_gm
import cgpalg_tm
import copy

# ----------------------------------------------------------------
# 559B final problem 1a.

print "-" * 64

#S3  = snc_gm.get_elements(3)

s1  = pmtc_tm.from_cycle([1],   3)
s12 = pmtc_tm.from_cycle([1,2], 3)
s13 = pmtc_tm.from_cycle([1,3], 3)
s23 = pmtc_tm.from_cycle([2,3], 3)
s123 = pmtc_tm.from_cycle([1,2,3], 3)
s132 = pmtc_tm.from_cycle([1,3,2], 3)
S3  = [s1, s12, s13, s23, s123, s132]

s1  = pmtc_tm.from_cycle([1],   3)
s12 = pmtc_tm.from_cycle([1,2], 3)
s13 = pmtc_tm.from_cycle([1,3], 3)

P = cgpalg_tm.cgpalg_t([[1,s1], [ 1,s12]])
Q = cgpalg_tm.cgpalg_t([[1,s1], [-1,s13]])
E = P*Q

print "S3:"
for g in S3:
	print g
print ""

print "P:", P
print "Q:", Q
print "E:", E
print "E*E", E*E
print

#print "AEs:"
#for g in S3:
#	A = cgpalg_tm.cgpalg_t([[1, g]])
#	AE = A * E
#	print AE
#print

print "AEs:"
for g in S3:
	A = cgpalg_tm.cgpalg_t([[1, g]])
	AE = A * E
	#print g, "--", AE.to_coef_array(S3)
	print AE.to_coef_array(S3)
print
# Got rank 2

print "AE invs:"
for g in S3:
	A = cgpalg_tm.cgpalg_t([[1, g]])
	AE = A * E
	#print g, "--", AE.to_coef_array(S3)
	print AE.inv()
print
# Got rank 2

print "AE inv checks:"
for g in S3:
	A = cgpalg_tm.cgpalg_t([[1, g]])
	AE = A * E
	#print g, "--", AE.to_coef_array(S3)
	print AE.inv() * AE
print
# Got rank 2

# ----------------------------------------------------------------
# 559B final problem 1b.

print "-" * 64

S4   = snc_gm.get_elements(4)

s1   = pmtc_tm.from_cycle([1],     4)
s12  = pmtc_tm.from_cycle([1,2],   4)

s13  = pmtc_tm.from_cycle([1,3],   4)
s14  = pmtc_tm.from_cycle([1,4],   4)
s34  = pmtc_tm.from_cycle([3,4],   4)
s134 = pmtc_tm.from_cycle([1,3,4], 4)
s143 = pmtc_tm.from_cycle([1,4,3], 4)

P = cgpalg_tm.from_pmtns([s1, s12])
Q = cgpalg_tm.from_pmtns_with_parity([s1, s13, s14, s34, s134, s143])
E = P*Q
print "P:", P
print "Q:", Q
print "E:", E
print "E*E", E*E
print

print "AEs:"
for g in S4:
	A = cgpalg_tm.cgpalg_t([[1, g]])
	AE = A * E
	print AE.to_coef_array(S4)
print
# Got rank 3


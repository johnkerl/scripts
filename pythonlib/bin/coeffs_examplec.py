#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2008-02-05
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
import sackmatc_m
from math import *

# ----------------------------------------------------------------
basis = [[1, -1], [1j, 2j]]
v = [3, 4j]
c = sackmatc_m.basis_coeffs(v, basis)
print "v = ", v
print "c = ", c
w = sackmatc_m.linear_combination(c, basis)
print "w = ", w
print

# ----------------------------------------------------------------
s = 1.0/sqrt(2.0)
basis = [[s, s], [s*1j, -s*1j]]
n = len(basis)
dots = sackmatc_m.make_zero_matrix(n, n)
for i in range(0, n):
	ui = basis[i]
	for j in range(0, n):
		uj = basis[j]
		uiuj = sackmatc_m.vecdot(ui, uj)
		dots[i][j] = uiuj
print dots
print
v = [3, 4j]
c = sackmatc_m.basis_coeffs_on(v, basis)
print "v = ", v
print "c = ", c
w = sackmatc_m.linear_combination(c, basis)
print "w = ", w


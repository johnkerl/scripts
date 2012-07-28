#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2008-02-05
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
import sackmat_m
from math import *

# ----------------------------------------------------------------
basis = [[1, -1], [1, 2]]
v = [3, 4]
c = sackmat_m.basis_coeffs(v, basis)
print "v = ", v
print "c = ", c
w = sackmat_m.linear_combination(c, basis)
print "w = ", w
print

# ----------------------------------------------------------------
s = 1.0/sqrt(2.0)
basis = [[s, s], [s, -s]]
n = len(basis)
for i in range(0, n):
	ui = basis[i]
	for j in range(0, n):
		uj = basis[j]
		uiuj = sackmat_m.vecdot(ui, uj)
		print " <u[%d],u[%d]>=%11.7f" % (i, j, uiuj),
	print
print
v = [3, 4]
c = sackmat_m.basis_coeffs_on(v, basis)
print "v = ", v
print "c = ", c
w = sackmat_m.linear_combination(c, basis)
print "w = ", w


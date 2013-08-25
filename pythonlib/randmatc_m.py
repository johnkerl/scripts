#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2008-02-06
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
import sys
import randc_m # For random complex scalars
import math
from sackmatc_m import *

# ----------------------------------------------------------------
def randmatc(m, n):
	A = make_zero_matrix(m, n)
	for i in range(0, m):
		for j in range(0, n):
			A[i][j] = randc_m.randc_mean_sq_1()
	return A

# ----------------------------------------------------------------
def randsqmatc(n):
	return randmatc(n, n)

# ----------------------------------------------------------------
def randgue(n):
	A = make_zero_matrix(n, n)
	for i in range(0, n):
		for j in range(i, n):
			A[i][j] = randc_m.randc_mean_sq_1()
	for i in range(0, n):
		for j in range(0, i):
			A[i][j] = conj(A[j][i])
	return A

# ----------------------------------------------------------------
def randxxt(n):
	A = randmatc(n, n)
	return A.transpose() * A


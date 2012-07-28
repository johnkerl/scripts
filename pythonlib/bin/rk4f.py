#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2008-02-08
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
import sys
from math import *
import copy
from sackmat_m import *

# ----------------------------------------------------------------
# Wikipedia:
#
# Approximation to
#   dy/dt = f(t,y) with y(t_0) = y_0.
# is
#   y_{n+1} = y_n + h/6(k1 + 2 k2 + 2 k3 + k4)
#   t_{n+1} = t_n + h
# where
#   k1 = f(t_n,       y_n)
#   k2 = f(t_n + h/2, y_n + k1 h/2)
#   k3 = f(t_n + h/2, y_n + k2 h/2)
#   k4 = f(t_n + h,   y_n + k3 h)

# ----------------------------------------------------------------
# y'' = -k y
#
# Let z = y'.  Then
# y' = z
# z' = -k y
#
# State vector is [y, z]

def f(t, yvec):
	return [yvec[1], -k * yvec[0]]

# ----------------------------------------------------------------
def vecsadd(u, v, s):
	n = len(u)
	rv = [0] * n
	for i in xrange(0, n):
		rv[i] = u[i] + v[i] * s
	return rv

# ----------------------------------------------------------------
def rksum(y, k1, k2, k3, k4, s):
	n = len(k1)
	for i in xrange(0, n):
		y[i] += s * (k1[i] + 2*k2[i] + 2*k3[i] + k4[i])

# ----------------------------------------------------------------
k  = 2.00
h  = 0.001
t0 = 0.0

if len(sys.argv) == 2:
	k = float(sys.argv[1])

y0 = [1.0, 0.0]

niter = 8000

y = y0
t = t0

for iter in range(0, niter):
	print "%11.7f %11.7f %11.7f" % (t, y[0], y[1])

	# k1 = f(t, y)
	# k2 = f(t+h/2, y + k1 * h/2)
	# k3 = f(t+h/2, y + k2 * h/2)
	# k4 = f(t+h,   y + k3 * h)
	# y += h/6 * (k1 + 2*k2 + 2*k3 + k4)

	k1 = f(t, y)
	k2 = f(t+h/2, vecsadd(y, k1, h/2))
	k3 = f(t+h/2, vecsadd(y, k2, h/2))
	k4 = f(t+h,   vecsadd(y, k3, h))
	rksum(y, k1, k2, k3, k4, h/6)

	t += h

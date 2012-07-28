#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2008-02-08
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
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
def f(t, yvec):
	return a * yvec[0]

# ----------------------------------------------------------------
a  = -0.04
h  = 0.001
t0 = 0.0

y0 = 1.0

niter = 80

y = y0
t = t0

for iter in range(0, niter):

	print "%11.7f %11.7f" % (t, y)

	k1 = f(t, [y])
	k2 = f(t+h/2, [y + k1 * h/2])
	k3 = f(t+h/2, [y + k2 * h/2])
	k4 = f(t+h,   [y + k3 * h])
	y += h/6 * (k1 + 2*k2 + 2*k3 + k4)

	t += h

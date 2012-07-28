#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2008-02-08
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
from math import *

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
# Euler:
# Approximation to
#   dy/dt = f(t,y) with y(t_0) = y_0.
# is
#   y_{n+1} += h * f(t_n, y_n)
#   t_{n+1} = t_n + h



# ----------------------------------------------------------------
# 1st attempt:
#   dy/dt = -at
# so
#   f(t,y) = -at
# ----------------------------------------------------------------

# ----------------------------------------------------------------
def f(t,y):
	return a*y
	#return a*t

# ----------------------------------------------------------------
a  = -0.4
h  = 0.001
t0 = 0.0

y0 = 1.0
#y0 = 0.0

niter = 80

eulery = y0
rk4y   = y0
t      = t0

for iter in range(0, niter):

	exacty = exp(a*t)
	#exacty = a*t**2 / 2
	print "%11.7f  %11.7f %11.7f %11.7f %10.3e %10.3e" % \
		(t, eulery, rk4y, exacty, eulery-exacty, rk4y-exacty)

	eulery += h * f(t, eulery)

	k1 = f(t,     rk4y)
	k2 = f(t+h/2, rk4y + k1 * h/2)
	k3 = f(t+h/2, rk4y + k2 * h/2)
	k4 = f(t+h,   rk4y + k3 * h)
	rk4y += h/6 * (k1 + 2*k2 + 2*k3 + k4)

	t += h

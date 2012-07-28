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
# Euler:
# Approximation to
#   dy/dt = f(t,y) with y(t_0) = y_0.
# is
#   y_{n+1} += h * f(t_n, y_n)
#   t_{n+1} = t_n + h



# ----------------------------------------------------------------
# 2nd attempt:
#   x'' + a^2 x = 0
# Converting to a system of 1st-order ODEs:
#   y1 = x
#   y2 = x'
# Then
#   y1' =      y2
#   y2' = -a^2 y1.
#
# Exact solution:
#
#   x  =    C cos(at) +   D sin(at)
#   x' = -a C sin(at) + a D cos(at)
#
#   x (0) =   C
#   x'(0) = a D
#
#   C = x (0) = C
#   D = x'(0) / a
#
#   x  =   x(0) cos(at) +  x'(0) sin(at) / a
#
# ----------------------------------------------------------------

# ----------------------------------------------------------------
def f(t, y):
	return [y[1], -a**2 * y[0]]

# ----------------------------------------------------------------
a  = 40
h  = 0.001
t0 = 0.0

y0 = [1.0, 0.0]

niter = 800

eulery = copy.copy(y0)
rk4y   = copy.copy(y0)
t      = t0

for iter in range(0, niter):

	exacty = [y0[0] * cos(a*t), y0[1] * sin(a*t) / a]

	print "%11.7f  %11.7f %11.7f %11.7f %10.3e %10.3e" % \
		(t, eulery[0], rk4y[0], exacty[0], eulery[0]-exacty[0], rk4y[0]-exacty[0])

	eulery = vecadd(eulery, vecsmul(f(t, eulery),h))

	k1 = f(t,     rk4y)
	k2 = f(t+h/2, vecadd(rk4y, vecsmul(k1, h/2)))
	k3 = f(t+h/2, vecadd(rk4y, vecsmul(k2, h/2)))
	k4 = f(t+h,   vecadd(rk4y, vecsmul(k3, h)))

	rk4y[0] += h/6 * (k1[0] + 2*k2[0] + 2*k3[0] + k4[0])
	rk4y[1] += h/6 * (k1[1] + 2*k2[1] + 2*k3[1] + k4[1])

	t += h

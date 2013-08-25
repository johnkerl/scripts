#!/usr/bin/python -Wall

# ================================================================
# Copyright (c) John Kerl 2007
# kerl.john.r@gmail.com
# ================================================================

# theta'' = k sin(theta) + b theta'
# k < 0, b < 0

# Two-variable system:
# u  = theta
# v  = theta'
#
# u' = v
# v' = k sin(u) + b v

# Euler (1st-order) approximation:
# u(k+1) = u(k) + u'(k) dt
# v(k+1) = v(k) + v'(k) dt

from __future__ import division # 1/2 = 0.5, not 0.
from math import *

nt = 10000
dt = 0.004

k = -10.00 # Pendulum constant
b =  -0.09 # Damping

t =  0.0 # Initial time
u =  0.0 # Initial angle, in radians
# 10 to wrap around a bit before damping; 1 to not wrap.
v =  10.1 # Initial velocity

for i in range(0, nt):
	nextu = u + dt * v
	nextv = v + dt * (k * sin(u) + b * v)

	u = nextu
	v = nextv

	# theta as a function of t:
	#print "%11.9f %11.9f" % (t, u)

	# phase portrait:
	print "%11.9f %11.9f" % (u, v)

	t += dt

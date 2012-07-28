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
# 4th attempt:
#   i hbar dpsi/dt = -hbar^2 / 2m Dpsi + V psi
#   i dpsi/dt = -hbar / 2m Dpsi + V/hbar psi
#   dpsi/dt = i (hbar / 2m Dpsi - V/hbar psi)
#   dpsi/dt = f(psi)  -- run RK4's at each x.

#   y += y + dt/6(k1 + 2 k2 + 2 k3 + k4)
#   t += t + dt
# where
#   k1 = f(psi)
#   k2 = f(psi + k1 h/2)
#   k3 = f(psi + k2 h/2)
#   k4 = f(psi + k3 h)

#   k1 = i (hbar / 2m D(psi)          - V/hbar (psi))
#   k2 = i (hbar / 2m D(psi + k1*h/2) - V/hbar (psi + k1*h/2))
#   k3 = i (hbar / 2m D(psi + k2*h/2) - V/hbar (psi + k2*h/2))
#   k4 = i (hbar / 2m D(psi + k3*h)   - V/hbar (psi + k3*h))

# hbar = 1; mass --> c
#   k1 = i (c D(psi)          - V (psi))
#   k2 = i (c D(psi + k1*h/2) - V (psi + k1*h/2))
#   k3 = i (c D(psi + k2*h/2) - V (psi + k2*h/2))
#   k4 = i (c D(psi + k3*h)   - V (psi + k3*h))

# ----------------------------------------------------------------
def f(t,y):
	return a*y

# ----------------------------------------------------------------
a  = -0.4
h  = 0.001
t0 = 0.0

y0 = 1.0

niter = 80

eulery = y0
rk4y   = y0
t      = t0

for iter in range(0, niter):

	print "%11.7f %11.7f %11.7f" % (t, eulery, rk4y)

	# Euler SE:
	#for k in range(0, N):
	#	psi[k] += 1j * dt * (Dpsi[k] - V[k]*psi[k])

	# sackvec class?  sackmat?

	# hbar = 1; mass --> c
	#   k1 = 1j * (c * disclap(psi)          - V * (psi))
	#   k2 = 1j * (c * disclap(psi + k1*h/2) - V * (psi + k1*h/2))
	#   k3 = 1j * (c * disclap(psi + k2*h/2) - V * (psi + k2*h/2))
	#   k4 = 1j * (c * disclap(psi + k3*h)   - V * (psi + k3*h))

	#   psi += psi + dt/6(k1 + 2 k2 + 2 k3 + k4)
	#   t += t + dt



	# Do this in Matlab?!?

	# Euler SE:
	# psi = psi + i * dt * (del2(psi) - V.*psi)

	# RK4 SE:
	# k1 = i * (c * del2(psi)          - V *  psi)
	# k2 = i * (c * del2(psi + k1*h/2) - V * (psi + k1*h/2))
	# k3 = i * (c * del2(psi + k2*h/2) - V * (psi + k2*h/2))
	# k4 = i * (c * del2(psi + k3*h)   - V * (psi + k3*h))
	# psi += psi + dt/6(k1 + 2 k2 + 2 k3 + k4)
	# t = t + dt




	eulery += h * f(t, eulery)

	k1 = f(t,     rk4y)
	k2 = f(t+h/2, rk4y + k1 * h/2)
	k3 = f(t+h/2, rk4y + k2 * h/2)
	k4 = f(t+h,   rk4y + k3 * h)
	rk4y += h/6 * (k1 + 2*k2 + 2*k3 + k4)

	t += h

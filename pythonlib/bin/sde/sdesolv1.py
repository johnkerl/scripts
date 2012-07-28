#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2008-02-22
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
import math, random

# ----------------------------------------------------------------
# Writes the motion into the Xt array, which must be predimensioned.

# Xt is dimensioned [nt][dim]?
# or have:
# Xt is dimensioned [dim][nt]?

# dXt = e(X_t, t) dt + f(Xt, t) db_t

def sdesolve1(Xt, e, f, params, dt):
	nt     = len(Xt)
	dim    = len(Xt[0])
	sqrtdt = math.sqrt(dt)
	T      = nt * dt
	t      = 0.0
	Bt     = 0.0

	Xt[0] = X0
	for i in xrange(1, dim):
		for j in xrange(1, nt):
			dB = random.gauss(0.0, sqrtdt)
			Xt[i][j] = Xt[i][j-1] + e(Xt, t) * dt + f(Xt, t) * dB
			t  += dt

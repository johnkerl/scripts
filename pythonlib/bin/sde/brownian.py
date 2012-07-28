#!/usr/bin/python -Wall

# ================================================================
# Routines for generating discrete-time approximations to Brownian motions
# and Brownian bridges.
#
# John Kerl
# kerl.john.r@gmail.com
# 2008-02-20
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
import math, random

# ----------------------------------------------------------------
# Returns the time series [0, dt, 2*dt, ..., (nt-1)*dt].

def get_t_series(nt, dt):
	ts = [0.0] * nt
	ts[0] = 0.0
	for k in xrange(1, nt):
		ts[k] = ts[k-1] + dt
	return ts

# ----------------------------------------------------------------
# Writes the motion into the Bt array, which must be predimensioned.

def get_BM_series(Bt, dt):
	nt = len(Bt)
	sqrtdt = math.sqrt(dt)
	Bt[0] = 0.0
	for k in xrange(1, nt):
		Bt[k] = Bt[k-1] + random.gauss(0.0, sqrtdt)

def get_SRW_series(St, dt):
	nt = len(St)
	sqrtdt = math.sqrt(dt)
	choices = [sqrtdt, -sqrtdt]
	St[0] = 0.0
	for k in xrange(1, nt):
		St[k] = St[k-1] + random.choice(choices)

# ----------------------------------------------------------------
# Writes the motion into the Xt array, which must be predimensioned.  The Bt
# array must be an already-computed Brownian motion of the same length.

def get_BB_series_from_BM(Xt, Bt, X0, XT, dt):
	nt     = len(Bt)
	BT     = Bt[-1]
	T      = nt * dt
	height = XT - X0 - BT
	t      = 0.0
	for k in xrange(0, nt):
		Xt[k] = X0 + Bt[k] + t/T * height
		t += dt

# ----------------------------------------------------------------
# Writes the motion into the Xt array, which must be predimensioned.

def get_BB_series_from_SDE(Xt, X0, XT, dt):
	nt     = len(Xt)
	sqrtdt = math.sqrt(dt)
	T      = nt * dt
	t      = 0.0
	Bt     = 0.0

	Xt[0] = X0
	for k in xrange(1, nt):
		dB = random.gauss(0.0, sqrtdt)
		Xt[k] = Xt[k-1] + (XT - Xt[k-1]) / (T - t) * dt + dB
		Bt += dB
		t  += dt

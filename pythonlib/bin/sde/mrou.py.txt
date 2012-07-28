#!/usr/bin/python -Wall

# ================================================================
# Routines for generating discrete-time approximations to the
# mean-reverting Ornstein-Uhlenbeck process.
#
# SDE:    dX = (m-X)*dt + sigma*db.
# Mean:   X0*exp(-t) + m*(1 - exp(-t)).
# Stddev: sqrt(sigma&*2/2 * (1 - exp(-2*t))).
#
# John Kerl
# kerl.john.r@gmail.com
# 2010-02-20
# ================================================================

from   __future__ import division # 1/2 = 0.5, not 0.
import copy, sys, re, random
from   math import sqrt, exp

# ----------------------------------------------------------------
# Writes the motion into the Xt array, which must be predimensioned.  The Bt
# array must be an already-computed Brownian motion of the same length.

def get_mrou_series_from_BM(Xt, Bt, X0, m, sigma, dt):
	nt    = len(Bt)
	Xt[0] = X0
	for k in xrange(1, nt):
		dB  = Bt[k] - Bt[k-1]
		Xt[k] = Xt[k-1] + (m - Xt[k-1]) * dt + sigma * dB

# ----------------------------------------------------------------
# Writes the motion into the Xt array, which must be predimensioned.

def get_mrou_series_from_SDE(Xt, X0, m, sigma, dt):
	nt     = len(Xt)
	sqrtdt = sqrt(dt)
	Bt     = 0.0

	Xt[0] = X0
	for k in xrange(1, nt):
		dB  = random.gauss(0, sqrtdt)
		Xt[k] = Xt[k-1] + (m - Xt[k-1]) * dt + sigma * dB
		Bt += dB

# ----------------------------------------------------------------
# Writes the mean of the motion into the mean_series array, which must be
# predimensioned.  ts must be already filled out.

def get_mrou_mean_series(mean_series, X0, m, ts):
	nt = len(ts)
	for i in xrange(0, nt):
		t = ts[i]
		expmt = exp(-t)
		mean_series[i] = X0 * expmt + m*(1 - expmt)

# ----------------------------------------------------------------
# Writes the stddev of the motion into the stddev_series array, which must be
# predimensioned.  ts must be already filled out.

def get_mrou_stddev_series(stddev_series, sigma, ts):
	nt = len(ts)
	for i in xrange(0, nt):
		t = ts[i]
		stddev_series[i] = sqrt(sigma**2/2 * (1 - exp(-2*t)))

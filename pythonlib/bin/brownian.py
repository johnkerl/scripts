#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2008-01-30
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
import random
import kerlutil

# ----------------------------------------------------------------
# 1D Brownian motion
# As is standard in Python, use an optional argument to implement what would be
# called a "static auto" in C or a "save parameter" in Fortran -- a local
# variable which is saved between calls.
def B(t, dt, uprev=[0.0]):
	du = random.gauss(0, dt)
	uprev[0] += du
	return uprev[0]

# ----------------------------------------------------------------
# 2D Brownian motion
def B2(t, dt, uprev=[0.0, 0.0]):
	du = random.gauss(0, dt)
	dv = random.gauss(0, dt)
	uprev[0] += du
	uprev[1] += dv
	return [uprev[0], uprev[1]]

# ----------------------------------------------------------------
def do_1D():
	T = 10.0
	dt = 0.01
	ts = kerlutil.mfrange(0, dt, T)
	nt = len(ts)

	# Brownian motion.
	# Run this first to find out what B(T) turns out to be.
	Bts = []
	for t in ts:
		Bt = B(t, dt)
		Bts.append(Bt)
	BT = Bts[-1]

	# Brownian bridge:  R(t) = B(t) - (t/T) B(T).
	Rts = []
	for i in range(0, nt):
		t  = ts[i]
		Bt = Bts[i]
		Rt = Bt - (t/T) * BT
		Rts.append(Rt)

	for i in range(0, nt):
		t  = ts[i]
		Bt = Bts[i]
		Rt = Rts[i]
		print "%11.6f %11.6f %11.6f" % (t, Bt, Rt)

# ----------------------------------------------------------------
def do_2D():
	T = 10.0
	dt = 0.01
	ts = kerlutil.mfrange(0, dt, T)
	nt = len(ts)

	# Brownian motion.
	# Run this first to find out what B(T) turns out to be.
	Bts = []
	for t in ts:
		Bt = B2(t, dt)
		Bts.append(Bt)
	BT = Bts[-1]

	# Brownian bridge:  R(t) = B(t) - (t/T) B(T).
	Rts = []
	for i in range(0, nt):
		t  = ts[i]
		Bt = Bts[i]
		Rt = [ Bt[0] - (t/T) * BT[0], Bt[1] - (t/T) * BT[1] ]
		Rts.append(Rt)

	for i in range(0, nt):
		t  = ts[i]
		Bt = Bts[i]
		Rt = Rts[i]
		#print "%11.6f %11.6f %11.6f" % (t, Bt[0], Bt[1])
		print "%11.6f %11.6f %11.6f" % (t, Rt[0], Rt[1])

# ----------------------------------------------------------------
#do_1D()
do_2D()

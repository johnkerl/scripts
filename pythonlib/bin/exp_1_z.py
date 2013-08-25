#!/usr/bin/python

# ================================================================
# Copyright (c) John Kerl 2007
# kerl.john.r@gmail.com
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
# Import the cmath module rather than the math module so that exp et al. may
# take complex arguments.
from cmath import *
import sys
from kerlutil import *

# ================================================================
# Integrate e^(1/z) around the essential singularity z=0, with path Re^it, and
# see what happens for smaller and smaller R.
# ----------------------------------------------------------------
def f(z):
	return exp(1.0/z)
	#return exp(z)

# ----------------------------------------------------------------
def pathz(R,t):
	return R * exp(1j*t)

# ----------------------------------------------------------------
# Mesh over path
tlo =  0.0
thi =  2*pi
nt  = 1000
dt = (thi-tlo)/nt

#[R1,R2,R3,R4] = [1.0, 0.1, 0.01, 0.001]
#[R1,R2,R3,R4] = [1.0, 0.9, 0.8, 0.7]
[R1,R2,R3,R4] = [1.0, 0.8, 0.6, 0.4]

for t in mfrange(tlo, dt, thi):
	z1 = pathz(R1,t)
	z2 = pathz(R2,t)
	z3 = pathz(R3,t)
	z4 = pathz(R4,t)

	w1 = f(z1)
	w2 = f(z2)
	w3 = f(z3)
	w4 = f(z4)

	printf_row([t, w1.real, w1.imag, w2.real, w2.imag, w3.real, w3.imag, w4.real, w4.imag])
	#printf_row([t, w1.real, w1.imag])

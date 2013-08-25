#!/usr/bin/python -Wall

# ================================================================
# Copyright (c) John Kerl 2007
# kerl.john.r@gmail.com
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
from math import *

# ----------------------------------------------------------------
def fprime(x):
	return sin(x)
	#return exp(x)
# ----------------------------------------------------------------
def fexact(x):
	return 1 - cos(x)
	#return exp(x) - 1
# ----------------------------------------------------------------

n  = 1000
dx = 0.5

L  = 0.0
R  = 0.0

x  = 0.0
for i in range(0, n):
	L += fprime(x)    * dx
	R += fprime(x+dx) * dx
	E  = fexact(x)
	error = E - L

	#print "%7.4f %7.4f %7.4f %7.4f" % (x, L, E, R)
	#print "%7.4f %7.4f %7.4f" % (x, L, E)
	#print "%7.4f %7.4f" % (x, error)
	print "%7.4f %7.4f %7.4f %7.4f" % (x, L, E, error)
	x += dx

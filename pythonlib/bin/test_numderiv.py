#!/usr/bin/python -Wall

# ================================================================
# Copyright (c) John Kerl 2007
# kerl.john.r@gmail.com
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
from kerlutil import *
from math import *
#from cmath import *

def c(x):
	return 1.0
def i(x):
	return x
def s(x):
	return x**2
def f(x):
	return sin(x)

def g(z):
	return exp(1j*z)/z

# ----------------------------------------------------------------
def rtest():
	#x  = frange(2., 4., 20)
	x  = frange(0, 2*pi, 200)
	y  = map(f, x)
	yp = numderiv(f, x)

	n = len(x)
	for i in range(0, n):
		printf_row([x[i], y[i], yp[i]])
#rtest()

# ----------------------------------------------------------------
from cmath import *

def ctest():
	#x  = frange(2., 4., 20)
	z  = ztrange(1., 0, 2*pi, 200)
	w  = map(g, z)
	wp = numderiv(g, z)

	n = len(z)
	for i in range(0, n):
		printf_row(clist_to_rlist([z[i], w[i], wp[i]]))
ctest()

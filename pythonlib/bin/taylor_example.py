#!/usr/bin/python -Wall

# ================================================================
# Copyright (c) John Kerl 2007
# kerl.john.r@gmail.com
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
from math import *

# ----------------------------------------------------------------
# Taylor series for e^x, with tabulation along the way.
def tabulate(x):
	sum = 0.0
	k = 0
	kfact = 1
	xpower = 1
	print "x=%11.7e" % (x)
	while True:
		term = xpower / kfact
		if (abs(term) < 1e-8):
			break
		sum += term
		print "  sum=%11.7e term=%11.7e" % (sum, term)
		#print "k=%4d kfact=%4d x^%d=%11.7e" % (k, kfact, k, xpower)
		xpower *= x
		kfact *= (k+1)
		k += 1
	print "e^x=%11.7e" % (sum)
	print

# ----------------------------------------------------------------
tabulate(0.001)
tabulate(0.01)
tabulate(0.1)
tabulate(1.0)
tabulate(10.0)

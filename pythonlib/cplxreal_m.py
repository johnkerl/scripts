#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2008-02-05
#
# In Python, x.conjugate() for real x throws an exception.  This is really
# annoying.  Here I implement a substitute.  Likewise for real(),
# imag(), and phz().  Note that abs() is already properly overloaded.
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
import math

# ----------------------------------------------------------------
def conj(c):
	if (isinstance(c, complex)):
		return c.conjugate()
	else:
		return c

# ----------------------------------------------------------------
def real(c):
	if (isinstance(c, complex)):
		return c.real
	else:
		return c

# ----------------------------------------------------------------
def imag(c):
	if (isinstance(c, complex)):
		return c.imag
	else:
		return 0.0

# ----------------------------------------------------------------
def phz(c):
	if (isinstance(c, complex)):
		return math.atan2(c.imag, c.real)
	else:
		if (c < 0.0):
			return math.pi
		else:
			return 0.0

# ----------------------------------------------------------------
def abssq(c):
	if (isinstance(c, complex)):
		return real(c.conjugate() * c)
	else:
		return c * c

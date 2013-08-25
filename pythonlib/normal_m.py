#!/usr/bin/python -Wall

# ================================================================
# Functions:
# * erf
# * erfc
# * inverf
# * normalpdf
# * normalcdf
# * invnorm
#
# Definition of erf:
# erf(x) = 2/sqrt(pi) int_0^x exp(-t^2) dt
#
# Connection with normalcdf:
# normalcdf(x) = 1/2 (1 + erf(x/sqrt(2)))
#
# There are series expansions which work; some formulas herein are from
# Mathworld and Wikipedia.  However, I found some code at root.cern.ch (under
# GNU LPL) which is more elegant.  This is due to Brun and Rademakers; see
# citation below.
#
# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2007-08-13
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
from math     import *
from kerlutil import *  # For factorial and double factorial

# ================================================================
def normalpdf(x):
	#return exp(-x**2) / sqrt(2.0*pi)
	return exp(-x**2) * 0.3989422804014327 # This is 1/sqrt(2pi)

# ----------------------------------------------------------------
def normalcdf(x):
	return 0.5 * (1.0 + erf(x/sqrt(2)))

# ----------------------------------------------------------------
#   N     = (1 + erf(x/sqrt(2))) * 0.5
# 2 N     =  1 + erf(x/sqrt(2))
# 2 N - 1 =  erf(x/sqrt(2))
# inverf(2 N - 1) =  x/sqrt(2)
# sqrt(2) * inverf(2 N - 1) =  x

def invnorm(x):
	return sqrt(2) * inverf(2 * x - 1)

# ================================================================
## This works well for positive x around 1.
#
## erf(x) = 2/sqrt(pi) sum n=0 to infty (-1)^n x^(2n+1)/(n!(2n+1))
#
#def erftaylor(x):
#	tol = 1e-15
#	x *= 1.0
#
#	sum = 0.0
#	done = 0
#	n = 0
#	neg_1_to_n = 1
#	while (not done):
#		two_n_plus_1 = n+n+1
#		# xxx power up n iteratively ...
#		# xxx compute n! iteratively ...
#		term = neg_1_to_n * x**two_n_plus_1 / fact(n) / two_n_plus_1
#		sum += term
#		#print "-- et", n
#		if (abs(term) < tol):
#			break
#
#		neg_1_to_n = -neg_1_to_n
#		n += 1
#
#	return sum * 2/sqrt(pi)

## ----------------------------------------------------------------
## This works well for positive x less than 0.01 or so.
#
## erf(x) = 2/sqrt(pi) exp(-x^2) sum n=0 to infty 2^n/(2n+1)!! x^(2n+1)
#
#def erfsmallx(x):
#	tol = 1e-15
#	x *= 1.0
#
#	sum = 0.0
#	done = 0
#	n = 0
#	neg_1_to_n = 1
#	while (not done):
#
#		two_n_plus_1 = n+n+1
#		# xxx power up n iteratively ...
#		# xxx compute n! iteratively ...
#		term = 2**n / dfact(two_n_plus_1) * x**two_n_plus_1
#		#print "-- es", n
#		sum += term
#		if (abs(term) < tol):
#			break
#
#		neg_1_to_n = -neg_1_to_n
#		n += 1
#
#	return sum * 2.0/sqrt(pi) * exp(-x**2)

## ----------------------------------------------------------------
## This works well for x > 5 or so.
## erf(x) = 1 - exp(-x^2)/sqrt(pi) sum n=0 to infty
##   (-1)^n (2n-1)!!/2^n x^(-2n+1)
#def erfbigx(x):
#	tol = 1e-15
#
#	sum = 0.0
#	done = 0
#	n = 0
#	neg_1_to_n = 1
#	while (not done):
#
#		two_n_plus_1 = n+n+1
#		# xxx power up n iteratively ...
#		# xxx compute n! iteratively ...
#		term = neg_1_to_n * dfact(2*n-1) / 2**n * x**(-2*n+1)
#		sum += term
#		#print "-- eb", n
#		if (abs(term) < tol):
#			break
#
#		neg_1_to_n = -neg_1_to_n
#		n += 1
#
#	return 1.0 - exp(-x**2)/sqrt(pi) * sum

## ----------------------------------------------------------------
#def erf(x):
#	# erf is an odd function.
#	sign = 1
#	if (x < 0):
#		x = -x
#		sign = -1
#
#	if (x < 0.01):
#		rv = erfsmallx(x)
#	elif (x < 5):
#		rv = erftaylor(x)
#	else:
#		rv = erfbigx(x)
#
#	return rv * sign

## ----------------------------------------------------------------
## Auxiliary routine for inverf (see comments below).
##
## This *must* be memoized, else computation of these coefficients quickly
## dominates for k > 10 or so.
#
#def inverfcoeff(k, cache={}):
#	if (k in cache):
#		return cache[k]
#	if (k == 0):
#		return 1
#	sum = 0
#	for m in range(0, k):
#		sum += inverfcoeff(m) * inverfcoeff(k-1-m) / (m+1.0) / (2*m+1)
#
#	cache[k] = sum
#	return sum

## ----------------------------------------------------------------
# This has convergence issues for x near -1 and 1.  Closer to 0, it's fine.
## inverf(x) = sum k=0 to infty c_k/(2k+1) ((sqrt(pi) x /2)^(2k+1) where
##   c_0 = 1
## and
##   c_k = sum m=0 to k-1 of c_m c_{k-1-m}/(m+1)(2m+1).
#
#def inverf(x):
#	tol = 1e-15
#	if ((x <= -1.0) or (x >= 1.0)):
#		print >> sys.stderr, "inverf:  input", x, "out of domain (0,1)."
#		sys.exit(1)
#
#	sum = 0.0
#	k = 0
#	done = 0
#	sqrtpix2 = sqrt(pi) * x / 2
#	while (not done):
#		term = inverfcoeff(k) / (2.0*k+1) * sqrtpix2 ** (2*k+1)
#		if (abs(term) < tol):
#			done = 1
#		sum += term
#		print "--", k, term
#		k += 1
#
#	return sum

# ================================================================
# Copyright (C) 1995-2004, Rene Brun and Fons Rademakers.
# All rights reserved.
# Released under the terms of the GNU LPL.
# Translated into Python John Kerl 2007.

# ----------------------------------------------------------------
def erf(x):
	return 1.0 - erfc(x)

# ----------------------------------------------------------------
def erfc(x):
	# The parameters of the Chebyshev fit
	a1  = -1.26551223
	a2  =  1.00002368

	a3  =  0.37409196
	a4  =  0.09678418

	a5  = -0.18628806
	a6  =  0.27886807

	a7  = -1.13520398
	a8  =  1.48851587

	a9  = -0.82215223
	a10 = 0.17087277

	rv = 1.0
	z = abs(x)

	if (z <= 0.0):
		return rv # erfc(0) = 1

	t = 1.0 / (1.0 + 0.5*z)

	rv = t*exp((-z**2) \
		+a1+t*(a2+t*(a3+t*(a4+t*(a5+t*(a6+t*(a7+t*(a8+t*(a9+t*a10)))))))))

	if (x < 0):
		rv = 2.0 - rv # erfc(-x) = 2-erfc(x)
	return rv

# ----------------------------------------------------------------
# Domain -1 < x < 1.
def inverf(x):
	maxits = 50
	tol = 1e-14
	sqrtpio2 = 0.8862269254527579 # sqrt(pi)/2.0

	if (abs(x) <= tol):
		return sqrtpio2 * x

	if (abs(x) >= 1.0):
		print >> sys.stderr, "inverf domain error: x", x, "not in (-1, 1)."
		sys.exit(1)

	# Newton-Raphson iterations
	erfi = sqrtpio2 * abs(x)
	y0 = erf(0.9 * erfi)
	derfi = 0.1 * erfi

	for iter in range(0, maxits):
		y1 = 1.0 - erfc(erfi)
		dy1 = abs(x) - y1
		if (abs(dy1) < tol):
			if (x < 0):
				return -erfi
			else:
				return erfi
		dy0 = y1 - y0
		derfi *= dy1/dy0
		y0 = y1
		erfi += derfi
		if (abs(derfi/erfi) < tol):
			if (x < 0):
				return -erfi
			else:
				return erfi

	print >> sys.stderr, "inverf(" + str(x) + "): did not converge."
	sys.exit(1)


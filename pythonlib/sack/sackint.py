#!/usr/bin/python -Wall

# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

# ----------------------------------------------------------------
def gcd(a, b):
	r = 0
	if (a == 0):
		return b
	if (b == 0):
		return a

	while (1):
		r = a % b
		if (r == 0):
			break
		a = b
		b = r
	if (b < 0):
		b = -b
	return b

# ----------------------------------------------------------------
# Blankinship's algorithm

def extgcd(a, b):

	# Initialize
	mprime = 1
	n      = 1
	m      = 0
	nprime = 0
	c      = a
	d      = b

	while (1):
		# Divide
		q = c / d
		r = c % d
		# Note:  now c = qd + r and 0 <= r < d

		# Remainder zero?
		if (r == 0):
			break

		# Recycle
		c = d
		d = r

		t      = mprime
		mprime = m
		qm     = q * m
		m      = t - qm

		t      = nprime
		nprime = n
		qn     = q * n
		n      = t - qn
	return [d, m, n]

# ----------------------------------------------------------------
# This function should be invoked with only one argument.
# The optional argument is a way to have a local static in Python.
# See Lutz & Ascher, 2nd. ed., p 241.

def eulerphi(n, cached_n_and_phi=[2,1]):
	if (n == cached_n_and_phi[0]):
		# Cache hit
		return cached_n_and_phi[1]

	phi = 0
	for i in range (1, n):
		if (gcd(n, i) == 1):
			phi += 1
	return phi

	cached_n_and_phi[0] = n
	cached_n_and_phi[1] = phi
	return phi

# ----------------------------------------------------------------
# Binary exponentiation

def intexp(x, e):
	xp = x
	rv = 1

	if (e < 0):
		print "intexp:  negative exponent", e, "disallowed."
		raise RuntimeError

	while (e != 0):
		if (e & 1):
			rv = (rv * xp)
		e = e >> 1
		xp = (xp * xp)
	return rv

# ----------------------------------------------------------------
# Binary exponentiation

def intmodexp(x, e, m):
	xp = x
	rv = 1

	if (e < 0):
		e = -e
		x = intmodrecip(x, m)

	while (e != 0):
		if (e & 1):
			rv = (rv * xp) % m
		e = e >> 1
		xp = (xp * xp) % m
	return rv

# ----------------------------------------------------------------
def intmodrecip(x, m):
	if (gcd(x, m) != 1):
		print "intmodrecip:  impossible inverse", x, "mod", m
		raise RuntimeError
	phi = eulerphi(m)
	return intmodexp(x, phi-1, m)

# ----------------------------------------------------------------
def factorial(n):
	if (n < 0):
		print "factorial: negative input disallowed."
		raise RuntimeError
	if (n < 2):
		return 1
	rv = 1
	for k in range(2, n+1):
		rv *= k
	return rv

# ----------------------------------------------------------------
# How to compute P(n) = number of partitions of n.  Examples for n = 1 to 5:
#
# 1    2      3        4          5
#      1 1    2 1      3 1        4 1
#             1 1 1    2 2        3 2
#                      2 1 1      3 1 1
#                      1 1 1 1    2 2 1
#                                 2 1 1 1
#                                 1 1 1 1 1
#
# This is a first-rest algorithm.  Loop over possible choices k for the first
# number.  The rest must sum to n-k. Furthermore, the rest must be descending
# and so each must be less than or equal to k.  Thus we naturally have an
# auxiliary function P(n, m) counting partitions of n with each element less
# than or equal to m.

def num_ptnsm(n, m):
	if (n <  0): return 0
	if (n <= 1): return 1
	if (m == 1): return 1
	sum = 0
	for k in range(1, m+1):
		if (n-k >= 0):
			sum += num_ptnsm(n-k, k)
	return sum

# ----------------------------------------------------------------
def num_ptns(n):
	return num_ptnsm(n, n)

# ----------------------------------------------------------------
def ptnsm(n, m):
	rv = []
	if (n <  0): return 0
	if (n == 0): return [[]]
	if (n == 1): return [[1]]
	if (m == 1): return [[1] * n]
	sum = 0
	for k in range(1, m+1):
		if (n-k >= 0):
			tails = ptnsm(n-k, k)
			for tail in tails:
				rv.append([k] + tail)
	return rv

# ----------------------------------------------------------------
def ptns(n):
	return ptnsm(n, n)

#for n in range(1, 21):
#	a = onum_ptns(n)
#	b =  num_ptns(n)
#	print "%2d %2d %2d" % (n, a, b)

#for n in range(1, 5+1):
#	for m in range(1, n+1):
#		p = num_ptnsm(n, m)
#		print n, m, p
#	print

#for n in range(1, 7+1):
#	for m in range(1, n+1):
#		X = ptnsm(n, m)
#		print n, m, len(X), X
#	print

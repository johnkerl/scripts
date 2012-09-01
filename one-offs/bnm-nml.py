#!/usr/bin/python

# ================================================================
# Plot binomial and normal probability distributions side-by-side.
# John Kerl 2012-08-31
# ================================================================

from __future__ import division
import sys
from math import sqrt, exp, floor, pi

# ----------------------------------------------------------------
def normal_pdf(x, mu, sigma):
	return exp(-0.5 * (x-mu)**2 / sigma**2) / (sigma * sqrt(2*pi))

# ----------------------------------------------------------------
def binc(n, k):
	if (k > n):
		return 0
	if (k < 0):
		return 0
	if (k > int(n/2)):
		k = n - k

	rv = 1
	for j in range(0, k):
		rv *= n - j
		rv /= j + 1
	return rv

# ----------------------------------------------------------------
def binomial_pmf(k, n, p):
	return binc(n, k) * p**k * (1-p)**(n-k)

# ----------------------------------------------------------------
n = 100
p = 0.5
delta = 0.02
argc = len(sys.argv)
if argc == 2:
	n = int(sys.argv[1])
elif argc == 3:
	n =   int(sys.argv[1])
	p = float(sys.argv[2])
elif argc == 4:
	n =       int(sys.argv[1])
	p =     float(sys.argv[2])
	delta = float(sys.argv[3])

xmin = -0.25 * n
xmax =  1.25 * n

mean   = n * p
stddev = sqrt(n * p * (1-p))

x = xmin
while x <= xmax:
	#k = int(floor(x))
	k = int(floor(x+0.5))
	print "%f,%f,%f" % (x, normal_pdf(x, mean, stddev), binomial_pmf(k, n, p))

	x += delta

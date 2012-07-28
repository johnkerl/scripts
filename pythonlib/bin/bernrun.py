#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2008-10-16
# ================================================================
# This is a program find the distribution of lengths of runs of consecutive
# zeroes in a sequence of IID Bernoulli random variables.
# ================================================================

from   __future__ import division
import sys
import re
import random

# ----------------------------------------------------------------
def get_counts(p, nflips, verbose=0):

	k = 0
	runlen = 0
	runlens = []
	maxrunlen = 0
	while (k < nflips):
		k += 1

		X = 0
		if (random.uniform(0, 1) < p):
			X = 1

		if (X == 0):
			runlen += 1
		else:
			if (runlen > 0):
				runlens.append(runlen)
				if (runlen > maxrunlen):
					maxrunlen = runlen
			runlen = 0

		if (verbose): print "-- X =", X

	if (runlen > 0):
		if (verbose): print "-- runlen =", runlen
		runlens.append(runlen)
		if (runlen > maxrunlen):
			maxrunlen = runlen

	if (verbose): print "-- maxrunlen =", maxrunlen

	bins   = range(0, maxrunlen+1)
	counts = [0] * (maxrunlen+1)
	for runlen in runlens:
		counts[runlen] += 1
	if (verbose):
		print "bins   =", bins
		print "counts =", counts
	return [bins, counts]

# ----------------------------------------------------------------
def usage():
	print >> sys.stderr, "foo"
	sys.exit(1)

# ================================================================
nflips   = 100000
p        = 0.5
verbose  = 0

argc = len(sys.argv)
for argi in range(1, argc):

	if re.match(r'^p=', sys.argv[argi]):
		p = float(sys.argv[argi][2:])
		if (p < 0): usage()
		if (p > 1): usage()

	elif re.match(r'^N=', sys.argv[argi]):
		nflips = int(sys.argv[argi][2:])
		if (nflips < 1): usage()

	elif re.match(r'^v=', sys.argv[argi]):
		verbose = int(sys.argv[argi][2:])

	else:
		usage()
	argi += 1

[bins, counts] = get_counts(p, nflips, verbose)
n = len(bins)
for k in range(1, n):
	print "%6d %6d" % (bins[k], counts[k])

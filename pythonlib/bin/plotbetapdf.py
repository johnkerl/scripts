#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2008-02-04
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
import betapdf_m
import kerlutil
import sys

alpha = 2.0
beta  = 3.0
nx    = 500

# ----------------------------------------------------------------
# Parse the command line.  Syntax: not -nx 400 but nx=400.
# This is crude (it's not syntax-error tolerant) but it's an easy-to-code
# hack.  It works in any language with an eval/exec (e.g. Python, Perl).
argc = len(sys.argv)
for argi in range(1, argc):
	if ((sys.argv[argi] == '-h') or (sys.argv[argi] == '--help')):
		print >> sys.stderr, "Usage: %s [nx=...] [alpha=...] [beta=...]" \
			% (sys.argv[0])
		sys.exit(1)
	exec(sys.argv[argi])

# ----------------------------------------------------------------
dx = 1.0 / nx
denom =  betapdf_m.betapdfdenom(alpha, beta)
for x in kerlutil.mfrange(dx, dx, 1.0):
	if (x >= 1.0): break

	#print "%.10f %.10f" % (x, betapdf_m.betapdf(x, alpha, beta))
	print "%.10f %.10f" % (x, betapdf_m.betapdfaux(x, alpha, beta, denom))

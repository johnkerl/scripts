#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2007-08-14
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
import sys
import sackmat_m
import stats_m

argc = len(sys.argv)
if (argc != 2):
	print >> sys.stderr, "Usage: %s {x file name}" % (sys.argv[0])
	print >> sys.stderr, "Use \"-\" as file name for stdin."
	sys.exit(1)

xs = sackmat_m.read_column_vector(float, sys.argv[1])
stats_m.print_normal_quantiles_zx(xs)

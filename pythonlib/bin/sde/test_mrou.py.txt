#!/usr/bin/python -Wall

# ================================================================
# Tests the routines in mrou.py:
# * Print time-series data in plottable format.
# * Confidence intervals mu_t, mu_t +/- sigma_t, and mu_t +/- 2 sigma_t
#   are also plotted.
#
# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2008-02-20
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
import sys, re, math, random
import brownian, mrou
import sackmat_m, stats_m
from math import sqrt, exp, log

# ----------------------------------------------------------------
def usage():
	print >> sys.stderr, "Usage: %s [options]" % (sys.argv[0])
	print >> sys.stderr, "Options:"
	print >> sys.stderr, "  T=[float]"
	print >> sys.stderr, "  nX=[int]"
	print >> sys.stderr, "  nt=[int]"
	print >> sys.stderr, "  X0=[float]"
	print >> sys.stderr, "  m=[float]"
	print >> sys.stderr, "  s=[float]"
	sys.exit(1)

# ----------------------------------------------------------------
T  = 10.0
nX = 20
nt = 1000
X0 = 1.0
m  = 3.0
s  = 0.5

argc = len(sys.argv)
for argi in range(1, argc):
	arg = sys.argv[argi]
	if arg == '-h' or arg == '--help': usage()

	elif re.match(r'^T=',  arg): T  = float(arg[2:])
	elif re.match(r'^nX=', arg): nX = int  (arg[3:])
	elif re.match(r'^nt=', arg): nt = int  (arg[3:])

	elif re.match(r'^X0=', arg): X0 = float(arg[3:])
	elif re.match(r'^m=',  arg): m  = float(arg[2:])
	elif re.match(r'^s=',  arg): s  = float(arg[2:])

	else: usage()

dt = T / nt

mean_series   = [0.0] * nt
stddev_series = [0.0] * nt
Xts = sackmat_m.make_zero_matrix(nX, nt)

ts  = brownian.get_t_series(nt, dt)
mrou.get_mrou_mean_series  (mean_series, X0, m, ts)
mrou.get_mrou_stddev_series(stddev_series, s, ts)
for i in xrange(0, nX):
	mrou.get_mrou_series_from_SDE(Xts[i], X0, m, s, dt)

# Plot
for i in xrange(0, nt):
	print '%11.7f' % (ts[i]),
	print '%11.7f' % (mean_series[i] - 2.0 * stddev_series[i]),
	print '%11.7f' % (mean_series[i] -       stddev_series[i]),
	print '%11.7f' % (mean_series[i]),
	print '%11.7f' % (mean_series[i] +       stddev_series[i]),
	print '%11.7f' % (mean_series[i] + 2.0 * stddev_series[i]),
	for j in xrange(0, nX):
		print ' %11.7f' % Xts[j][i],
	print

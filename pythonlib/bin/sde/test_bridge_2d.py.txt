#!/usr/bin/python -Wall

# ================================================================
# Plots Brownian bridges in the plane.
#
# John Kerl
# kerl.john.r@gmail.com
# 2008-02-20
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
import sys, re, math, random
import brownian
import sackmat_m, stats_m
from math import sqrt, exp, log

# ----------------------------------------------------------------
def usage():
	print >> sys.stderr, "Usage: %s [options]" % (sys.argv[0])
	print >> sys.stderr, "Options:"
	print >> sys.stderr, "  T=[float]"
	print >> sys.stderr, "  nR=[int]"
	print >> sys.stderr, "  nt=[int]"
	print >> sys.stderr, "  X0=[float]"
	print >> sys.stderr, "  Y0=[float]"
	print >> sys.stderr, "  XT=[float]"
	print >> sys.stderr, "  YT=[float]"
	sys.exit(1)

# ----------------------------------------------------------------
T  = 2.0

nR = 20
nt = 2000
X0 = -2.0
Y0 = -1.0
XT = 4.0
YT = 3.0

argc = len(sys.argv)
for argi in range(1, argc):
	arg = sys.argv[argi]
	if arg == '-h' or arg == '--help': usage()
	elif re.match(r'^T=',  arg): T  = float(arg[2:])
	elif re.match(r'^nR=', arg): nR = int  (arg[3:])
	elif re.match(r'^nt=', arg): nt = int  (arg[3:])
	elif re.match(r'^X0=', arg): X0 = float(arg[3:])
	elif re.match(r'^Y0=', arg): Y0 = float(arg[3:])
	elif re.match(r'^XT=', arg): XT = float(arg[3:])
	elif re.match(r'^YT=', arg): YT = float(arg[3:])

	else: usage()

dt = T / nt

ts  = brownian.get_t_series(nt, dt)

BtXs = sackmat_m.make_zero_matrix(nR, nt)
BtYs = sackmat_m.make_zero_matrix(nR, nt)
Xts  = sackmat_m.make_zero_matrix(nR, nt)
Yts  = sackmat_m.make_zero_matrix(nR, nt)
for i in xrange(0, nR):
	brownian.get_BM_series(BtXs[i], dt)
	brownian.get_BM_series(BtYs[i], dt)
	brownian.get_BB_series_from_BM(Xts[i], BtXs[i], X0, XT, dt)
	brownian.get_BB_series_from_BM(Yts[i], BtYs[i], Y0, YT, dt)

# ----------------------------------------------------------------
# Print time-series data.

for i in xrange(0, nt):
	for j in xrange(0, nR):
		print ' %11.7f %11.7f' % (Xts[j][i], Yts[j][i]),
	print

#!/usr/bin/python -Wall

# ================================================================
# Tests the routines in brownian.py in three ways:
# * Print time-series data in plottable format.
# * Print time slices at specified times s and t, in a format suitable
#   for histogramming.
# * Print population and sample mean, variance, and covariance of X_s
#   and X_t for specified s and t.
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
	print >> sys.stderr, "  s=[float]"
	print >> sys.stderr, "  t=[float]"
	print >> sys.stderr, "  nX=[int]"
	print >> sys.stderr, "  nt=[int]"
	print >> sys.stderr, "  X0=[float]"
	print >> sys.stderr, "  XT=[float]"
	print >> sys.stderr, "  bm | bbbm | bbsde"
	print >> sys.stderr, "  stats | print_slices | plot"
	sys.exit(1)

# ----------------------------------------------------------------
T  = 2.0
s  = 0.8
t  = 1.6

nX = 10000
nt = 200
X0 = 2.0
XT = 3.0

which_process = 'bm'
which_action  = 'stats'

argc = len(sys.argv)
for argi in range(1, argc):
	arg = sys.argv[argi]
	if arg == '-h' or arg == '--help': usage()

	elif re.match(r'^T=',  arg): T  = float(arg[2:])
	elif re.match(r'^s=',  arg): s  = float(arg[2:])
	elif re.match(r'^t=',  arg): t  = float(arg[2:])

	elif re.match(r'^nX=', arg): nX = int  (arg[3:])
	elif re.match(r'^nt=', arg): nt = int  (arg[3:])
	elif re.match(r'^X0=', arg): X0 = float(arg[3:])
	elif re.match(r'^XT=', arg): XT = float(arg[3:])

	elif arg == 'bm'           : which_process = 'bm'
	elif arg == 'bbbm'         : which_process = 'bbbm'
	elif arg == 'bbsde'        : which_process = 'bbsde'

	elif arg == 'stats'        : which_action  = 'stats'
	elif arg == 'print_slices' : which_action  = 'print_slices'
	elif arg == 'plot'         : which_action  = 'plot'

	else: usage()

if (s < 0) or (s >= T):
	print >> sys.stderr, 's = %11.7f is outside (0, T = %11.7f).' & (s, T)
	sys.exit(1)
if (t < 0) or (t >= T):
	print >> sys.stderr, 't = %11.7f is outside (0, T = %11.7f).' & (t, T)
	sys.exit(1)

dt = T / nt

ts  = brownian.get_t_series(nt, dt)

if   which_process == 'bm':
	Bts = sackmat_m.make_zero_matrix(nX, nt)
	for i in xrange(0, nX):
		brownian.get_BM_series(Bts[i], dt)
	values = Bts
elif which_process == 'bbbm':
	Bts = sackmat_m.make_zero_matrix(nX, nt)
	Xts = sackmat_m.make_zero_matrix(nX, nt)
	for i in xrange(0, nX):
		brownian.get_BM_series(Bts[i], dt)
		brownian.get_BB_series_from_BM(Xts[i], Bts[i], X0, XT, dt)
	values = Xts
elif which_process == 'bbsde':
	Yts = sackmat_m.make_zero_matrix(nX, nt)
	for i in xrange(0, nX):
		brownian.get_BB_series_from_SDE(Yts[i], X0, XT, dt)
	values = Yts

if   which_process == 'bm':    values = Bts
elif which_process == 'bbbm':  values = Xts
elif which_process == 'bbsde': values = Yts

# ----------------------------------------------------------------
# Print time-series data.

if which_action == 'plot':
	for i in xrange(0, nt):
		t = ts[i]

		if which_process == 'bm':
			mean_t = 0.0
			stddev_t = sqrt(t)
		else:
			mean_t = X0 + t/T*(XT-X0)
			var_t  = t*(T-t)/T
			stddev_t = sqrt(var_t)

		print '%11.7f' % (t),
		print '%11.7f' % (mean_t - 2*stddev_t),
		print '%11.7f' % (mean_t -   stddev_t),
		print '%11.7f' % (mean_t),
		print '%11.7f' % (mean_t +   stddev_t),
		print '%11.7f' % (mean_t + 2*stddev_t),

		for j in xrange(0, nX):
			print ' %11.7f' % values[j][i],

		print
	sys.exit(0)

# ----------------------------------------------------------------
# Print time slices

time_i = int(s/T * nt)
time_j = int(t/T * nt)

slice_s = values.get_column(time_i)
slice_t = values.get_column(time_j)

if which_action == 'print_slices':
	print 'Slice at %d/%d = %9.4f' % (time_i, nt, s)
	sackmat_m.print_column_vector(slice_s)
	print ''

	print 'Slice at %d/%d = %9.4f' % (time_i, nt, t)
	sackmat_m.print_column_vector(slice_t)
	print ''
	sys.exit(0)

# ----------------------------------------------------------------
# Print stats

if which_process == 'bm':
	print 'Brownian motion'
elif which_process == 'bbbm' or which_process == 'bbsde':
	print 'Brownian bridges'

if which_process == 'bm':
	expected_mean_s = 0.0
	expected_mean_t = 0.0
	expected_var_s  = s
	expected_var_t  = t
	expected_cov_st = min(s, t)

elif which_process == 'bbbm' or which_process == 'bbsde':
	expected_mean_s = X0 + s/T*(XT-X0)
	expected_mean_t = X0 + t/T*(XT-X0)
	expected_var_s  = s*(T-s)/T
	expected_var_t  = t*(T-t)/T
	if s < t:
		expected_cov_st = s*(T-t)/T
	else:
		expected_cov_st = t*(T-s)/T

mean_s = stats_m.find_mean(slice_s)
mean_t = stats_m.find_mean(slice_t)
var_s  = stats_m.find_sampvaraux(slice_s, mean_s)
var_t  = stats_m.find_sampvaraux(slice_t, mean_t)
cov_st = stats_m.find_sample_covariance(slice_s, slice_t)

diff_mean_s = mean_s - expected_mean_s
diff_mean_t = mean_t - expected_mean_t
diff_var_s  = var_s  - expected_var_s
diff_var_t  = var_t  - expected_var_t
diff_cov_st = cov_st - expected_cov_st

if which_process == 'bm':
	print 'T  = %11.7f' % T
elif which_process == 'bbbm' or which_process == 'bbsde':
	print 'X0 = %11.7f' % X0
	print 'XT = %11.7f' % XT
	print 'T  = %11.7f' % T
print ''

print 'i  = %6d  s = %11.7f' % (time_i, s)
print 'j  = %6d  t = %11.7f' % (time_j, t)
print 'nX = %6d nt = %6d' % (nX, nt)
print ''

# Print CI's / sigmas as well ... first, need the distribution of sample var
# and sample cov.
print   'Actual    mean X(s): %11.7f' % mean_s,
print '  Actual    mean X(t): %11.7f' % mean_t
print   'Expected  mean X(s): %11.7f' % expected_mean_s,
print '  Expected  mean X(t): %11.7f' % expected_mean_t
print   'Diff      mean X(s): %11.7f' % diff_mean_s,
print '  Diff      mean X(t): %11.7f' % diff_mean_t
# Variance of sample mean is variance of individual samples over N.
# So, stddev of mean = stddev_t / sqrt N.
stddev_s = sqrt(var_s)
stddev_t = sqrt(var_t)
if stddev_s == 0.0: sigdev_s = 0.0
else:               sigdev_s = diff_mean_s / (stddev_s / sqrt(nX))
if stddev_t == 0.0: sigdev_t = 0.0
else:               sigdev_t = diff_mean_t / (stddev_t / sqrt(nX))
print   '                      %9.6f sigma' % (sigdev_s),
print   '                   %9.6f sigma' % (sigdev_t)
print ''

print   'Actual    Var  X(s): %11.7f' % var_s,
print '  Actual    var  X(t): %11.7f' % var_t
print   'Expected  Var  X(s): %11.7f' % expected_var_s,
print '  Expected  var  X(t): %11.7f' % expected_var_t
print   'Diff      Var  X(s): %11.7f' % diff_var_s,
print '  Diff      var  X(t): %11.7f' % diff_var_t
print ''

print 'Actual    Cov(X(s),X(t)): %11.7f' % cov_st
print 'Expected  Cov(X(s),X(t)): %11.7f' % expected_cov_st
print 'Diff      Cov(X(s),X(t)): %11.7f' % diff_cov_st
print ''

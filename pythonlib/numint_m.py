#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2007-07-02
#
# Under construction
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
import sys
import math
import cmath

# ----------------------------------------------------------------
# Naive -- no refinement.

def nnumint(f, xs):
	"""nnumint(f, xarray):  Naive numerical integration for float and complex."""
	sum = 0
	n = len(xs)
	ys = map(f, xs)
	for i in range(0, n-1):
		sum += 0.5 * (ys[i] + ys[i+1]) * (xs[i+1] - xs[i])
	sum += ys[n-1] * (xs[n-1]-xs[n-2])
	return sum

# ----------------------------------------------------------------
def rnumint(f, lo, hi, h, hmin, tol, level=0):
	# Walk from lo to hi by at most hmax.
	# Compute left-hand and right-hand halves.
	# if abs(difference) <= tol):
	#    use it.
	# else:
	#   if h/2 < hmin:
	#     abend
	#   else:
	#     recurse.

	left = lo
	sum = 0.0
	while (left < hi):
		right = left + h
		if (right > hi):
			right = hi

		# xxx directionalize, to handle reversed real limits as well as linear
		# complex paths.
		half_step = 0.5 * (right - left)
		middle = left + half_step

		fleft   = f(left)
		fmiddle = f(middle)
		fright  = f(middle)

		left_sum  = (fleft   + fmiddle) * 0.5 * half_step
		right_sum = (fmiddle + fright)  * 0.5 * half_step
		#print "-- %11.7f %11.7f %11.7f   %11.7f %11.7f  %5d" % \
		#	(left, middle, right, left_sum, right_sum, level)
		if (abs(left_sum - right_sum) <= tol):
			sum += left_sum + right_sum
			#print "-- %11.7f %11.7f %11.7f %11.7f %5d" % \
			#	(left, middle, right, fmiddle, level)
		elif (half_step < hmin):
			print >> sys.stderr, "rnumint:  h underflow (%.6e)" % (half_step)
			sys.exit(1)
		else:
			sum += rnumint(f, left, right, half_step, hmin, tol, level+1)

		left = right

	return sum

# ================================================================
def myf(x):
	return x
def myc(x):
	return 1.0
#print rnumint(f=myf, lo=0.0, hi=1.0, h=0.3, hmin=1e-6, tol=1e-4)
#print rnumint(f=myf, lo=1.0, hi=0.0, h=0.3, hmin=1e-6, tol=1e-4)
#print rnumint(f=myc, lo=0.0, hi=1.0, h=0.01, hmin=1e-6, tol=1e-4)
#print rnumint(f=math.sin, lo=0.0, hi=2.0*math.pi, h=0.01, hmin=1e-6, tol=1e-7)

# To do:
# * Adaptive with semi-infinite or doubly-infinite.
# * Complex with radial paths.  And, linear w/ spec endpoints.

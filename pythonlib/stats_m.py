#!/usr/bin/python -Wall

# ================================================================
# Some simple statistics routines.
#
# John Kerl
# kerl.john.r@gmail.com
# 2007-06-28
#
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
import math
import copy
import sackmat_m
import normal_m
import sys

# ----------------------------------------------------------------
def make_histogram(farray, lo, hi, num_bins):
	bins = [0] * num_bins

	# Ensure they are floats.
	lo *= 1.0; hi *= 1.0

	# This is loop-invariant; hoist it out.
	mul = num_bins / (hi - lo)

	for element in farray:
		if ((element >= lo) and (element < hi)):
			idx = int((element-lo) * mul)
			bins[idx] += 1
	return bins

# ----------------------------------------------------------------
def make_histogram2(xy_pairs, lo_x, hi_x, num_x_bins, lo_y, hi_y, num_y_bins):
	bins = sackmat_m.make_zero_matrix(num_x_bins, num_y_bins)

	# Ensure they are floats.
	lo_x *= 1.0; hi_x *= 1.0; lo_y *= 1.0; hi_y *= 1.0

	# These are loop-invariant; hoist them out.
	mul_x = num_x_bins / (hi_x - lo_x)
	mul_y = num_y_bins / (hi_y - lo_y)

	for [x, y] in xy_pairs:
		if ((x >= lo_x) and (x < hi_x) and (y >= lo_y) and (y < hi_y)):
			x_idx = int((x-lo_x) * mul_x)
			y_idx = int((y-lo_y) * mul_y)
			bins[x_idx][y_idx] += 1
	return bins

# ----------------------------------------------------------------
def make_histogram_labels(lo, hi, num_bins, center=0):
	list = []
	delta = (hi-lo)/(1.0*num_bins)
	for i in range(0, num_bins):
		if (center):
			label = lo + (i + 0.5) *delta
		else:
			label = lo + i*delta
		list.append(label)
	return list

# ----------------------------------------------------------------
def find_min(farray):
	lo = farray[0]
	for element in farray:
		if (element < lo):
			lo = element
	return lo

# ----------------------------------------------------------------
def find_max(farray):
	hi = farray[0]
	for element in farray:
		if (element > hi):
			hi = element
	return hi

# ----------------------------------------------------------------
def find_bounds(farray):
	lo = farray[0]
	hi = farray[0]
	for element in farray:
		if (element < lo):
			lo = element
		if (element > hi):
			hi = element
	return [lo, hi]

# ----------------------------------------------------------------
# Scalar mean
def find_mean(farray):
	sum = 0.0
	for element in farray:
		sum += element
	return sum / len(farray)

# ----------------------------------------------------------------
# Scalar standard deviation
def find_stddev(farray, mean):
	sum = 0.0
	for element in farray:
		sum += (element - mean) ** 2
	return math.sqrt(sum / (len(farray) - 1))

# ----------------------------------------------------------------
# Standard error, i.e. standard deviation of the sample mean.
def find_stderr(farray, mean):
	s = find_stddev(farray, mean)
	n = len(farray)
	return s / math.sqrt(n)

# ----------------------------------------------------------------
# Population variance
def find_popvaraux(xs, mean):
	sum = 0.0
	for x in xs:
		sum += (x - mean) ** 2
	return sum / len(xs)

def find_popvar(xs):
	return find_popvaraux(xs, find_mean(xs))

# Sample variance
def find_sampvaraux(xs, mean):
	sum = 0.0
	for x in xs:
		sum += (x - mean) ** 2
	return sum / (len(xs) - 1)

def find_sampvar(xs):
	return find_sampvaraux(xs, find_mean(xs))

def find_var_of_sample_mean(xs):
	return find_sampvar(xs) / len(xs)

# U = 1 - <X^4> / (3 <X^2>^2)
# where X is taken to have zero mean
def find_fourth_order_cumulant(farray):
	n     = len(farray)
	sumx  = 0.0
	sumx2 = 0.0
	sumx4 = 0.0

	for x in farray:
		sumx += x
	meanx = sumx / n

	for y in farray:
		x      = y - meanx
		x2     = x*x
		x4     = x2*x2
		sumx2 += x2
		sumx4 += x4
	meanx2 = sumx2 / n
	meanx4 = sumx4 / n
	if meanx2 == 0.0:
		return 0.0
	else:
		return 1.0 - meanx4 / (3 * meanx2 * meanx2);

def find_fourth_order_cumulant_temp(farray):
	n     = len(farray)
	sumx  = 0.0
	sumx2 = 0.0
	sumx3 = 0.0
	sumx4 = 0.0

	for x in farray:
		sumx  += x
		sumx2 += x*x
		sumx3 += x*x*x
		sumx4 += x*x*x*x
	xbar = sumx / n

	xbar2 = xbar * xbar
	xbar3 = xbar * xbar2
	xbar4 = xbar * xbar3
	numer =                 \
		sumx4               \
		- 4 * xbar  * sumx3 \
		+ 6 * xbar2 * sumx2 \
		- 4 * xbar3 * sumx  \
		+ n * xbar4
	denom =                       \
		sumx2 * sumx2             \
		+ 4 * xbar2 * sumx * sumx \
		+ n * n * xbar4           \
		+ 2 * n * xbar2 * sumx2   \
		- 4 * xbar * sumx * sumx2 \
		- 4 * n * xbar3 * sumx
	if denom == 0.0:
		return 0.0
	else:
		return 1.0 - (n * numer) / (3 * denom)

# ----------------------------------------------------------------
# Sample covariance of two lists.

def find_sample_covariance(xs, ys):
	N = len(xs)
	mean_x = find_mean(xs)
	mean_y = find_mean(ys)

	sum = 0.0
	for k in range(0, N):
		sum += (xs[k] - mean_x) * (ys[k] - mean_y)

	return sum / (N-1.0)

# ----------------------------------------------------------------
# Sample correlation of two lists:
# Corr(X,Y) = Cov(X,Y) / sigma_X sigma_Y.

def find_sample_correlation(xs, ys):
	N  = len(xs)
	cov = find_sample_covariance(xs, ys)
	mean_x   = find_mean(xs)
	mean_y   = find_mean(ys)
	stddev_x = find_stddev(xs, mean_x)
	stddev_y = find_stddev(ys, mean_y)
	return cov / (stddev_x * stddev_y)

# ----------------------------------------------------------------
def find_sample_tauint(xs, numk=0):
	N = len(xs)
	if numk == 0:
		numk = N
	tauint = [0.0] * numk
	autocorr = find_sample_autocorr(xs, numk)
	sum = 1.0
	tauint[0] = sum
	for t in range(1, numk):
		sum += 2 * autocorr[t]
		tauint[t] = sum
	return tauint

# ----------------------------------------------------------------
# Computing running sum of $\hat{\tau}_int(t)$.
# Stop after a flat spot has been found, detected via a turning point.
# Be clever about re-using previous sums.
#
# See my dissertation for details.  Or, Berg's Markov Chain Monte Carlo
# Simulations and Their Statistical Analysis.

def find_sample_tauint_flat_spot(xs):
	N = len(xs)
	minflat = 4

	# Within-window sums sumi, sumi2, sumj, and sumj2 contain terms which can
	# be re-used across k.  The cross-sums sumij are different for each k and
	# must be recomputed.
	#
	# Here, compute the full-window sums.
	sumi = 0.0; sumi2 = 0.0
	for k in range(0, N):
		x = xs[k]
		sumi  += x
		sumi2 += x*x
	sumj = sumi; sumj2 = sumi2

	tauint = 1.0
	nflat = 0
	# Go up only to t=N-2.  The autocorr estimator for t=N-1 doesn't work (only
	# one sample), and if we haven't found a flat spot of tauint by then, we
	# aren't going to.
	for t in range(1, N-1):
		winsz = N - t
		winszm1 = winsz - 1
		denom = winszm1
		if winszm1 == 0:
			denom = 1
		i = t; j = N-t-1

		# Update the within-window sums.
		xi  = xs[ i ];  xj  = xs[ j ]
		xim = xs[i-1];  xjp = xs[j+1]
		sumi -= xim; sumi2 -= xim*xim
		sumj -= xjp; sumj2 -= xjp*xjp

		# Compute the cross-sum.
		sumij = 0.0
		for k in range(0, winsz):
			sumij += xs[k] * xs[t+k]

		# Compute the autocorrelation term for this t.
		meani = sumi / winsz; meanj = sumj / winsz
		stdi  = math.sqrt((sumi2 - (sumi**2 / winsz)) / denom)
		stdj  = math.sqrt((sumj2 - (sumj**2 / winsz)) / denom)

		autocorr_t = 0.0
		if (stdi != 0.0) and (stdj != 0.0):
			autocorr_t = (sumij / winsz - (meani*meanj)) / (stdi*stdj)
		tauint += 2.0 * autocorr_t

		#print '%d %11.7f %11.7f' % (t, autocorr_t, tauint)
		if autocorr_t < 0.0:
			return tauint

	return tauint

# ----------------------------------------------------------------
# E[X_i X_j] - mu^2
# -----------------.
#     sigma^2

# More efficient autocorrelation:
#
# The cross-window sums must be computed for each k, because they differ for
# each k.  But the within-window sums may be accumulated, as long as we start
# with k at the end and work our way backward to the beginning.

# Example with N = 8:

# [ 0               ]         k = 7
# [ o               ]
# [               o ]
# [               7 ]

# [ 0 1             ]         k = 6
# [ o o             ]
# [             o o ]
# [             6 7 ]

# ...

# [ 0 1 2 3 4 5 6   ]         k = 1
# [ o o o o o o o   ]
# [   o o o o o o o ]
# [   1 2 3 4 5 6 7 ]

# [ 0 1 2 3 4 5 6 7 ]         k = 0
# [ o o o o o o o o ]
# [ o o o o o o o o ]
# [ 0 1 2 3 4 5 6 7 ]

# ----------------------------------------------------------------
# Pass numk=0 or numk=N to compute all possible autocorrelations.  Pass numk =
# something smaller to compute only the first numk autocorrelations.
def find_sample_autocorr(xs, numk=0):
	N  = len(xs)
	if numk == 0:
		numk = N
	autocorr = [0.0] * numk

	if (numk <= 1) or (numk > N):
		print >> sys.stderr, \
			"find_sample_autocorr: numk must be > 1 and <= N=%d; got %d." \
			% (N, numk)
		sys.exit(1)

	# Sums over first and second windows
	sumi  = 0.0; sumi2 = 0.0
	sumj  = 0.0; sumj2 = 0.0

	# k = N-1: accumulate sums, but set autocorr to zero.  Sample sizes
	# are 1; standard deviations would get a division by zero.
	i = 0; j = N-1
	for k in range(N-1, numk-1, -1):
		xi     = xs[i]; xj     = xs[j]
		sumi  += xi;    sumi2 += xi**2
		sumj  += xj;    sumj2 += xj**2
		i += 1; j -= 1

	# k = N-2 down to 1.
	for k in range(numk-1, 0, -1):
		xi     = xs[i]; xj     = xs[j]
		sumi  += xi;    sumi2 += xi**2
		sumj  += xj;    sumj2 += xj**2
		winsz   = N-k;  winszm1 = winsz - 1
		if k == N-1: # Leave autocorr[N-1] = 0.0 to avoid division by zero.
			i += 1; j -= 1
			continue

		sumij = 0.0
		for ell in range(0, winsz):
			sumij += xs[ell] * xs[ell+k]

		meani = sumi / winsz; meanj = sumj / winsz
		stdi  = math.sqrt((sumi2 - (sumi**2 / winsz)) / winszm1)
		stdj  = math.sqrt((sumj2 - (sumj**2 / winsz)) / winszm1)

		if (stdi == 0.0) or (stdj == 0.0):
			autocorr[k] = 0.0
		else:
			autocorr[k] = (sumij / winsz - (meani*meanj)) / (stdi*stdj)
		i += 1; j -= 1

	# k = 0: sumij, sumi2, and sumj2 are all the same.
	k       = 0
	winsz   = N; winszm1 = N-1
	xi      = xs[N-1]
	sumi   += xi
	sumi2  += xi**2
	meani   = sumi / N
	stdi    = math.sqrt((sumi2 - (sumi**2 / winsz)) / winszm1)

	autocorr[0]  = (sumi2 / N - (meani*meani)) / (stdi*stdi)

	return autocorr

## ----------------------------------------------------------------
#def find_sample_full_autocorr(xs):
#	N  = len(xs)
#	autocorr = [0.0] * N
#
#	# Sums over first and second windows
#	sumi  = 0.0; sumi2 = 0.0
#	sumj  = 0.0; sumj2 = 0.0
#
#	# k = N-1: accumulate sums, but set autocorr to zero.  Sample sizes
#	# are 1; standard deviations would get a division by zero.
#	i = 0; j = N-1
#	k = N-1
#	xi     = xs[i]; xj     = xs[j]
#	sumi  += xi;    sumi2 += xi**2
#	sumj  += xj;    sumj2 += xj**2
#	autocorr[k] = 0.0
#	i += 1; j -= 1
#
#	# k = N-2 down to 1.
#	for k in range(N-2, 0, -1):
#		xi     = xs[i]; xj     = xs[j]
#		sumi  += xi;    sumi2 += xi**2
#		sumj  += xj;    sumj2 += xj**2
#		winsz   = N-k;  winszm1 = winsz - 1
#
#		sumij = 0.0
#		for ell in range(0, winsz):
#			sumij += xs[ell] * xs[ell+k]
#
#		meani = sumi / winsz; meanj = sumj / winsz
#		stdi  = math.sqrt((sumi2 - (sumi**2 / winsz)) / winszm1)
#		stdj  = math.sqrt((sumj2 - (sumj**2 / winsz)) / winszm1)
#
#		autocorr[k] = (sumij / winsz - (meani*meanj)) / (stdi*stdj)
#		i += 1; j -= 1
#
#	# k = 0: sumij, sumi2, and sumj2 are all the same.
#	k       = 0
#	winsz   = N; winszm1 = N-1
#	xi      = xs[N-1]
#	sumi   += xi
#	sumi2  += xi**2
#	meani   = sumi / N
#	stdi    = math.sqrt((sumi2 - (sumi**2 / winsz)) / winszm1)
#
#	autocorr[0]  = (sumi2 / N - (meani*meani)) / (stdi*stdi)
#
#	return autocorr
#
## ----------------------------------------------------------------
#def find_sample_short_autocorr(xs, numk):
#	N  = len(xs)
#	autocorr = [0.0] * numk
#
#	if (numk <= 1) or (numk >= N):
#		print >> sys.stderr, \
#			"find_sample_short_autocorr: numk must be > 1 and < N=%d; got %d." \
#			% (N, numk)
#		sys.exit(1)
#
#	# Sums over first and second windows
#	sumi  = 0.0; sumi2 = 0.0
#	sumj  = 0.0; sumj2 = 0.0
#
#	# k = N-1: accumulate sums, but set autocorr to zero.  Sample sizes
#	# are 1; standard deviations would get a division by zero.
#	i = 0; j = N-1
#	for k in range(N-1, numk-1, -1):
#		xi     = xs[i]; xj     = xs[j]
#		sumi  += xi;    sumi2 += xi**2
#		sumj  += xj;    sumj2 += xj**2
#		i += 1; j -= 1
#
#	# k = N-2 down to 1.
#	for k in range(numk-1, 0, -1):
#		xi     = xs[i]; xj     = xs[j]
#		sumi  += xi;    sumi2 += xi**2
#		sumj  += xj;    sumj2 += xj**2
#		winsz   = N-k;  winszm1 = winsz - 1
#
#		sumij = 0.0
#		for ell in range(0, winsz):
#			sumij += xs[ell] * xs[ell+k]
#
#		meani = sumi / winsz; meanj = sumj / winsz
#		stdi  = math.sqrt((sumi2 - (sumi**2 / winsz)) / winszm1)
#		stdj  = math.sqrt((sumj2 - (sumj**2 / winsz)) / winszm1)
#
#		autocorr[k] = (sumij / winsz - (meani*meanj)) / (stdi*stdj)
#		i += 1; j -= 1
#
#	# k = 0: sumij, sumi2, and sumj2 are all the same.
#	k       = 0
#	winsz   = N; winszm1 = N-1
#	xi      = xs[N-1]
#	sumi   += xi
#	sumi2  += xi**2
#	meani   = sumi / N
#	stdi    = math.sqrt((sumi2 - (sumi**2 / winsz)) / winszm1)
#
#	autocorr[0]  = (sumi2 / N - (meani*meani)) / (stdi*stdi)
#
#	return autocorr

# ----------------------------------------------------------------
# E[X_i X_j] - mu^2
# -----------------.
#     sigma^2

# Example:
#
# N = 8,  k = 2
# 0 1 2 3 4 5
# o o o o o o
#     o o o o o o
#     2 3 4 5 6 7

def find_sample_autocorr_old1(xs):
	N  = len(xs)
	autocorr = [0.0] * N
	for k in range(0, N-1): # k = j-i

		window1 = xs[0:N-k]
		window2 = xs[k:N]
		mean1 = find_mean(window1)
		mean2 = find_mean(window2)
		std1  = find_stddev(window1, mean1)
		std2  = find_stddev(window2, mean2)

		cross_sum = 0.0
		for i in range(0, N-k):
			cross_sum += xs[i] * xs[i+k]
		cross_mean = cross_sum / (N-k)

		autocorr[k] = (cross_mean - mean1*mean2) / (std1 * std2)

	return autocorr

# ----------------------------------------------------------------
# Vector mean:  varray is a list of N vectors, each having n elements.  This
# could be done more elegantly using calls to sackmat_m's vecadd but it seems
# tighter performancewise this way.

def find_vector_mean(varray):
	N = len(varray)
	n = len(varray[0])
	sum = [0.0] * n
	for vector in varray:
		for j in range(0, n):
			sum[j] += vector[j]
	for j in range(0, n):
		sum[j] *= (1.0/N)
	return sum

# ----------------------------------------------------------------
# Vector standard deviation:  varray is a list of N vectors, each having n
# elements.  This could be done more elegantly using calls to sackmat routines
# but it seems tighter performancewise this way.

def find_vector_stddev(varray, vmean):
	N = len(varray)
	n = len(varray[0])
	sum = [0.0] * n
	for vector in varray:
		for j in range(0, n):
			sum[j] += (vector[j] - vmean[j])**2
	denom = 1.0 / (N-1)
	for j in range(0, n):
		sum[j] = math.sqrt(sum[j] * denom)
	return sum

# ----------------------------------------------------------------
# find_sample_covariance_matrix
# ----------------------------------------------------------------
#
# There are nx vectors x, each having dim elements.
# The sample covariance matrix Q is dim x dim with elements
#   q[i][j] = (1/(nx-1)) sum_{k=1}^nx (x[k][i] - mu[i])(x[k][j] - mu[j])
# where k indexes the set of x's and i,j index elements within the k'th vector.
# I.e. the ij'th entry of Q is the (scalar) sample covariance of xi and xj.
# In particular, the diagonal entries are the variances of the xi.

# Example:
# nx = 3 and dim = 2.
#
# x0 = [ 1 ]  x1 = [ 2 ]  x2 = [ 3 ]
#      [-4 ]       [-5 ]       [-6 ]
#
# mu = [ 2 ]
#      [-5 ]

# q[0][0] = (x[0][0] - mu[0]) * (x[0][0] - mu[0])
#         + (x[1][0] - mu[0]) * (x[1][0] - mu[0])
#         + (x[2][0] - mu[0]) * (x[2][0] - mu[0])
#
#         = ( 1 - 2) * ( 1 - 2)
#         + ( 2 - 2) * ( 2 - 2)
#         + ( 3 - 2) * ( 3 - 2)
#
#         = 1 + 0 + 1 =  2

# q[0][1] = (x[0][0] - mu[0]) * (x[0][1] - mu[1])
#         + (x[1][0] - mu[0]) * (x[1][1] - mu[1])
#         + (x[2][0] - mu[0]) * (x[2][1] - mu[1])
#
#         = ( 1 - 2) * (-4 + 5)
#         + ( 2 - 2) * (-5 + 5)
#         + ( 3 - 2) * (-6 + 5)
#
#         =-1 + 0 - 1 = -2

# q[1][0] = (x[0][1] - mu[1]) * (x[0][0] - mu[0])
#         + (x[1][1] - mu[1]) * (x[1][0] - mu[0])
#         + (x[2][1] - mu[1]) * (x[2][0] - mu[0])
#
#         = (-4 + 5) * ( 1 - 2)
#         + (-5 + 5) * ( 2 - 2)
#         + (-6 + 5) * ( 3 - 2)
#
#         =-1 + 0 - 1 = -2

# q[1][1] = (x[0][1] - mu[1]) * (x[0][1] - mu[1])
#         + (x[1][1] - mu[1]) * (x[1][1] - mu[1])
#         + (x[2][1] - mu[1]) * (x[2][1] - mu[1])
#
#         = (-4 + 5) * (-4 + 5)
#         + (-5 + 5) * (-5 + 5)
#         + (-6 + 5) * (-6 + 5)
#
#         = 1 + 0 + 1 =  2

# Q = [ 2 -2 ] * (1/2)
#     [-2  2 ]
#
#   = [ 1 -1 ]
#     [-1  1 ]

def find_sample_covariance_matrix(xs):
	nx   = len(xs)
	dim  = len(xs[0])
	mean = find_vector_mean(xs)
	Q  = sackmat_m.make_zero_matrix(dim, dim)

	for i in range(0, dim):
		for j in range(0, dim):
			sum = 0.0

			for k in range(0, nx):
				sum += (xs[k][i] - mean[i]) * (xs[k][j] - mean[j])

			Q[i][j] = sum / (nx-1.0)
	return Q

# ----------------------------------------------------------------
# Corr(X,Y)   = Cov(X,Y)   / sigma_X  sigma_Y
# Corr(Xi,Xj) = Cov(Xi,Xj) / sigma_Xi sigma_Xj
# The ijth entry of the correlation matrix is the correlation of Xi and Xj.

def find_sample_correlation_matrix(xs):
	nx  = len(xs)
	dim = len(xs[0])
	cov = find_sample_covariance_matrix(xs)
	vmean = find_vector_mean(xs)
	vstddev = find_vector_stddev(xs, vmean)
	for i in range(0, dim):
		for j in range(0, dim):
			cov[i][j] /= vstddev[i] * vstddev[j]
	return cov

# ----------------------------------------------------------------
# Univariate linear regression
# ----------------------------------------------------------------
# There are N (xi, yi) pairs.
#
# E = sum (yi - m xi - b)^2
#
# DE/Dm = sum 2 (yi - m xi - b) (-xi) = 0
# DE/Db = sum 2 (yi - m xi - b) (-1)  = 0
#
# sum (yi - m xi - b) (xi) = 0
# sum (yi - m xi - b)      = 0
#
# sum (xi yi - m xi^2 - b xi) = 0
# sum (yi - m xi - b)         = 0
#
# m sum(xi^2) + b sum(xi) = sum(xi yi)
# m sum(xi)   + b N       = sum(yi)
#
# [ sum(xi^2)   sum(xi) ] [ m ] = [ sum(xi yi) ]
# [ sum(xi)     N       ] [ b ] = [ sum(yi)    ]
#
# [ m ] = [ sum(xi^2) sum(xi) ]^-1  [ sum(xi yi) ]
# [ b ]   [ sum(xi)   N       ]     [ sum(yi)    ]
#
#       = [ N         -sum(xi)  ]  [ sum(xi yi) ] * 1/D
#         [ -sum(xi)   sum(xi^2)]  [ sum(yi)    ]
#
# where
#
#   D = N sum(xi^2) - sum(xi)^2.
#
# So
#
#      N sum(xi yi) - sum(xi) sum(yi)
# m = --------------------------------
#                   D
#
#      -sum(xi)sum(xi yi) + sum(xi^2) sum(yi)
# b = ----------------------------------------
#                   D

def linear_regression(xs, ys):
	sumxi   = 0.0
	sumyi   = 0.0
	sumxiyi = 0.0
	sumxi2  = 0.0

	N = len(xs)
	for i in range(0, N):
		x = xs[i]
		y = ys[i]
		sumxi   += x
		sumyi   += y
		sumxiyi += x*y
		sumxi2  += x*x

	D =  N * sumxi2 - sumxi**2
	m = (N * sumxiyi - sumxi * sumyi) / D
	b = (-sumxi * sumxiyi + sumxi2 * sumyi) / D

	# Young 1962, pp. 122-124.  Compute sample variance of linear
	# approximations, then variances of m and b.
	var_z = 0.0
	for i in range(0, N):
		var_z += (m * xs[i] + b - ys[i])**2
	var_z /= N

	var_m = (N * var_z) / D
	var_b = (var_z * sumxi2) / D

	return [m, b, math.sqrt(var_m), math.sqrt(var_b)]

# ----------------------------------------------------------------
def get_corr_coeff(xs, ys):
	sumxi   = 0.0
	sumyi   = 0.0
	sumxiyi = 0.0
	sumxi2  = 0.0
	sumyi2  = 0.0

	N = len(xs)
	for i in range(0, N):
		x = xs[i]
		y = ys[i]
		sumxi   += x
		sumyi   += y
		sumxiyi += x*y
		sumxi2  += x*x
		sumyi2  += y*y

	# Young 1962, p. 130.
	a = N*sumxiyi - sumxi*sumyi
	b = N*sumxi2  - sumxi**2
	c = N*sumyi2  - sumyi**2
	corr_coeff = a / math.sqrt(b*c)
	return corr_coeff

# ----------------------------------------------------------------
def zscore(x):
	return normal_m.invnorm(x)

# ----------------------------------------------------------------
def get_normal_quantiles_zs(xarray):
	# Assume inputs are sorted?
	n = len(xarray)
	zarray = []
	for i in range(0, n):
		z = zscore((1.0*(i+0.5))/n)
		zarray.append(z)
	return zarray

# ----------------------------------------------------------------
def print_normal_quantiles_zx(xarray):
	xs = copy.copy(xarray)
	xs.sort()
	zs = get_normal_quantiles_zs(xs)
	n = len(xs)
	for i in range(0, n):
		print zs[i], xs[i]

# ----------------------------------------------------------------
# Suppose x_1, ..., x_N are IID samples of a random variable X.
# The kernel density approximator of the PDF of X, with bandwidth parameter
# h, is the function
#
#   KDA(x) = (1/Nh) sum K((x-x_i)/h)
#
# where the kernel K may be taken to be the PDF of the standard normal.

def kernel_density_estimator(x, xarray, h):
	N = len(xarray)
	sum = 0.0
	for xi in xarray:
		sum += normal_m.normalpdf((x-xi)/h)
	return sum/N/h

def plot_kde(xarray, h, xlo, xhi, nx):
	dx = (xhi - xlo) / (1.0*nx)
	for i in range(0, nx+1):
		x = xlo + i*dx
		y = kernel_density_estimator(x, xarray, h)
		print x, y

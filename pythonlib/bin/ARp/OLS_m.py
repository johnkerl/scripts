#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# http://en.wikipedia.org/wiki/Ordinary_least_squares
# 2010-11-22
# kerl.john.r@gmail.com
# ================================================================

# ----------------------------------------------------------------
# i=1,..,n samples
# y_i = x_i . beta + eps_i
# each x_i is a k-dimensional regressor
# beta is a k-dimensional coefficient vector
# residual terms e_i

# y = X beta + eps

# OLS estimator of beta: beta_hat = (X^t X)^-1 X^t y
# covariance matrix of beta_hat is (X^t X)^-1 (X^t V X) (X^t X)^-1
# (assume the residuals have zero mean)
# where V is the covariance matrix of the eps_i's

# Note X^t X is k x k with (i,j) entry being ith column dot with jth column.

# ----------------------------------------------------------------
from __future__ import division # 1/2 = 0.5, not 0.
from math import sqrt
import sys
import tabutil_m, sackmat_m, stats_m

# 1. read the x vectors & the y vector
argc = len(sys.argv)
if argc == 1:
	columns = tabutil_m.float_columns_from_file('-')
	y = columns[0]
	xs = columns[1:]
elif argc == 2:
	columns = tabutil_m.float_columns_from_file(sys.argv[1])
	y = columns[0]
	xs = columns[1:]
elif argc == 3:
	[y] = tabutil_m.float_columns_from_file(sys.argv[1])
	xs = tabutil_m.float_columns_from_file(sys.argv[2])
else:
	print >> sys.stderr, "Usage: %s {y and xs file name}" % (sys.argv[0])
	print >> sys.stderr, "Or: %s {xs file name} {y file name}" % (sys.argv[0])
	sys.exit(1)

# 2. compute XtX
k = len(xs)
n = len(y)
XtX = sackmat_m.make_zero_matrix(k, k)
for i in range(0, k):
	xi = xs[i]
	for j in range(i, k):
		xj = xs[j]
		xi_dot_xj = sackmat_m.vecdot(xi, xj)
		XtX[i][j] = xi_dot_xj
		if i != j:
			XtX[j][i] = xi_dot_xj

# 3. commpute XxT.inv
XtXi = XtX.inv()
# xxx handle singular ...

# 4. commpute XtX.inv Xt y
Xt = sackmat_m.sackmat(xs)
X  = Xt.transpose()
beta_hat = XtXi * Xt * y

print 'beta_hat: '
print beta_hat
print

# 5. Estimate eps
X_beta_hat = X * beta_hat
eps_hat = sackmat_m.vecsub(y, X_beta_hat)
#print 'eps_hat '
#print eps_hat
#print

# 6. Estimate V
sigma = sqrt(sackmat_m.vecdot(eps_hat, eps_hat) / (n-k))
print 'sigma: '
print sigma
print

# 7. Estimate the covariance matrix of beta.
cov_beta_hat = XtXi * sigma**2
print 'cov beta hat:'
print cov_beta_hat
print
# covariance matrix of beta_hat is (X^t X)^-1 (X^t V X) (X^t X)^-1

# 8. Print the t-statistic
# xxx Q = E[X Xt ] .... ?
# xxx sigma_j_hat = sqrt(sigma**2/n [Q^-1]_{jj})
# xxx t_stat = sackmat_m.vecdiv(beta_hat,  sigma_js)
print 't-statistic:'
print t_stat
print

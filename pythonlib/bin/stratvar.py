#!/usr/bin/python -Wall

# ================================================================
# An example of stratified random sampling.
# John Kerl
# kerl.john.r@gmail.com
# 2008-01-25
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
import random
import stats_m
import sackmat_m

# ----------------------------------------------------------------
def set_up_normal_strata(true_mu, true_sigma, Nis):
	strata = []
	k = len(Nis)
	for i in range(0, k):
		Ni = Nis[i]
		stratum = [0.0] * Ni
		for j in range(0, Ni):
			stratum[j] = random.normalvariate(true_mu, true_sigma)
		strata.append(stratum)
	return strata

# ----------------------------------------------------------------
def sumup(list):
	sum = 0.0
	for elt in list:
		sum += elt
	return sum

# ----------------------------------------------------------------
def flatten(list):
	rv = []
	for sublist in list:
		rv = rv + sublist
	return rv

# ----------------------------------------------------------------
def random_sample_with_replacement(population, sample_size):
	N = len(population)
	n = sample_size
	sample = []
	for i in range(0, n):
		sample.append(random.choice(population))
	return sample

# ----------------------------------------------------------------
def set_up_test_strata():
	return [[5, 9], [1, 2, 3]]

# ================================================================
# Generate the data
#strata = set_up_test_strata()

true_mu    = 2.0
true_sigma = 3.0
Nis  = [1000, 2000, 3000]
nis  = [ 100,  200,  300]
num_sample_reps = 1000
strata = set_up_normal_strata(true_mu, true_sigma, Nis)

# Compute population size and number of strata.
population = flatten(strata)
Nis = map(len, strata)
N = sumup(Nis)
k = len(Nis)

# Compute stratum weights
wis = [0.0] * k
for i in range(0, k):
	wis[i] = (1.0 * Nis[i]) / N

# Compute sample size n = sum_{i=1}^k w[i]*n[i]
n = 0
for i in range(0, k):
	n += wis[i] * nis[i]
n = int(n)

# Compute the simple and stratified means
mis = map(stats_m.find_mean, strata)
m = stats_m.find_mean(population)

# Compute the simple and stratified variances
vis = [0.0] * k
for i in range(0, k):
	vis[i] = stats_m.find_popvaraux(strata[i], mis[i])
v = stats_m.find_popvaraux(population, m)

# ----------------------------------------------------------------
if (1):
	print "N = %6d k = %6d m = %7.4f  v = %7.4f" % (N, k, m, v)

	if (N < 20):
		print
		for i in range(0, k):
			print "Stratum", i+1, " = ", strata[i]
		print

	for i in range(0, k):
		print "N_%d = %7d  w_%d = %7.4f  m_%d = %7.4f  v_%d = %7.4f" % \
			(i+1, Nis[i], i+1, wis[i], i+1, mis[i], i+1, vis[i])

	print

# ----------------------------------------------------------------
# v = sum_{i=1}^k w_i*v_i + sum_{i=1}^k w_i (m_i - m)^2.

if (0):

	print "----------------------------------------------------------------"

	term1 = 0.0
	for i in range(0, k):
		term1 += wis[i] * vis[i]

	term2 = 0.0
	for i in range(0, k):
		term2 += wis[i] * (mis[i] - m)**2

	RHS = term1 + term2
	LHS = v
	print "LHS =", LHS, "RHS =", RHS
	print

# ----------------------------------------------------------------
# Compute Xbar = sample mean and Ybar = sum_{i=1}^k w[i]*Xibar
# (i.e. weighted sum of stratified sample means).
# Expect E[(Ybar-m)^2] <= E[(Xbar-m)^2], with equality when m_i's are all equal.

Xbars = []
Ybars = []
for rep in range(0, num_sample_reps):
	X = random_sample_with_replacement(population, n)
	Xbar = stats_m.find_mean(X)
	Xbars.append(Xbar)

	Ybar = 0.0
	for i in range(0, k):
		stratum = strata[i]
		ni = nis[i]
		wi = wis[i]

		Xi = random_sample_with_replacement(stratum, ni)
		Xibar = stats_m.find_mean(Xi)
		Ybar += wi * Xibar
	Ybars.append(Ybar)

EXbar = stats_m.find_mean(Xbars)
EYbar = stats_m.find_mean(Ybars)
VXbar = stats_m.find_sampvaraux(Xbars, true_mu)
VYbar = stats_m.find_sampvaraux(Ybars, true_mu)

print "n   = %7d" % (n)
for i in range(0, k):
	print "n_%d = %7d" % (i, nis[i])
print
print "E[Xbar] = %7.4f" % (EXbar)
print "E[Ybar] = %7.4f" % (EYbar)
print "E[(Xbar-m)^2] = %7.4f" % (VXbar)
print "E[(Ybar-m)^2] = %7.4f" % (VYbar)

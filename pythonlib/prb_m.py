#!/usr/bin/python -Wall

# ================================================================
# Some Markov-chain hackwork.
# John Kerl
# kerl.john.r@gmail.com
# 2007-07-09
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
import sackmat_m
import random
import copy
import sys
import pmtc_tm

# ----------------------------------------------------------------
# Scales the vector so its row sum is 1.
def row_normalize_vector(v):
	sum = sackmat_m.vec_contract(v)
	if (sum == 0.0):
		return
	n = len(v)
	for i in range(0, n):
		v[i] /= sum

# ----------------------------------------------------------------
# Scales each row of the matrix so the row sums are 1.
def row_normalize_matrix(A):
	[nr, nc] = A.dims()
	for i in range(0, nr):
		row_normalize_vector(A[i])

# ----------------------------------------------------------------
# Use the metric induced by the max norm.
def are_close(A, B, tol = 1e-4):
	# Assume same dims
	n = A.square_dim()
	for i in range(0, n):
		for j in range(0, n):
			d = abs(A[i][j] - B[i][j])
			if (d > tol):
				return [0, d]
	return [1, tol]

# ----------------------------------------------------------------
# Iterates the chain, looking for stability.
def is_stable(A, verbose=0):
	Ap = copy.copy(A)

	#maxits = 20
	maxits = 1000
	k = 0
	while (k < maxits):
		Ao = Ap
		Ap = Ap * A

		[yn, err] = are_close(Ao, Ap)

		if (verbose):
			print "-- k = %d err = %.4e" % (k, err)
			Ap.printf()
			print ""

		if (yn == 1):
			return [1, Ap]
		k += 1
	return [0, Ap]

# ----------------------------------------------------------------
# Let q = 1-p.

# p q 0 0 0 0
# 0 p q 0 0 0
# 0 0 p q 0 0
# 0 0 0 p q 0
# 0 0 0 0 p q
# q 0 0 0 0 p

def circpmat1(n, p):
	A = sackmat_m.make_zero_matrix(n, n)
	for i in range(0, n):
		A[i][i] = p
		A[i][(i+1)%n] = 1-p
	return A

# ----------------------------------------------------------------
# Let q = 1-p.

# 0 q 0 0 0 p
# p 0 q 0 0 0
# 0 p 0 q 0 0
# 0 0 p 0 q 0
# 0 0 0 p 0 q
# q 0 0 0 p 0

def circpmat2(n, p):
	A = sackmat_m.make_zero_matrix(n, n)
	for i in range(0, n):
		A[i][(i-1)%n] = p
		A[i][(i+1)%n] = 1-p
	return A

# ----------------------------------------------------------------
# Assign matrix elements using uniform distribution on [0, 1), then
# normalize rows.
def randprbmat(n):
	A = sackmat_m.make_zero_matrix(n, n)
	for i in range(0, n):
		for j in range(0, n):
			A[i][j] = random.random()
	row_normalize_matrix(A)
	return A

# ----------------------------------------------------------------
def pqmat(p, q):
	return sackmat_m.sackmat([[p, 1-p],[1-q, q]])

# ================================================================
#A = randprbmat(6,6)
#A = pmtc_tm.from_cycles([[1,2],[3,4,5]],5).to_permutation_matrix()
#A = circpmat1(6, .5)
#A = circpmat2(6, .1)

p = 0.9
q = 0.8
if (len(sys.argv) == 3):
	p=float(sys.argv[1])
	q=float(sys.argv[2])
A=pqmat(p, q)

print "A:"
A.printf()
print ""

#sys.exit(0)

[yn, As] = is_stable(A, 1)
if (yn == 1):
	print "stable"
	As.printf()
else:
	print "unstable"
	As.printf()

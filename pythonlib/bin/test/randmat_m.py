#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2007-01-12
# ================================================================

import sys
import random
import math
from sackmat_m import *

#import copy
#import re
#import math
#import array # For binary I/O
#import types

# ----------------------------------------------------------------
# The random module's distribution is [0,1].  Or [0,1) ... .  Scale to [-1, 1].
# Maybe use a different (in particular, non-uniform) distribution?

def randscalar():
	lo    = -4.0
	range =  8.0 # -10 to 10.
	return lo + random.random() * range

# ----------------------------------------------------------------
def randmat(m, n):
	A = make_zero_matrix(m, n)
	for i in range(0, m):
		for j in range(0, n):
			A[i][j] = randscalar()
	return A

# ----------------------------------------------------------------
def randsqmat(n):
	return randmat(n, n)

# ----------------------------------------------------------------
def randgl(n):
	tol = 1e-10
	k = 1
	while (1):
		A = randmat(n, n)
		d = A.det()
		if (abs(d) >= tol):
			break
	return A

# ----------------------------------------------------------------
def randsl(n):
	A = randgl(n)
	d = A.det()
	absd = abs(d)
	absdroot = absd ** (1.0/n)
	for i in range(0, n):
		for j in range(0, n):
			A[i][j] /= absdroot
	if (d < 0.0):
		for j in range(0, n):
			A[0][j] = -A[0][j] 
	return A

# ----------------------------------------------------------------
def rando(n):
	A = randmat(n, n)
	A = gram_schmidt(A)
	return A

# ----------------------------------------------------------------
def randso(n):
	A = rando(n)
	d = A.det()
	if (d < 0.0):
		for j in range(0, n):
			A[0][j] = -A[0][j] 
	return A

# ----------------------------------------------------------------
def randsymm(n):
	A = randmat(n, n)
	A = A + A.transpose()
	return A

# ----------------------------------------------------------------
def randsksymm(n):
	A = randmat(n, n)
	A = A - A.transpose()
	return A


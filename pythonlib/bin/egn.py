#!/usr/bin/python -Wall

# ----------------------------------------------------------------
def power_set(Omega):
	return power_set_sort(raw_power_set(Omega))

# ----------------------------------------------------------------
# Easy to compute, but unnaturally ordered.
def raw_power_set(Omega):
	n = len(Omega)
	N = 1 << n
	P = []
	for k in range(0, N):
		subset = []
		for j in range(0, n):
			if (k & (1 << j)):
				subset.append(Omega[j])
		P.append(subset)
	return P

# ----------------------------------------------------------------
# Easy to compute, but unnaturally ordered.
def power_set_sort(P):
	P.sort(power_set_cmp)
	return P

# First sort by length, then lexically
def power_set_cmp(a, b):
	la = len(a)
	lb = len(b)
	if (la < lb): return -1
	if (la > lb): return  1
	if (la == 0): return 0
	for i in range(0, la):
		if (a[i] < b[i]): return -1
		if (a[i] > b[i]): return  1
	return 0

# ----------------------------------------------------------------
# Computes P(X=x) = P(X^-1(x)).
def PXx(X, x, P):
	n = len(X)
	sum = 0.0
	for i in range(0, n):
		if (X[i] == x):
			sum += P[i]
	return sum

# ----------------------------------------------------------------
# Computes X^-1(x).
def Xinv(X, x, Omega):
	n = len(X)
	rv = []
	for i in range(0, n):
		omega = Omega[i]
		if (X[i] == x):
			rv.append(omega)
	return rv

# ----------------------------------------------------------------
def E(X, P):
	sum = 0.0
	n = len(X)
	for i in range(0, n):
		sum += X[i] * P[i]
	return sum

# ----------------------------------------------------------------
# E[X;G] = E[X 1_G]
def E_semicolon(X, G, Omega, P):
	sum = 0.0
	n = len(X)
	for i in range(0, n):
		omega = Omega[i]
		x     = X[i]
		if (omega in G):
			sum += x * P[i]
	return sum

# ----------------------------------------------------------------
# E[X|G] =   sum_x  x P(X=x|G)
# =   sum_x  x P(X=x, G) / P(G)
# = (1/P(G))  sum_x  x P(X=x, G)
# = (1/P(G))  sum_x  x sum_{omega in X^-1(x) \cap G} P({omega})
# = (1/P(G))  sum_x  x sum_{omega: omega in G and X(omega) = x} P(omega)

def E_given(X, G, Omega, P):
	sum = 0.0
	PG  = 0.0
	n   = len(X)

	for i in range(0, n):
		omega = Omega[i]
		if (omega in G):
			PG += P[i]
	if (PG == 0.0):
		return 0.0

	for i in range(0, n):
		x     = X[i]

		# Don't overcount
		if x in X[:i]:
			continue

		for j in range(0, n):
			omega = Omega[j]
			if (omega in G and X[j] == x):
				sum += x * P[j]
		print
	return sum / PG

# ----------------------------------------------------------------
def report_on_subset(Omega, P, X, G):
	print "----------------------------------------------------------------"
	print "Omega:", Omega
	print "G:", G
	print "X:", X

	EX = E(X, P)
	E_X_semicolon_G = E_semicolon(X, G, Omega, P)
	E_X_given_G = E_given(X, G, Omega, P)

	print "EX=", EX
	print "E[X|G]", E_X_given_G
	print "E[X;G]", E_X_semicolon_G
	print

# ================================================================
Omega = ["a",  "b",  "c",  "d"]
P     = [0.25, 0.25, 0.25, 0.25]
X     = [2,    3,    2,    3]
Y     = [6,    7,    8,    9]

mcF = power_set(Omega)
mcG = [[], [1], [2,3,4], [1,2,3,4]]

if (0):
	print "2^Omega:"
	for S in mcF:
		print S
	print

if (0):
	print "P:", P

if (0):
	print "X:", X

if (0):
	print "Y:", Y

if (0):
	print "P(X=1) = ", PXx(X, 1, P)
	print "P(X=2) = ", PXx(X, 2, P)
	print "P(X=3) = ", PXx(X, 3, P)
	print "P(X=4) = ", PXx(X, 4, P)
	print
	print "P(Y=1) = ", PXx(Y, 1, P)
	print "P(Y=2) = ", PXx(Y, 2, P)
	print "P(Y=3) = ", PXx(Y, 3, P)
	print "P(Y=4) = ", PXx(Y, 4, P)
	print

if (0):
	X1inv = Xinv(X, 1, Omega)
	X2inv = Xinv(X, 2, Omega)
	X3inv = Xinv(X, 3, Omega)
	print "X^-1(1)=", X1inv
	print "X^-1(2)=", X2inv
	print "X^-1(3)=", X3inv
	print

if (1):
	#G = ["a", "b"]; report_on_subset(Omega, P, X, G)
	#G = ["a", "c"]; report_on_subset(Omega, P, X, G)
	for G in mcF:
		print "================================================================"
		report_on_subset(Omega, P, X, G)
		

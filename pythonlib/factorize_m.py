#!/usr/bin/perl -Wall

# John Kerl
# kerl.john.r@gmail.com
# 2008-09-14

from math import *

# ----------------------------------------------------------------
def factorize(n):
	factors = []

	if (n == 0):
		return []
	if (n < 0):
		factors = [-1]
		n = -n

	i = 2
	while (n > 1):
		power = 0;
		while ((n % i) == 0):
			power += 1
			n /= i
		if (power > 0):
			factors.append([i, power])
		i += 1
	return factors

# ----------------------------------------------------------------
def isprime(n):
	top = int(sqrt(n))
	if (n < 0):
		n = -n
	if (n < 2):
		return 0
	if (n == 2):
		return 1
	if (n % 2) == 0:
		return 0
	for d in range(3, top+1, 2):
		if (n % d) == 0:
			if (n != d):
				return 0
	return 1

# ----------------------------------------------------------------
def issquarefree(n):
	if (n == 0):
		return 1
	if (n < 0):
		n = -n

	i = 2
	while (n > 1):
		power = 0;
		while ((n % i) == 0):
			power += 1
			n /= i
		if (power > 1):
			return 0
		i += 1
	return 1

# ================================================================
nsqf=0
top=100000
for n in range(0, top):
	#print n, isprime(n)
	if (issquarefree(n)):
		nsqf += 1
print nsqf, top

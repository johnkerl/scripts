#!/usr/bin/python -Wall -Qnew

# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

# ----------------------------------------------------------------
def isprime_trial(n):
	if (n < 0):
		n = -n

	if (n <= 1):
		return 0
	elif (n <= 3):
		return 1
	elif ((n & 1) == 0):
		return 0

	d = 3
	q = n
	while (d <= q):
		q = int(n / d)
		if (n == (q * d)):
			return 0
		d += 2

	return 1

# ----------------------------------------------------------------
def isprime(n):
	return isprime_trial(n)
	#return isprime_table(n)

#// ----------------------------------------------------------------
#int isprime_table(int n)
#{
#	int i
#	unsigned un
#
#	if (n == -n)
#		return 0
#	elif (n < 0)
#		n = -n
#
#	if (n <= 1)
#		return 0
#
#	un = (unsigned) n
#	for (i = 0 i < numprimes16 i++) {
#		if ((un % primes16[i]) == 0) {
#			if (un == primes16[i])
#				return 1
#			else
#				return 0
#		}
#		if (primes16[i] * primes16[i] > un)
#			return 1
#	}
#	return 1
#}
#
#// ----------------------------------------------------------------
#int isprime(int n)
#{
#	//return isprime_trial(n)
#	return isprime_table(n)
#}
#
#
#================================================================
#
##!/usr/bin/python
#
#import sys
#
## ----------------------------------------------------------------
#def usage():
#	print >> sys.stderr, "Usage: {numbers}"
#	print >> sys.stderr, "Performs the Fermat primality test by computing a^{p-1} mod p for several small a."
#	sys.exit(1)
#
## ----------------------------------------------------------------
#def mod_power(b, e, m):
#	b2 = b % m
#	rv = 1
#
#	while (e != 0):
#		if (e & 1):
#			rv = (rv * b2) % m
#		e = e >> 1
#		b2 = (b2 * b2) % m
#	return rv
#
## ----------------------------------------------------------------
#def test_one_base(a, p):
#	x = mod_power(a, p-1, p)
#	print "%d ^ %d = %d (mod %d)" % (a, p-1, x, p)
#	if ((x != 1) and (p != a)):
#		return 0
#	return 1
#
## ----------------------------------------------------------------
#def fermat_test(p):
#	rv = 1
#	for a in [2, 3, 5, 7, 11, 13, 17, 19]:
#		if (not test_one_base(a, p)):
#			rv = 0
#			return rv
#	return rv
#
## ----------------------------------------------------------------
#argc = len(sys.argv)
#if (argc < 2):
#	usage()
#
#for argi in range(1, argc):
#	p = int(sys.argv[argi])
#	if (fermat_test(p)):
#		print p, "might be prime."
#	else:
#		print p, "is not prime."
#	print

## ----------------------------------------------------------------
#def foo():
#	for n in range(0, 40):
#		ip = isprime_trial(n)
#		print n, ip
#foo()

# ----------------------------------------------------------------
def int_factor(n):
	rv = []
	if (n == 0):
		return [n]
	if (n < 0):
		return [-1] + int_factor(-n)
	if (n == 1):
		return [1]

	# This is a painfully naive implementation.  However it works fine
	# for small numbers.
	d = 2
	while (n > 1):
		while ((n % d) == 0):
			rv.append(d)
			n = int(n/d)
		d += 1
	return rv

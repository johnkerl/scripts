#!/usr/bin/python -Wall

# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

def fact(n):
	if (n < 0):
		return 0
	rv = 1
	while (n > 0):
		rv *= n
		n -= 1
	return rv

def binc(n, k):
	if (k > n):
		return 0
	if (k < 0):
		return 0
	if (k > int(n/2)):
		k = n - k

	rv = 1
	for j in range(0, k):
		rv *= n - j
		rv /= j + 1
	return rv


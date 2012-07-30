#!/usr/bin/python -Wall

# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

import re
import copy # xxx temp

# The Clifford group with (hard-coded) Simon's quadratic form.
# See Simon's text.
#
# alpha eA beta eB = alpha beta chi(A, B) e{A xor B}.
# A and B are multi-indices; alpha and beta are signs.
#
# Explanation of chi(A, B) is by example:
#
# * a = e2 e3 e6 e7; b = e1 e3 e5 e6.
# * a*b = e2 e3 e6 e7 | e1 e3 e5 e6.  Then sort:
# - Move e1 left: e1 e2 e3 e6 e7|e3 e5 e6, passing a's e2, e3, e6, e7.
# - move e3 left: e1 e2 e3 e3 e6 e7|e5 e6, passing a's e6 and e7.
# - Move e5 left: e1 e2 e3 e3 e5 e6 e7|e6, passing a's e6 and e7.
# - Move e5 left: e1 e2 e3 e3 e5 e6 e6 e7, passing a's e7.
#
# If sqsign == -1, then ei*ei = -1, else ei*ei = +1.
# One can imagine implementing more general quadratic forms: not yet. :)

class cl2_t:

	def __init__(self, sign, bits, n, sqsign):
		self.sign   = sign
		self.bits   = bits & ((1 << n) - 1)
		self.n      = n
		self.sqsign = sqsign

	def __mul__(a,b):
		c = cl2_t(a.sign * b.sign, a.bits ^ b.bits, a.n, a.sqsign)
		for j in range(0, b.n):
			if ((b.bits >> j) & 1):
				# Count the number of times to move this element of b left
				# past elements of a.
				#
				# If sqsign == -1, then ei*ei = -1, else ei*ei = +1.
				lolim = j+1
				if (a.sqsign == -1):
					lolim = j
				for i in range(lolim, a.n):
					if ((a.bits >> i) & 1):
						c.sign *= -1
		return c

	def __eq__(a,b):
		return (a.sign == b.sign and a.bits == b.bits and a.n == b.n and a.sqsign == b.sqsign)

	def __ne__(a,b):
		return not (a == b)

	def __lt__(a,b):
		if (a.bits < b.bits):
			return 1
		return a.sign > b.sign
	def __le__(a,b):
		if (a.bits <= b.bits):
			return 1
		return a.sign >= b.sign
	def __gt__(a,b):
		if (a.bits > b.bits):
			return 1
		return a.sign < b.sign
	def __ge__(a,b):
		if (a.bits >= b.bits):
			return 1
		return a.sign <= b.sign

	def inv(a):
		c = copy.copy(a)
		return c

	def scan(self, string):
		if (1):
			self.__init__(1, 0, 4) # stub
		else:
			raise IOError

	def __str__(self):
		rv = "+"
		if (self.sign < 0):
			rv = "-"
		for i in range(0, self.n):
			rv += str((self.bits >> i) & 1)
		return rv

	def __repr__(self):
		return self.__str__()

def params_from_string(params_string):
	n = 0
	sqsign = 1
	fields = re.split(',', params_string)
	ok = 1

	if (len(fields) == 2):
		n = int(fields[0])
		if   (fields[1] == "+"):
			sqsign =  1
		elif (fields[1] == "+1"):
			sqsign =  1
		elif (fields[1] == "1"):
			sqsign =  1
		elif (fields[1] == "-"):
			sqsign = -1
		elif (fields[1] == "-1"):
			sqsign = -1
		else:
			ok = 0
	else:
		ok = 0

	if (not ok):
		print "cl2_tm.from_string:  expected parameters n,sign."
		print "Got: ", params_string
		raise IOError
	return [n, sqsign]


def from_string(value_string, params_string):
	[n, sqsign] = params_from_string(params_string)
	obj = cl2_t(1, 0, n, sqsign)
	obj.scan(value_string)
	return obj

## xxx temp
#a = cl2_t(1, 0x66, 8)
#b = cl2_t(1, 0x35, 8)
#c = a * b

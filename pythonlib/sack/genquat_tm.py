#!/usr/bin/python -Wall

# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

# Presentation:
# < a, b | a^2n = 1, b^2 = a^n, ab = ba^-1 >
#
# Expressions simplify to a^i b^j for i=0,1,..,n-1 and j=0,1,2,3:
# * Powers on a don't exceed 2n.
# * Powers on b don't exceed 4.
# * Powers on a of n .. 2n-1 may have have a^n replaced with b^2.
# * The quasi-commutator ab=ba^-1 leads to ba = a^-1b which allows
#   all powers of a, and all powers of b, to be collected together.
#
# That is:
# * ba = a^-1 b
# * b a^i = a^-i b
# * b^j a = a^s b^j  where s = (-1)^j
#
# Thus
#   b^j a^i = b^j-1 b a^i
#           = b^j-2 a^i  b^2
#           = b^j-3 a^-i b^3
#           = b^j-4 a^i  b^4
#           = ...
#           = a^i   b^j  if  j even
#           = a^-i  b^j  if  j odd
#           = a^si  b^j  where s = (-1)^j
#
# Thus
#   a^i b^j a^k b^l = a^i (b^j a^k) b^l
#                   = a^i (a^sk b^j) b^l
#                   = a^(i+sk) b^(j+l)
#

# Inverse of a^i b^j:
#   (a^i b^j)^-1 = b^-j a^-i
#                = b^(4-j) a^(2n-i)
#                = a^s(2n-i) b^(4-j) where s = (-1)^j

import re

class genquat_t:
	#i = 0
	#j = 0
	#n = 0

	def __init__(self, argi, argj, argn):
		argi %= argn + argn;
		if (argi >= argn):
			argj += 2
			argi -= argn
		self.n = argn
		self.i = argi
		self.j = argj & 3

	def __eq__(a,b):
		return ((a.i == b.i) and (a.j == b.j))

	def __ne__(a,b):
		return not (a == b)

	def __mul__(a,b):
		# a^i b^j a^k b^l = a^(i+sk) b^(j+l)
		if (a.n != b.n):
			raise RuntimeError
		c = genquat_t(0, 0, a.n)

		i = a.i
		j = a.j
		k = b.i
		l = b.j
		n = a.n
		twon = n + n
		if (j & 1):
			c.i = (i-k+twon) % twon
		else:
			c.i = (i+k) % twon
		c.j = (j+l) & 3
		if (c.i >= n):
			c.i -= n
			c.j += 2
			c.j &= 3
		return c

	def inv(a):
		# Inverse of a^i b^j:
		#   (a^i b^j)^-1 = a^s(2n-i) b^(4-j) where s = (-1)^j
		if (a.j & 1):
			msi = a.i
		else:
			msi = a.n + a.n - a.i
		c = genquat_t(msi, -a.j, a.n)
		return c

	def scan(self, string, argn):
		groups = re.match(r"^(\d)+,(\d+)$", string).groups();
		if len(groups) != 2:
			raise IOError
		self.__init__(int(groups[0]), int(groups[1]), argn)

	def __str__(self):
		return str(self.i) + "," + str(self.j)

	def __repr__(self):
		return self.__str__()

def params_from_string(params_string):
	n = int(params_string)
	return n

def from_string(value_string, params_string):
	n = params_from_string(params_string)
	obj = genquat_t(0, 0, n)
	obj.scan(value_string, n)
	return obj

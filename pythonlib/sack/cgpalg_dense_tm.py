#!/usr/bin/python -Wall

# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

import sys
import re
import copy

# ================================================================
# Initial attempt at complex group algebras CG for small finite groups G.  This
# could, conceivably, be generalized to FG (for arbitrary user-specified
# fields) or RG (for arbitrary user-specified rings).
#
# There are two possible storage representations for an element of CG:
# * Sparse:  Keep a list of non-zero coefficients, with their
#   corresponding group elements.
# * Dense:   Keep a list of group elements, with another list of coefficients.
#
# For now I will attempt the latter.  Good hygiene would require me to make
# the following checks (which I will not):
# * A's coef-array length = A's group-elements-array length
# * B's coef-array length = B's group-elements-array length
# * A's coef-array length = B's coef-array length
# * A's group-elements-array length = B's group-elements-array length
#
# ================================================================
# John Kerl
# 2007-05-08
# ================================================================

class cgpalg_t:
	def __init__(self, coef_array, gp_elt_array):
		#self.check_lengths(len(coef_array), len(gp_elt_array), "coefs", "gp_elts")
		self.coefs   = copy.copy(coef_array)
		self.gp_elts = copy.copy(gp_elt_array)

	def __add__(a,b):
		#a.check_lengths(len(a.gp_elts), len(b.gp_elts), "coefs", "gp_elts")
		c = cgpalg_t(a.coefs, a.gp_elts)
		for i in range (0, len(a.coefs)):
			c.coefs[i] = a.coefs[i] + b.coefs[i]
		return c

	def __sub__(a,b):
		#a.check_lengths(len(a.gp_elts), len(b.gp_elts), "coefs", "gp_elts")
		c = cgpalg_t(a.coefs, a.gp_elts)
		for i in range (0, len(a.coefs)):
			c.coefs[i] = a.coefs[i] - b.coefs[i]
		return c

	def index_of(self, g):
		for k in range(0, len(self.gp_elts)):
			if (g == self.gp_elts[k]):
				return k
		print "cgpalg_t:  Couldn't find [", g, "] in gp_elts array."
		sys.exit(1)

	def __mul__(a,b):
		#a.check_lengths(len(a.gp_elts), len(b.gp_elts), "coefs", "gp_elts")
		c = cgpalg_t(a.coefs, a.gp_elts)
		# XXX XXX XXX
		zero = a.coefs[0] - a.coefs[0]
		for i in range (0, len(a.coefs)):
			c.coefs[i] = zero
		for i in range (0, len(a.coefs)):
			for j in range (0, len(b.coefs)):
				k = c.index_of(a.gp_elts[i] * b.gp_elts[j])
				c.coefs[k] += a.coefs[i] * b.coefs[j]
		return c

	def __eq__(a,b):
		if (len(a.coefs) != len(b.coefs)):
			return 0
		n = len(a.coefs)
		for i in range(0, n):
			if (a.coefs[i] != b.coefs[i]):
				return 0
		return 1

	def __ne__(a,b):
		return not (a == b)

	def __neg__(a):
		c = cgpalg_t(a.coefs, a.gp_elts)
		for i in range(0, len(a.gp_elts)):
			c.coefs[i] = -a.coefs[i]
		return c

#	def scan(self, res_string, cgpalg_array):
#		res_strings = re.split(',', res_string)
#		#self.check_lengths(len(res_strings), len(cgpalg_array), res_strings,
#			str(cgpalg_strings))
#		n = len(res_strings)
#		coef_array = range(0, n)
#		for i in range(0, n):
#			coef_array[i] = int(res_strings[i])
#		self.__init__(coef_array, gp_elt_array)

	def __str__(self):
		string = ""
		for i in range(0, len(self.coefs)):
			if (i > 0):
				string += " "
			string += "["
			string += str(self.coefs[i])
			string += "]*["
			string += str(self.gp_elts[i])
			string += "]"
		return string

	def __repr__(self):
		return self.__str__()

#	def check_length(self, length, desc):
#		if (length < 1):
#			print desc, "length", str(length), "< 1"
#			raise RuntimeError

#	def check_lengths(self, len1, len2, desc1, desc2):
#		self.check_length(len1, desc1)
#		self.check_length(len2, desc2)
#		if (len1 != len2):
#			print desc1, "length", str(len1), "!=", desc2, "length", len2
#			raise RuntimeError

#def params_from_string(params_string):
#	if (len(params_string) == 0):
#		print "Modadd requires non-empty parameter string"
#		sys.exit(1)
#	cgpalg_strings = re.split(',', params_string)
#	n = len(cgpalg_strings)
#	cgpalg_array = range(0, n)
#	for i in range(0, n):
#		cgpalg_array[i] = int(cgpalg_strings[i])
#	return cgpalg_array

#def from_string(value_string, params_string):
#	cgpalg_array = params_from_string(params_string)
#	obj = cgpalg_t([1], [1])
#	obj.scan(value_string, cgpalg_array)
#	return obj

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
# * Dense:   Keep a list of group elements in each algebra element, with
# another list of coefficients.
#
# For now I will attempt the former.  A "pair" is a two-element list of
# coefficient and group element; an algebra element is a list of pairs.
#
# ================================================================
# John Kerl
# 2007-05-08
# ================================================================

class cgpalg_t:

	def __init__(self, pairs_array):
		self.pairs = copy.deepcopy(pairs_array)

	def index_of(self, g):
		for k in range(0, len(self.pairs)):
			if (g == self.pairs[k][1]):
				return [1, k]
		return [0, 0]

	def zero_strip(self):
		untested = self.pairs
		self.pairs = []
		while (untested):
			x = untested[0]
			untested = untested[1:]
			if (x[0] != 0):
				self.pairs += [x]

	# I am using sparse storage.  However, this routine permits a dense
	# extraction of coefficients:  Given an array of group elements, it
	# returns a list of coefficients (in the same order).
	#
	# This makes it possible to hand the results off to a linear-algebra
	# routine.
	def to_coef_array(self, group_elements):
		coefs = []
		for g in group_elements:
			coef = 0
			[found, k] = self.index_of(g)
			if (found):
				coef = self.pairs[k][0]
			coefs += [coef]
		return coefs

	def __add__(a,b):
		# Concatenate the two lists.  Then merge the pairs with matching
		# group elements.
		c = cgpalg_t([])
		unmerged_pairs = copy.deepcopy(a.pairs + b.pairs)
		while (unmerged_pairs):
			current_pair = unmerged_pairs[0]
			[found, k] = c.index_of(current_pair[1])
			if (found):
				# Update
				c.pairs[k][0] += current_pair[0]
			else:
				# Insert
				c.pairs += [current_pair]
			unmerged_pairs = unmerged_pairs[1:]
		return c

	def __neg__(b):
		negb = cgpalg_t(b.pairs)
		for k in range(0, len(negb.pairs)):
			negb.pairs[k][0] = -negb.pairs[k][0]
		return negb

	def __sub__(a,b):
		return a + (-b)

	def __mul__(a,b):
		c = cgpalg_t([])
		for ap in a.pairs:
			for bp in b.pairs:
				ccoef  = ap[0] * bp[0] # Field multiplication
				cgpelt = ap[1] * bp[1] # Group multiplication
				[found, k] = c.index_of(cgpelt)
				if (found):
					# Update
					c.pairs[k][0] += ccoef
				else:
					# Insert
					c.pairs += [[ccoef, cgpelt]]
		c.zero_strip()
		return c

	# The group data type must support the inv() method.
	# This is a stub for correct implementation and doesn't work (except for singletons).
	def inv(self):
		bi = cgpalg_t([])
		n = len(self.pairs)
		if (n == 0):
			print "cgpalg_t.inv:  division by zero."
			sys.exit(1)
		recip_n = 1.0/n
		for pair in self.pairs:
			bi.pairs += [[recip_n/pair[0], pair[1].inv()]]
		return bi

	def __div__(a,b):
		return a * b.inv()

#	def __eq__(a,b):
#		if (len(a.pairs) != len(b.pairs)):
#			return 0
#		n = len(a.coefs)
#		for i in range(0, n):
#			if (a.coefs[i] != b.coefs[i]):
#				return 0
#		return 1

#	def __ne__(a,b):
#		return not (a == b)

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
		if (len(self.pairs) == 0):
			string = "0"
		for i in range(0, len(self.pairs)):
			if (i > 0):
				string += " "
			string += "["
			string += str(self.pairs[i][0])
			string += "]*["
			string += str(self.pairs[i][1])
			string += "]"
		return string

	def __repr__(self):
		return self.__str__()

# Construct an element of C S_n, given only a list of permutations: each
# coefficient is 1.
def from_pmtns(pmtn_array):
	pairs = []
	for pmtn in pmtn_array:
		pairs += [[1, pmtn]]
	return cgpalg_t(pairs)

# Construct an element of C S_n, given only a list of permutations: compute the
# coefficient from the parity.  The group class being used must support the
# sgn() method.
def from_pmtns_with_parity(pmtn_array):
	pairs = []
	for pmtn in pmtn_array:
		pairs += [[pmtn.sgn(), pmtn]]
	return cgpalg_t(pairs)

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

#!/usr/bin/python -Wall

# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

import re
import copy
import sys

import spec_tables
import sackgrp

def name_to_index(string, name_table):
	i = 0
	for name in name_table:
		if string == name:
			return [1, i]
		i += 1
	return [0, 0]

def name_to_index_or_die(string, name_table):
	[found, idx] = name_to_index(string, name_table)
	if (not found):
		print "spec scan failure on \"%s\"." % (string)
		sys.exit(1)
	return idx

class spec_t:
	def __init__(self, argcode):
		self.code = argcode

	def __mul__(a,b):
		c = spec_t(spec_tables.mul_table[a.code][b.code]);
		return c

	def __eq__(a,b):
		return (a.code == b.code)
	def __ne__(a,b):
		return not (a == b)

	def __lt__(a,b):
		return (a.code <  b.code)
	def __le__(a,b):
		return (a.code <= b.code)
	def __gt__(a,b):
		return (a.code >  b.code)
	def __ge__(a,b):
		return (a.code >= b.code)

	def inv(a):
		c = spec_t(spec_tables.inv_table[a.code]);
		return c

	def scan(self, string):
		self.code = name_to_index_or_die(string, spec_tables.name_table)

	def __str__(self):
		return spec_tables.name_table[self.code]

	def __repr__(self):
		return self.__str__()

def params_from_string(params_string):
	return params_string

def from_string(value_string, params_string):
	not_used = params_from_string(params_string)
	idx = name_to_index_or_die(value_string, spec_tables.name_table)
	obj = spec_t(idx)
	return obj

def install_table(cayley_table_with_names):
	spec_tables.mul_table  = []
	spec_tables.inv_table  = []
	spec_tables.name_table = []
	n = len(cayley_table_with_names)

	# Populate the name table
	spec_tables.name_table = copy.copy(cayley_table_with_names[0])

	# Populate the mul table.
	#
	# I should do some checking on the cayley_table_with_names -- the user
	# might have given me input which is non-square, or even ragged.

	# Fill it with zeroes, so the matrix has the correct size and may be indexed.
	row = [1] * n
	for i in range(0, n):
		spec_tables.mul_table.append(copy.copy(row))

	# Now put real data in.
	for i in range(0, n):
		for j in range(0, n):
			spec_tables.mul_table[i][j] = name_to_index_or_die(cayley_table_with_names[i][j], spec_tables.name_table)

	# Populate the inv table.
	# I am being crass here.  I'm assuming the Cayley table is good before I start.
	# The good news is that the is-group functions don't use the inv table.
	G = []
	for i in range(0, n):
		G.append(spec_t(i))
	[found, e] = sackgrp.find_id(G)
	if (found):
		for i in range(0, n):
			x = G[i]
			for j in range(0, n):
				y = G[j]
				z = x*y
				if (z.code == e.code):
					spec_tables.inv_table.append(j)
					continue

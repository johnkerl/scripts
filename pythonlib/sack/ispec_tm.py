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
import ispec_tbl

import sackgrp

class ispec_t:
	def __init__(self, argcode):
		self.code = argcode

	def __mul__(a,b):
		c = ispec_t(ispec_tbl.ispec_mul_table[a.code][b.code]);
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
		c = ispec_t(ispec_tbl.ispec_inv_table[a.code]);
		return c

	def scan(self, string):
		self.code = int(string)

	def __str__(self):
		return str(self.code)

	def __repr__(self):
		return self.__str__()

def params_from_string(params_string):
	return params_string

def from_string(value_string, params_string):
	not_used = params_from_string(params_string)
	k = int(value_string) # xxx needs error checking
	obj = ispec_t(k)
	return obj

def install_table(table):
	ispec_tbl.ispec_mul_table = copy.copy(table)
	ispec_tbl.ispec_inv_table = []
	n = len(table)

	# Populate the inv table.
	# I am being crass here.  I'm assuming the Cayley table is good before I start.
	# The good news is that the is-group functions don't use the inv table.
	G = []
	for i in range(0, n):
		G.append(ispec_t(i))
	[found, e] = sackgrp.find_id(G)
	if (found):
		for i in range(0, n):
			x = G[i]
			for j in range(0, n):
				y = G[j]
				z = x*y
				if (z.code == e.code):
					ispec_tbl.ispec_inv_table.append(j)
					continue

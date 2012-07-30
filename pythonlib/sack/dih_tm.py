#!/usr/bin/python -Wall

# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

import re

class dih_t:
	#rot  = 0
	#flip = 0
	#n    = 0

	def __init__(self, argrot, argflip, argn):
		self.n    = argn
		self.rot  = argrot  % self.n
		self.flip = argflip & 1

	def __eq__(a,b):
		return ((a.rot == b.rot) and (a.flip == b.flip))

	def __ne__(a,b):
		return not (a == b)

	def __mul__(a,b):
		if (a.n != b.n):
			raise RuntimeError
		if (a.flip):
			crot = a.rot - b.rot
		else:
			crot = a.rot + b.rot
		c = dih_t(crot, a.flip ^ b.flip, a.n)
		return c

	def inv(a):
		if (a.flip):
			c = dih_t(a.rot, a.flip, a.n)
			return c
		else:
			c = dih_t(a.n - a.rot, a.flip, a.n)
			return c

	def scan(self, string, argn):
		groups = re.match(r"^(\d)+,(\d+)$", string).groups();
		if len(groups) != 2:
			raise IOError
		self.__init__(int(groups[0]), int(groups[1]), argn)

	def __str__(self):
		return str(self.rot) + "," + str(self.flip)

	def __repr__(self):
		return self.__str__()

def params_from_string(params_string):
	n = int(params_string)
	return n

def from_string(value_string, params_string):
	n = params_from_string(params_string)
	obj = dih_t(0, 0, n)
	obj.scan(value_string, n)
	return obj

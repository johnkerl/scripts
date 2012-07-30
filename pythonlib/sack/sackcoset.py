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

class coset:
	slots = []

	def __init__(self, slots):
		self.slots = copy.copy(slots)
		self.slots.sort()
		# xxx need deep sort

	def __eq__(a,b):
		#xxx check lens
		n = len(a.slots)
		for i in range(0, n):
			if (a.slots[i] != b.slots[i]):
				return 0
		return 1

	def __ne__(a,b):
		return not (a == b)

	def __mul__(a,b):
		#xxx check lens
		#xxx take a.slots[0] * b.slots and sort.
		#Don't check well-definedness here.
		n = len(a.slots)
		c = coset(a.slots)
		for i in range(0, n):
			c.slots[i] = a.slots[0] * b.slots[i]
		c.slots.sort()
		return c

	def inv(a):
		#xxx take a.slots[i].inv and sort.
		n = len(a.slots)
		c = coset(a.slots)
		for i in range(0, n):
			c.slots[i] = a.slots[i].inv()
		c.slots.sort()
		return c

	def __str__(self):
		string = "["
		string += str(self.slots[0])
		n = len(self.slots)
		for i in range(1, n):
			string += ","
			string += str(self.slots[i])
		string += "]"
		return string

	def __repr__(self):
		return self.__str__()

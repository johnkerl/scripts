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

class tuple:
	slots = []

	def __init__(self, slots):
		self.slots = copy.copy(slots)

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
		n = len(a.slots)
		c = tuple(a.slots)
		for i in range(0, n):
			c.slots[i] = a.slots[i] * b.slots[i]
		return c

	def inv(a):
		n = len(a.slots)
		c = tuple(a.slots)
		for i in range(0, n):
			c.slots[i] = a.slots[i].inv()
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

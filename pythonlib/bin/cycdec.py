#!/usr/bin/python

# ================================================================
# Copyright (c) John Kerl 2007
# kerl.john.r@gmail.com
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
import sys

# ----------------------------------------------------------------
def int_cycle_decomposition(list):
	n = len(list)
	cd = []
	marks = [0] * (n)
	for i in range(0, n):
		if (marks[i]):
			continue
		cycle = []
		next = i
		marks[next] = 1
		while (1):
			cycle = cycle + [next]
			next = list[next]
			if (next == i):
				break
			marks[next] = 1
		cd = cd + [cycle]
	return cd

# ----------------------------------------------------------------
def index_of(value, string):
	n = len(string)
	for i in range(0, n):
		if (string[i] == value):
			return i
	return -1

# ----------------------------------------------------------------
def string_cycle_decomposition(old_string, new_string):
	n = len(old_string)
	cd = []
	marks = [0] * (n)
	for i in range(0, n):
		if (marks[i]):
			continue
		cycle = []
		nexti = i
		marks[nexti] = 1
		num_passes = 0
		while (1):
			num_passes += 1
			if (num_passes > n):
				print >> sys.stderr, "string_cycle_decomposition:  \"%s\" is not a permutation of \"%s\"." % \
					(new_string, old_string)
				sys.exit(1)
			cycle = cycle + [old_string[nexti]]

			# A B C D
			# C A B D
			#
			# nexti = 0

			nextval = new_string[nexti]
			nexti = index_of(nextval, old_string)
			if (nexti == -1):
				print >> sys.stderr, "string_cycle_decomposition:  \"%s\" is not a permutation of \"%s\"." % \
					(new_string, old_string)
				sys.exit(1)

			if (nexti == i):
				break
			marks[nexti] = 1
		cd = cd + [cycle]
	return cd

# ----------------------------------------------------------------
def stringify_cycle_decomposition(old_string, new_string):
	cd = string_cycle_decomposition(old_string, new_string)
	s = ""
	for cycle in cd:
		s += "("
		for elt in cycle:
			s += elt
		s += ")"
	return s

# ----------------------------------------------------------------
print int_cycle_decomposition([0,1,2,3])
print int_cycle_decomposition([0,2,1,3])
print int_cycle_decomposition([1,2,3,0])

print string_cycle_decomposition("abcd", "cabd")
print string_cycle_decomposition("numbers", "srembnu")
print stringify_cycle_decomposition("NUMBERS", "SREMBNU")

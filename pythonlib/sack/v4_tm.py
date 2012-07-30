#!/usr/bin/python -Wall

# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

import re

# e a b c
# a e c b
# b c e a
# c b a e

# v4_table = [
# 	[ 0,1,2,3 ],
# 	[ 1,0,3,2 ],
# 	[ 2,3,0,1 ],
# 	[ 3,2,1,0 ]]

class v4_t:
	#code = 0

	def __init__(self, argcode):
		self.code = argcode & 3

	def __eq__(a,b):
		return (a.code == b.code)

	def __ne__(a,b):
		return not (a == b)

	def __mul__(a,b):
		#c = v4_t(v4_table[a.code][b.code]);
		c = v4_t(a.code ^ b.code)
		return c

	def inv(a):
		c = v4_t(a.code)
		return c

	def scan(self, string):
		if (string == "e"):
			self.__init__(0)
		elif (string == "a"):
			self.__init__(1)
		elif (string == "b"):
			self.__init__(2)
		elif (string == "c"):
			self.__init__(3)
		else:
			raise IOError

	def __str__(self):
		if (self.code == 0):
			return "e"
		elif (self.code == 1):
			return "a"
		elif (self.code == 2):
			return "b"
		elif (self.code == 3):
			return "c"
		else:
			raise IOError

	def __repr__(self):
		return self.__str__()

def params_from_string(params_string):
	return 0

def from_string(value_string, params_string):
	not_used = params_from_string(params_string)
	obj = v4_t(0)
	obj.scan(value_string)
	return obj

#x = v4_t(3)
#y = v4_t(2)
#print x
#print y
#z = x * y
#print z
#z.scan("a")
#print z
#print

#for i in range(0, 4):
#	for j in range(0, 4):
#		x = v4_t(i)
#		y = v4_t(j)
#		z = x * y
#		print x, y, z
#	print

#!/usr/bin/python -Wall

# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

import re

quatu_mul_table = [
	# 1 -1  i -i  j -j  k -k
	[ 0, 1, 2, 3, 4, 5, 6, 7 ], #  1
	[ 1, 0, 3, 2, 5, 4, 7, 6 ], # -1
	[ 2, 3, 1, 0, 6, 7, 5, 4 ], #  i
	[ 3, 2, 0, 1, 7, 6, 4, 5 ], # -i
	[ 4, 5, 7, 6, 1, 0, 2, 3 ], #  j
	[ 5, 4, 6, 7, 0, 1, 3, 2 ], # -j
	[ 6, 7, 4, 5, 3, 2, 1, 0 ], #  k
	[ 7, 6, 5, 4, 2, 3, 0, 1 ], # -k
]

quatu_inv_table = [ 0, 1, 3, 2, 5, 4, 7, 6 ]
# 1 -1  i -i  j -j  k -k

class quatu_t:
	#code = 0

	def __init__(self, argcode):
		self.code = argcode & 7

	def __mul__(a,b):
		c = quatu_t(quatu_mul_table[a.code][b.code]);
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
		c = quatu_t(quatu_inv_table[a.code]);
		return c

	def scan(self, string):
		if (string == "1"):
			self.__init__(0)
		elif (string == "-1"):
			self.__init__(1)
		elif (string == "i"):
			self.__init__(2)
		elif (string == "-i"):
			self.__init__(3)
		elif (string == "j"):
			self.__init__(4)
		elif (string == "-j"):
			self.__init__(5)
		elif (string == "k"):
			self.__init__(6)
		elif (string == "-k"):
			self.__init__(7)
		else:
			raise IOError

	def __str__(self):
		if (self.code == 0):
			return " 1"
		elif (self.code == 1):
			return "-1"
		elif (self.code == 2):
			return " i"
		elif (self.code == 3):
			return "-i"
		elif (self.code == 4):
			return " j"
		elif (self.code == 5):
			return "-j"
		elif (self.code == 6):
			return " k"
		elif (self.code == 7):
			return "-k"
		else:
			raise IOError

	def __repr__(self):
		return self.__str__()

def params_from_string(params_string):
	# xxx check empty
	return 0

def from_string(value_string, params_string):
	not_used = params_from_string(params_string)
	obj = quatu_t(0)
	obj.scan(value_string)
	return obj

#x = quatu_t(3)
#y = quatu_t(2)
#print x
#print y
#z = x * y
#print z
#z.scan("i")
#print z
#print

#for i in range(0, 8):
#	for j in range(0, 8):
#		x = quatu_t(i)
#		y = quatu_t(j)
#		z = x * y
#		print x, y, z
#	print

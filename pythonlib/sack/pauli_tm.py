#!/usr/bin/python -Wall

# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

import re

# sigmax =  0  1
#           1  0
#
# sigmay =  0 -i
#           i  0
#
# sigmaz =  1  0
#           0 -1

# ----------------------------------------------------------------
def sanitize1(x):
	if (type(x) == type(0)):
		return x
	elif (type(x) == type(0.0)):
		return x
	elif (x == x.conjugate()):
		return x.real
	else:
		return x

# ----------------------------------------------------------------
class pauli_t:

	def sanitize(self):
		self.a = sanitize1(self.a)
		self.b = sanitize1(self.b)
		self.c = sanitize1(self.c)
		self.d = sanitize1(self.d)

	def __init__(self, a, b, c, d):
		self.a = a
		self.b = b
		self.c = c
		self.d = d
		self.sanitize()

	def __mul__(X,Y):
		# a b   a b
		# c d   c d
		za = X.a*Y.a + X.b*Y.c
		zb = X.a*Y.b + X.b*Y.d
		zc = X.c*Y.a + X.d*Y.c
		zd = X.c*Y.b + X.d*Y.d
		Z = pauli_t(za, zb, zc, zd)
		return Z

	def __eq__(X,Y):
		if (X.a != Y.a): return 0
		if (X.b != Y.b): return 0
		if (X.c != Y.c): return 0
		if (X.d != Y.d): return 0
		return 1

	def __ne__(X,Y):
		return not (X == Y)

	def __lt__(X,Y):
		if (X.a <  Y.a): return 0
		if (X.b <  Y.b): return 0
		if (X.c <  Y.c): return 0
		if (X.d <  Y.d): return 0
		return 1
	def __le__(X,Y):
		if (X.a <= Y.a): return 0
		if (X.b <= Y.b): return 0
		if (X.c <= Y.c): return 0
		if (X.d <= Y.d): return 0
		return 1
	def __gt__(X,Y):
		if (X.a >  Y.a): return 0
		if (X.b >  Y.b): return 0
		if (X.c >  Y.c): return 0
		if (X.d >  Y.d): return 0
		return 1
	def __ge__(X,Y):
		if (X.a >= Y.a): return 0
		if (X.b >= Y.b): return 0
		if (X.c >= Y.c): return 0
		if (X.d >= Y.d): return 0
		return 1

	def inv(X):
		det = X.a*X.d - X.b*X.c
		Z = pauli_t(X.d/det, -X.b/det, -X.c/det, X.a/det)
		return Z

	# xxx stub
	def scan(self, string):
		if (string == "I"):
			self.__init__(1,0,0,1)
		elif (string == "sx"):
			self.__init__(0,1,1,0)
		elif (string == "sy"):
			self.__init__(0,-1j,1j,0)
		elif (string == "sz"):
			self.__init__(1,0,0,-1)
		# parse on slashes ...
		else:
			raise IOError

	def __str__(self):
		return str(self.a) + "/" + str(self.b) + "/" + str(self.c) + "/" + str(self.d)

	def __repr__(self):
		return self.__str__()

def params_from_string(params_string):
	# xxx check empty
	return 0

def from_string(value_string, params_string):
	not_used = params_from_string(params_string)
	obj = pauli_t(0,0,0,0)
	obj.scan(value_string)
	return obj

## ----------------------------------------------------------------
#from sackgrp import *
#X=from_string("sx",""); print X
#Y=from_string("sy",""); print Y
#Z=from_string("sz",""); print Z
#XX=X*X;print XX
#YY=Y*Y;print YY
#ZZ=Z*Z;print ZZ
#print
#G=[X,Y,Z]
#close_group(G)
#for g in G:
#	print g
#print
#print_cayley_table(G)
#print
#orders = get_orders(G)
#n = len(G)
#for k in range(0, n):
#	print G[k], orders[k]

#!/usr/bin/python -Wall

# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# John Kerl
# kerl.john.r@gmail.com
# 2008-11-14
# ================================================================

import sys
import re
import copy

import f2poly_tm

# xxx this is in mid-port from C++.

# ================================================================
def f2polymod_from_string(string):
	return f2polymod_t(int(string, 16))

# ================================================================
class f2polymod_t:

	#def __init__(self, resbits, modbits):
	#	self.modbits = modbits
	#	self.resbits = f2poly_tm.imod(resbits, modbits)

	# Both arguments should be of type f2poly_t.
	def __init__(self, residue, modulus):
		self.modulus = modulus
		self.residue = residue % modulus

	def __add__(a,b):
		c = f2polymod_t(a.residue + b.residue, a.modulus)
		return c
	def __sub__(a,b):
		c = f2polymod_t(a.residue - b.residue, a.modulus)
		return c
	def __mul__(a,b):
		c = f2polymod_t(a.residue * b.residue, a.modulus)
		return c

	# xxx fix me
	def recip(a):
		pass

#int f2polymod_t::recip(f2polymod_t & rinv)
#	f2poly_t g, a, b;
#	g = this->residue.ext_gcd(this->modulus, a, b);
#
#	if (g.find_degree() != 0): # Error check
#		//std::cerr << "f2polymod recip: zero or zero divisor.";
#		return 0
#	else:
#		rinv = f2polymod_t(a, this->modulus)
#		return 1

	def __div__(a,b):
		return a * b.recip()

	# xxx fix me
	def __pow__(a, e):
		ap = a.residue
		one = f2poly_t(1)
		rv = one

		xxx types
		if (e == 0):
			if (a.residue.bits == 0):
				print >> sys.stderr, "f2polymod_t.exp:  0^0 undefined."
				sys.exit(1)
			return one
		elif (e < 0):
			if (a.residue.bits == 0):
				print >> sys.stderr, "f2polymod_t.exp:  division by zero."
				sys.exit(1)
			
			xxx
			f2polymod_t inv = one/ *this
			xp = inv.residue
			e = -e

		while (e != 0):
			if e & 1:
				rv.residue = (rv.residue * xp) % this->modulus
			e >>= 1
			xp = (xp * xp) % this->modulus
		return rv


	def __eq__(a,b):
		return a.bits == b.bits
	def __ne__(a,b):
		return not (a == b)
	def __neg__(a):
		return a

	def scan(self, string):
		self.bits = int(string, 16)

	def __str__(self):
		# xxx temp
		return self.residue.__str__()
		#return "%x" % self.bits
	def __repr__(self):
		return self.__str__()


#std::ostream & operator<<(std::ostream & os, const f2polymod_t & a)
#	a.residue.dprint(os, a.modulus.find_degree() - 1)
#
#int f2polymod_t::from_string(char * string, f2poly_t m)
#	f2poly_t r;
#	std::istringstream iss(string, std::ios_base::in);
#	iss >> r;
#	if (iss.fail()) {
#		return 0;
#	}
#	else {
#		*this = f2polymod_t(r, m);
#		return 1;
#	}
#
#void f2polymod_t::check_moduli(f2polymod_t & that) const
#	if (this->modulus != that.modulus) {
#		std::cerr
#			<< "f2polymod_t: mixed moduli "
#			<< this->modulus
#			<< ", "
#			<< that.modulus
#			<< ".";
#		std::cerr << std::endl;
#		exit(1);
#	}

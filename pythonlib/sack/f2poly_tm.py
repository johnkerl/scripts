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

# ================================================================
def f2poly_from_string(string):
	return f2poly_t(int(string, 16))

def idegree(bits):
	if (bits == 0):
		return 0 # The zero polynomial has degree zero by fiat.
	rv = -1
	while bits:
		rv += 1
		bits >>= 1
	return rv

def imul(abits, bbits):
	cbits = 0
	shift = 0
	while bbits:
		if bbits & 1:
			cbits ^= abits << shift
		bbits >>= 1
		shift += 1
	return cbits

# ----------------------------------------------------------------
# iquot_and_rem
# Returns [quotient, remainder].
# ----------------------------------------------------------------
# E.g.
# dividend = 1,2,3,4 (1 + 2x + 3x^2 + 4x^3)
# divisor  = 1,1,2   (1 +  x + 2x^2)
# modulus = 7
#
#             q=4,2   r = 4,3
#        +----------
# 1,1,2  |  1,2,3,4
#        |    2,2,4 shift = 1.  4/2 mod 7 = 2.  1,1,2 * 2 = 2,2,4.
#        +----------
#        |  1 0 1
#        |  4 4 1   shift = 0.  1/2 mod 7 = 4   1,1,2 * 4 = 4,4,1
#        +----------
#        |  4 3
#
# ----------------------------------------------------------------

def iquot_and_rem(abits, bbits):
	if bbits == 0: # Divisor is zero.
		print >> sys.stderr, "f2poly_tm.iquot_and_rem: Divide by zero."
		sys.exit(1)
	divisor_l1_pos = idegree(bbits)

	if abits == 0: # Dividend is zero.
		return [0, 0]
	dividend_l1_pos = idegree(abits)

	l1_diff = dividend_l1_pos - divisor_l1_pos
	if l1_diff < 0: # Dividend has lower degree than divisor.
		return [0, abits]

	shift_divisor = bbits << l1_diff
	quotbits  = 0
	rembits   = abits
	check_pos = dividend_l1_pos
	quot_pos  = l1_diff
	while check_pos >= divisor_l1_pos:
		# if f2poly_bit_at(rembits, check_pos)
		if rembits & (1 << check_pos):
			rembits ^= shift_divisor
			# f2poly_set_bit(quotbits, quot_pos)
			quotbits |= 1 << quot_pos
		shift_divisor >>= 1
		check_pos -= 1
		quot_pos  -= 1

	return [quotbits, rembits]

# ----------------------------------------------------------------
# This is quot_and_rem, but doesn't track the quotient.  This saves a few
# cycles for finite-field arithmetic.

def imod(abits, bbits):
	if bbits == 0: # Divisor is zero.
		print >> sys.stderr, "f2poly_tm.iquot_and_rem: Divide by zero."
		sys.exit(1)
	divisor_l1_pos = idegree(bbits)

	if abits == 0: # Dividend is zero.
		return 0
	dividend_l1_pos = idegree(abits)

	l1_diff = dividend_l1_pos - divisor_l1_pos
	if l1_diff < 0: # Dividend has lower degree than divisor.
		return abits

	shift_divisor = bbits << l1_diff
	rembits   = abits
	check_pos = dividend_l1_pos
	quot_pos  = l1_diff
	while check_pos >= divisor_l1_pos:
		# if f2poly_bit_at(rembits, check_pos)
		if rembits & (1 << check_pos):
			rembits ^= shift_divisor
		shift_divisor >>= 1
		check_pos -= 1
		quot_pos  -= 1

	return rembits

# ----------------------------------------------------------------
def iexp(abits, e):
	deg = idegree(abits)
	ap  = abits
	rv  = 1

	if abits == 0:
		if e == 0:
			print >> sys.stderr, "f2poly_t.iexp:  0 ^ 0 undefined."
			sys.exit(1)
		elif e < 0:
			print >> sys.stderr, "f2poly_t.iexp:  division by zero."
			sys.exit(1)
		else:
			return 0
	elif deg == 0: # Unit
		return 1
	else: # Degree 1 or higher.
		if e < 0:
			print >> sys.stderr, "f2poly_t.iexp:  division by non-unit."
			sys.exit(1)
		else:
			while e != 0:
				if e & 1:
					rv *= ap
				e = e >> 1
				ap *= ap
			return rv

# ----------------------------------------------------------------
def igcd(abits, bbits):
	if abits == 0: return bbits
	if bbits == 0: return abits

	cbits = abits
	dbits = bbits
	while True:
		[qbits, rbits] = iquot_and_rem(cbits, dbits)
		if rbits == 0:
			break
		cbits = dbits
		dbits = rbits
	return dbits

# ----------------------------------------------------------------
# xxx b0rk3n:  f2test 3 6

# Blankinship's algorithm.
# Returns [g, r, s] where g = ar + bs.
def iext_gcd(abits, bbits):
	if (abits == 0):
		return [bbits, 0, 1]
	if (bbits == 0):
		return [abits, 1, 0]

	rprime = 1
	s      = 1
	r      = 0
	sprime = 0
	c      = abits
	d      = bbits

	while 1:
		[q, r] = iquot_and_rem(c, d)
		# Note:  now c = qd + r and 0 <= r < d
		if r == 0:
			break
		c = d
		d = r

		t      = rprime
		rprime = r
		qr     = imul(q, r)
		r      = t ^ qr

		t      = sprime
		sprime = s
		qs     = imul(q, s)
		s      = t ^ qs

	return [d, r, s]

# ================================================================
class f2poly_t:
	def __init__(self, bits):
		self.bits = bits

	def __add__(a,b):
		c = f2poly_t(a.bits ^ b.bits)
		return c
	def __sub__(a,b):
		c = f2poly_t(a.bits ^ b.bits)
		return c

	# This helps avoid infinite shift loops.
	# xxx mv to an ifunc
	def check_unsigned_bits(self):
		if self.bits < 0:
			print >> sys.stderr, \
				"f2poly_t:  signed input %d detected." % (self.bits)
			sys.exit(1)
		return self.bits

	def degree(self):
		return idegree(self.check_unsigned_bits())

	def __mul__(a,b):
		bbits = b.check_unsigned_bits()
		return f2poly_t(imul(a.bits, bbits))

	def __div__(a,b):
		[qbits, rbits] = iquot_and_rem(a.bits, b.bits)
		return f2poly_t(qbits)

	def __mod__(a,b):
		[qbits, rbits] = iquot_and_rem(a.bits, b.bits)
		return f2poly_t(rbits)

	def __pow__(a, e):
		return f2poly_t(iexp(a.bits, e))

	def gcd(a, b):
		return f2poly_t(igcd(a.bits, b.bits))

	# ----------------------------------------------------------------
	# Blankinship's algorithm.
	# Returns [g, r, s] where g = ar + bs.
	def ext_gcd(a, b):
		[gbits, rbits, sbits] = iext_gcd(a.bits, b.bits)
		return [f2poly_t(gbits), f2poly_t(rbits), f2poly_t(sbits)]

	def __eq__(a,b):
		return a.bits == b.bits
	def __ne__(a,b):
		return not (a == b)
	def __neg__(a):
		return a

	def scan(self, string):
		self.bits = int(string, 16)

	def __str__(self):
		return "0x%x" % self.bits
		#return "%x" % self.bits
	def __repr__(self):
		return self.__str__()

#inline f2poly_t f2poly_t::prime_sfld_elt(int v) const
#
#	f2poly_t rv(v & 1)
#	return rv

#inline int f2poly_t::get_char(void)
#
#	return 2

#inline f2poly_t f2poly_t::deriv(void)
#
#	f2poly_t rv = *this
#	rv.bits >>= 1
#	rv.bits &= 0x55555555
#	return rv

#inline int  f2poly_t::operator< (f2poly_t that) const
#
#	return this->bits < that.bits
#
#inline int  f2poly_t::operator> (f2poly_t that) const
#
#	return this->bits > that.bits
#
#inline int  f2poly_t::operator<=(f2poly_t that) const
#
#	return this->bits <= that.bits
#
#inline int  f2poly_t::operator>=(f2poly_t that) const
#
#	return this->bits >= that.bits
#
#inline void f2poly_t::increment(void)
#
#	this->bits++

#inline void f2poly_t::set_coeff(int deg, bit_t b)
#
#	this->bounds_check(deg)
#	if b.get_residue():
#		this->bits |= 1 << deg
#	else
#		this->bits &= ~(1 << deg)

##ifdef F2POLY_SMALL
#f2poly_t f2poly_t::ext_gcd(f2poly_t & that, f2poly_t & rm, f2poly_t & rn)
#
#	f2poly_t mprime, nprime, c, q, r, t, qm, qn
#	f2poly_t d    # Return value.
#
#	if *this == 0:
#		rm.bits = 0
#		rn.bits = 1
#		return that
#	if that == 0:
#		rm.bits = 1
#		rn.bits = 0
#		return *this
#
#	 Initialize
#	mprime.bits = 1
#	rn    .bits = 1
#	rm    .bits = 0
#	nprime.bits = 0
#	c = *this
#	d = that
#
#	while 1:
#
#		# Divide
#		# q = c / d, r = c % d
#		c.quot_and_rem(d, q, r)
#		# Note:  now c = qd + r and 0 <= r < d
#
#		# Remainder zero?
#		if r == 0:
#			break
#
#		# Recycle
#		c = d
#		d = r
#
#		t      = mprime
#		mprime = rm
#		qm     = q * rm
#		rm     = t - qm
#
#		t      = nprime
#		nprime = rn
#		qn     = q * rn
#		rn     = t - qn
#
#	return d
#
##endif

# ----------------------------------------------------------------
##ifndef F2POLY_SMALL
#f2poly_t f2poly_t::deriv(void)
#
#	f2poly_t rv = *this
#	rv.demote_1()
#	for (int i = 0; i < rv.num_parts; i++)
#		rv.parts[i] &= 0x55555555
#	rv.trim_parts()
#	return rv
#
##endif

# ----------------------------------------------------------------
# Relies on the fact that f(x^p) = f^p(x) over Fp[x].
#
# in  = a4 x^4 + a2 x^2 + a0
# out = a4 x^2 + a2 x   + a0
#
##ifndef F2POLY_SMALL
#int f2poly_t::square_root(f2poly_t & rroot)
#
#	int deg = this->degree()
#	f2poly_t root(0)
#
#	for (si = 0, di = 0; si <= deg; si+=2, di++):
#		if this->bit_at(si):
#			root.set_bit(di)
#		if this->bit_at(si + 1):
#			return 0
#
#
#	rroot = root
#	return 1
#
##endif

# ----------------------------------------------------------------
#int f2poly_t::eval(int c)
#
#	if c & 1:
#		return this->zcount_one_bits()
#	else
#		return this->parts[0] & 1

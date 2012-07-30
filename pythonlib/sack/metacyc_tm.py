#!/usr/bin/python -Wall

# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

import re
import sackint

# ================================================================
# Old explanation (circa 2004):

# ----------------------------------------------------------------
# Multiplication:
# a^i b^j  a^k b^l  =  a^(i + k t^j) b^(j + l)
# t   != 1 mod p
# t^q == 1 mod p

# ----------------------------------------------------------------
# Inversion:
# (a^i b^j)^(-1) = b^-j a^-i
#                = a^0 b^-j a^-i b^0
#                = a^(0 + -i t^-j) b^(-j + 0)
#                = a^(-i t^-j) b^-j

# ================================================================
# Alternate point of view, from scratch (2006-11-28):
# Zm X|_phi Zn (semidirect product):
#   (a, b) + (c, d) = (a + (phi(b))(c), b + d).
# Zm and Zn are cyclic so the action of b on c is specified by the action of
# Zn's 1 on Zm's 1.  Call this t.
#
# ----------------------------------------------------------------
# An example before I continue further:  Let m=7 and n=3.  Then we need phi to
# be a homomorphism from Z3 to Aut(Z7).  Here's what Aut(Z7) looks like:
#
# Z7 | s1 s2 s3 s4 s5 s6
# -- + -- -- -- -- -- --
#  0 |  0  0  0  0  0  0
#  1 |  1  2  3  4  5  6
#  2 |  2  4  6  1  3  5
#  3 |  3  6  2  5  1  4
#  4 |  4  1  5  2  6  3
#  5 |  5  3  1  6  4  2
#  6 |  6  5  4  3  2  1
#
# Note that si(x) = ix, i.e. the ith automorphism is just multiplication by i.
# Also, how do we compose automorphisms?  si(sj(x)) = ij(x) so si o sj is sij.
# So, arithmetic on the i's and j's is done in the multiplicative group of Z7.
#
# Now, Aut(Z7) is isomorphic to Z6, but how?  Additive groups of Zm always are
# cyclic of order m with 1 as generator; multiplicative groups of Zp* are
# always cyclic of order p-1, but with a generator we usually have to search
# for.  By searching we can find that 3 (or 5) generates Z7*.  So, Aut(Z7) is
# cyclic with automorphism s3 (or s5) as generator.  Here are the powers of 3
# mod 7:
#   3^1 3^2 3^3 3^4 3^5 3^6
#     3   2   6   4   5   1.
# So the cyclic structure of the cyclic group Aut(Z7) is
#    s3  s2  s6  s4  s5  s1
# with s3 as generator.  (If s5 is used as the generator, then the cycle
# structure is the reverse of this.)
#
# So, back to the semidirect product of Z7 and Z3, the possible homomorphisms
# from the order-3 cyclic group Z3 to the order-3 cyclic group Z7 are specified
# by the image of Z3's 1.  It can map to s1 (trivial homomorphism), s2
# (monomomorphism), or s4 (monomomorphism):
#
# Z3 | phi_1 phi_2 phi_3
# -- + ----- ----- -----
#  0 |    s1    s1    s1
#  1 |    s1    s2    s4
#  2 |    s1    s4    s2
#
# Since Z3 is cyclic, and since Aut(Z7) is cyclic, to specify phi we need only
# to specify the image of Z3's 1.  Call that st.
#
# Let c be in Z7 and b in Z3.  What is (phi(b))(c)?  Since phi is a
# homomorphism and Z3 is cyclic, written additively, phi(b) = b*phi(1).  Now,
# phi(1) is some automorphism st of Z7.  Moreover, it can't be any old
# automorphism: the order of st must divide the order of Z3's 1.  So, st^n must
# be the identity automorphism s1.  Since the arithmetic in Aut(Z7) is that of
# the multiplicative group Z7*, this means that t^n must be 1 mod m.
# ----------------------------------------------------------------



# ================================================================
# Auxiliary function:
# Second component of return value is t.
# First  compoment of return value is a flag indicating whether t was found.
def find_t(p, q):
	for t in range(2, p):
		if (sackint.intmodexp(t, q, p) == 1):
			return [1, t]
	return [0, 0]

# ================================================================
class metacyc_t:

	def __init__(self, i, j, p, q, t):

		tq = sackint.intmodexp(t, q, p)
		if ((tq % p) != 1):
			print "metacyc:  t^q must be 1 mod p"
			print "Got p =", p, "q =", q, "t =", t
			raise RuntimeError

		# xxx jrk 2006-11-28 allow trivial homomorphisms.
		#if ((t % p) == 1):
		#	print "metacyc:  t must not be 1 mod p"
		#	print "Got p =", p, "q =", q, "t =", t
		#	raise RuntimeError

		self.i = i % p
		self.j = j % q
		self.p = p
		self.q = q
		self.t = t

	def __eq__(a,b):
		return ((a.i == b.i) and (a.j == b.j))

	def __ne__(a,b):
		return not (a == b)

	def __mul__(a,b):
		if ((a.p != b.p) or (a.q != b.q) or (a.t != b.t)):
			print "Parameter mismatch in metacyc mul"
			raise RuntimeError
		ci = (a.i + b.i * sackint.intmodexp(a.t, a.j, a.p)) % a.p
		cj = (a.j + b.j) % a.q
		c = metacyc_t(ci, cj, a.p, a.q, a.t)
		return c

	def inv(a):
		ci = -a.i * sackint.intmodexp(a.t, -a.j, a.p)
		cj = -a.j
		c = metacyc_t(ci, cj, a.p, a.q, a.t)
		return c

	def scan(self, string, argp, argq, argt):
		groups = re.match(r"^(\d)+,(\d+)$", string).groups();
		if len(groups) != 2:
			raise IOError
		self.__init__(int(groups[0]), int(groups[1]), argp, argq, argt)

	def __str__(self):
		return str(self.i) + "," + str(self.j)

	def __repr__(self):
		return self.__str__()

def params_from_string(params_string):
	pqt = re.split(',', params_string)

	if (len(pqt) == 3):
		p = int(pqt[0])
		q = int(pqt[1])
		t = int(pqt[2])
	elif (len(pqt) == 2):
		p = int(pqt[0])
		q = int(pqt[1])
		[got_it, t] = find_t(p, q)
		if (not got_it):
			print "metacyc_t:  No t found for p =", p, "q =", q
			print "Got: ", params_string
			raise IOError
	else:
		print "metacyc_tm.from_string:  expected parameters p,q or p,q,t."
		print "Got: ", params_string
		raise IOError
	return [p, q, t]

def from_string(value_string, params_string):
	[p, q, t] = params_from_string(params_string)
	obj = metacyc_t(0, 0, p, q, t)
	obj.scan(value_string, p, q, t)
	return obj

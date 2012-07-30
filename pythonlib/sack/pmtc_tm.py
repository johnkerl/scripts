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
import sys
import random
import sackint
import sackmat_m

# Permutations with cycle-decomposition I/O.

# Python arrays are zero-up.  Permutations are almost universally taken
# to be on the set {1, 2, 3, ..., n}.  So, elements[0] is always 0;
# elements[1] through elements[n] are images.

# Naming convention:
# * Something called "images" is an externally visible list of the
#   form [3, 1, 2, 4].
# * Something called "zimages" is an internal list of the
#   form [0, 3, 1, 2, 4].

# ================================================================
class pmtc_t:

	def __init__(self, images, n):
		if (len(images) != n):
			raise RuntimeError
		self.n = n
		self.zimages = [0] + copy.copy(images)

	def __eq__(a,b):
		return (a.zimages == b.zimages)

	def __ne__(a,b):
		return (a.zimages != b.zimages)

	# For sorting and display purposes.
	# Return -1 if a <  b;
	# return  0 if a == b;
	# return +1 if a >  b.
	# Compare lexically on cycle types.
	# Break ties within cycle type by lexical compare on image maps.
	def __cmp__(a,b):
		cta = a.cycle_type()
		ctb = b.cycle_type()
		m = len(cta)
		for i in range(0, m):
			if (cta[i] < ctb[i]):
				return -1
			if (cta[i] > ctb[i]):
				return  1
		n = a.n
		for i in range(1, n+1):
			azi = a.zimages[i]
			bzi = b.zimages[i]
			if (azi < bzi):
				return -1
			if (azi > bzi):
				return  1
		return 0

	def __mul__(a,b):
		if (a.n != b.n):
			raise RuntimeError
		c = pmtc_t(range(1, a.n+1), a.n)
		for i in range(1, a.n+1):
			c.zimages[i] = a.zimages[b.zimages[i]]
		return c

	def check_permutation(self):
		test = copy.copy(self.zimages)
		test.sort()
		for i in range(1, self.n+1):
			if (test[i] != i):
				print "Not a permutation:", self.zimages
				print "Test:", test
				raise RuntimeError

	def inv(a):
		c = pmtc_t(range(1, a.n+1), a.n)
		for i in range(1, c.n+1):
			c.zimages[a.zimages[i]] = i
		return c

	def __getitem__(self, i):
		if (i == 0):
			print "pmtc: zimage[0] is protected."
			raise RuntimeError
		return self.zimages[i]

	# Left group action on a specified set.  The set is indexed zero-up,
	# though.
	def of(self, input):
		output = copy.copy(input)
		for i in range(1, len(self.zimages)):
			output[i-1] = input[self.zimages[i]-1]
		return output

	# Example:
	# ( 1 2 3 4 5 6 ) <-- src
	# ( 4 3 1 2 6 5 ) <-- dst
	# Want inverse of 2 which is 4.  Search for the src which maps to dst=2.

	def inv_img(self, dst):
		for src in range(1, self.n+1):
			if self.zimages[src] == dst:
				return src
		print >> sys.stderr, "pmtc.inv_img: inverse not found."
		print >> sys.stderr, "input       = ", dst
		print >> sys.stderr, "permutation = ", self
		sys.exit(1)


	def sgn(self):
		numers = 1
		denoms = 1
		n = self.n
		for i in range(1, n+1):
			si = self.zimages[i]
			for j in range(i+1, n+1):
				sj = self.zimages[j]
				numer   = sj - si
				denom   =  j -  i
				numers *= numer
				denoms *= denom
		return numers/denoms

	def parity(self):
		if self.sgn() == 1:
			return 0
		else:
			return 1


	# Bubble sort and count the swaps.
	def oldparity(self):
		nswap = 0
		n = len(self.zimages) - 1
		imsort = copy.copy(self.zimages)
		top = n
		while (top > 0):
			for i in range(1, top):
				if (imsort[i] > imsort[i+1]):
					temp = imsort[i]
					imsort[i] = imsort[i+1]
					imsort[i+1] = temp
					nswap += 1
			top -= 1
		return nswap & 1

	def oldsgn(self):
		if (self.parity() == 0):
			return  1
		else:
			return -1

	# Example:  images are [3, 1, 2, 4].
	# I.e.
	# [1 2 3 4]
	# [3 1 2 4]
	#
	# Returns [[1, 3, 2], [4]]

	def cycle_decomposition(self):
		n = self.n
		cd = []
		marks = [0] * (n+1)
		for i in range(1, n+1):
			if (marks[i]):
				continue
			cycle = []
			next = i
			marks[next] = 1
			while (1):
				cycle = cycle + [next]
				next = self.zimages[next]
				if (next == i):
					break
				marks[next] = 1
			cd = cd + [cycle]
		return cd

	def cycle_type(self):
		cd = self.cycle_decomposition()
		ct = map(len, cd)
		ct.sort(reverse=True)
		return ct


	# Algorithm for transposition decomposition:
	# Find the smallest i such that sigma(i) != i.
	#   If there is no such, we are done.
	# Form the transposition tau which swaps i and sigma(i).
	# Set sigma := tau * sigma.
	# Repeat.
	# The decomposition is tau_1 * tau_2 * ... .

	# Example:
	# Given sigma = 
	#   [1 2 3 4]
	#   [2 3 4 1],
	# returns
	# [2,1,3,4, 1,3,2,4, 1,2,4,3]

	def transposition_decomposition(self):
		taus = []
		n = self.n
		id_imgs = range(1, n+1)
		sigma = pmtc_t(self.zimages[1:], n)
		done = False
		while not done:
			# Find the smallest i such that sigma(i) != i.
			#   If there is no such, we are done.
			i = -1
			for k in range(1, n+1):
				if sigma.zimages[k] != k:
					i = k
					break
			if i == -1:
				done = True
				break
			# Form the transposition tau which swaps i and sigma(i).
			tau = pmtc_t(id_imgs, n)
			j = sigma.zimages[i]
			tau.zimages[i] = j
			tau.zimages[j] = i
			taus.append(tau)
			# Set sigma := tau * sigma.
			sigma = tau * sigma
			# Repeat.
		return taus

	# e.g. 1,2:3,4
	# xxx this method needs some comments. :)
	def scan(self, cycles_string, n):
		zimages = range(0, n+1)
		cycle_strings = re.split(':', cycles_string)

		# Loop over cycles, e.g. given 1,2:3,4, we have 3,4 and 1,2.
		# (Composition goes from right to left so we have to loop backward.)
		num_cycles = len(cycle_strings)
		cidx = num_cycles - 1
		while (cidx >= 0):
			cycle_string = cycle_strings[cidx]
			index_strings = re.split(',', cycle_string)
			indices = []
			for index_string in index_strings:
				indices.append(int(index_string))

			# Parse one cycle.
			# Note that (a b c d) is the same as (a d)(a c)(a b).
			num_indices = len(indices)
			k = num_indices-1
			while (k > 0):
				# WARNING!  This swap logic doesn't work right if the cycles
				# aren't disjoint.
				temp = zimages[indices[0]]
				zimages[indices[0]] = zimages[indices[k]]
				zimages[indices[k]] = temp
				k -= 1

			cidx -= 1

		images = zimages[1:]
		self.__init__(images, n)
		self.check_permutation()


	# e.g. [[1,2],[3,4]]
	# xxx this method also needs some comments. :)
	def cycle_fill(self, cycles, n):
		zimages = range(0, n+1)
		# Loop over cycles, e.g. given [[1,2],[3,4]] we have [3,4] and [1,2].
		# (Composition goes from right to left so we have to loop backward.)
		num_cycles = len(cycles)
		cidx = num_cycles - 1
		while (cidx >= 0):
			cycle = cycles[cidx]
			# Apply one cycle.
			# Note that (a b c d) is the same as (a d)(a c)(a b).
			num_indices = len(cycle)
			k = num_indices-1
			while (k > 0):
				# WARNING!  This swap logic doesn't work right if the cycles
				# aren't disjoint.
				temp = zimages[cycle[0]]
				zimages[cycle[0]] = zimages[cycle[k]]
				zimages[cycle[k]] = temp
				k -= 1

			cidx -= 1

		images = zimages[1:]
		self.__init__(images, n)
		self.check_permutation()

	# xxx make a fcn to map an image list to a cycle decomposition.
	# THEN, a fcn to print a cycle decomposition.

	def __str__(self):
		cd = self.cycle_decomposition()
		num_non_trivial_cycles = 0
		cd_string = ""
		for cycle in cd:
			if (len(cycle) > 1):
				num_non_trivial_cycles += 1
			else:
				continue
			cycle_string = str(cycle[0])
			cycle_len = len(cycle)
			for j in range(1, cycle_len):
				cycle_string += ","
				cycle_string += str(cycle[j])

			if (num_non_trivial_cycles > 1):
				cd_string += ":"
			cd_string += cycle_string

		if (num_non_trivial_cycles == 0):
			#cd_string = "[]"
			cd_string = "1"
		return cd_string

	def __repr__(self):
		return self.__str__()

	# Example:
	# * permutation = [1, 2] [3, 4, 5]
	# * zimages = [0, 2, 1, 4, 5, 3]
	# * P = 0 1 0 0 0
	#       1 0 0 0 0
	#       0 0 0 1 0
	#       0 0 0 0 1
	#       0 0 1 0 0

	def to_permutation_matrix(self):
		n = self.n
		P = sackmat_m.make_zero_matrix(n, n)
		for i in range(1, n+1):
			j = self.zimages[i]
			P[i-1][j-1] = 1
		return P

def from_cycles(cycles, n):
	obj = pmtc_t(range(1, n+1), n)
	obj.cycle_fill(cycles, n)
	return obj

def from_cycle(cycle, n):
	obj = pmtc_t(range(1, n+1), n)
	obj.cycle_fill([cycle], n)
	return obj

# Example:  [3 2 1] --> ((1 2 3)(4 5)(6))
def from_cycle_type(ct):
	# Create cycles of the specified type.
	n = 0
	k = 1
	cycles = []
	for elt in ct:
		cycle = range(k, k+elt)
		cycles.append(cycle)
		k += elt
		n += elt
	return from_cycles(cycles, n)

def cycle_type_reps(n):
	ptns = sackint.ptns(n)
	reps = []
	for ptn in ptns:
		reps.append(from_cycle_type(ptn))
	return reps

# Auxiliary function.
# Converts a list of sorted numbers into a list of pairs of elements and
# repetition counts.  Example( with commas suppressed):
# [4 4 4  3 3 3 3 3  2  1 1] -> [[4 3] [3 5] [2 1] [1 2]]
def type_to_counts(ct):
	if (ct == []):
		return []
	pairs = []
	previous = ct[0]
	count = 0
	for e in ct:
		if (e == previous):
			count +=1
		else:
			pairs.append([previous, count])
			previous = e
			count = 1
	pairs.append([previous, count])
	return pairs

# Counts the number of permutations in Sn which share a given
# cycle type.  This is best explained by example.
# * Cycle type = [3 2 2]
# * I have 7 boxes to fill: [ _ _ _ | _ _ | _ _ ].
# * There are 7! = 5040 ways to put the numbers 1-7 in those
#   boxes.
# * This overcounts.  For example, [1 2 3][4 5][6 7]
#   is equivalent to [2 3 1][4 5][6 7] -- these are the same
#   permutation.  Likewise [1 2 3][4 5][6 7] is the same
#   permutation as [1 2 3][6 7][4 5].
# * Divide 5040 by 3*2*2, to count cyclic shifts within a cycle.
# * Divide by 2!, since adjacent two-cycles can be transposed.
#   E.g. (1 2 3)(4 5)(6 7) is equivalent to (1 2 3)(6 7)(4 5).

def num_ct_reps(ct):
	# Find n
	n = 0
	for e in ct:
		n += e

	# Find n!
	rv = sackint.factorial(n)

	# Account for cyclic shifts within cycles.
	for e in ct:
		rv /= e

	# Account for permutations of same-length cycles.
	pairs = type_to_counts(ct)
	for pair in pairs:
		rv /= sackint.factorial(pair[1])

	return rv

# ----------------------------------------------------------------
def params_from_string(params_string):
	n = int(params_string)
	return n

def from_string(value_string, params_string):
	n = params_from_string(params_string)
	obj = pmtc_t(range(1, n+1), n)
	obj.scan(value_string, n)
	return obj

def kth_pmtc(k, n, nfact):
	nifact = nfact
	images = range(0, n)
	temp   = range(0, n+1)

	ni = n
	for pos in range(0, n):
		nifact /= ni
		r = k % nifact
		q = k / nifact
		k = r

		images[pos] = temp[q] + 1
		del temp[q]

		ni -= 1
	return pmtc_t(images, n)

def identity_pmtc(n):
	return pmtc_t(range(1, n+1), n)

# ================================================================
# rand_pmtc:  returns a permutation on N symbols, uniformly distributed on S_N.

# ----------------------------------------------------------------
# Idea:
# * Start with a pool of N unused images.
# * For the image of 1, select an image at random from the N choices.
# * For the image of 2, select an image from the remaining N-1 choices.
# * ...
# * For the image of N-1, select from the remaining 2 choices.
# * The image of N has only one choice left.
#
# ----------------------------------------------------------------
# Example:  N=4.  Image map and unused images are:
#
#   [ 1 2 3 4 ]
#   [ ? ? ? ? ]      [ 1 2 3 4 ] <-- unused.
#
# Image of 1:  select 2 from [ 1 2 3 4].
#
#   [ 1 2 3 4 ]
#
# Image of 2:  select 3 from [1 3 4].
#
#   [ 1 2 3 4 ]
#   [ 2 3 ? ? ]      [ 1 4 ] <-- unused.
#
# Image of 3:  select 1 from [1 4].
#
#   [ 1 2 3 4 ]
#   [ 2 3 1 ? ]      [ 4 ] <-- unused.
#
# Image of 4:  select 4 from [4].
#
#   [ 1 2 3 4 ]
#   [ 2 3 1 4 ]      [ ] <-- unused.
#
# Done.
#
# ----------------------------------------------------------------
# This is easy to do.  The only question is how to do it efficiently -- without
# lots of data movement and/or unnecessary memory allocation.
#
# The pool of unused images could be an array of length N ... yet I already
# *have* an array of length N which is the permutation's images[] array.  I can
# visualize the used and unused images as simply a concatenation.  E.g.  after
# selecting the image of 2, the pipe separates the used from the unused:
#
#   [ 1 2 3 4 ]
#   [ 2 3|1 4 ]
#
# Then selecting an unused image for k amounts to choosing a pseudorandom
# integer uniformly between 0 and N-k-1; applying that image amounts to doing
# a swap.

def rand_pmtc(N):
	zimages = range(0, N+1)
	unused_start = 1
	num_unused   = N

	for k in range(1, N+1):
		#print "-- [",
		#for j in range(0, N+1):
		#	if (j == k):
		#		print "|",
		#	else:
		#		print " ",
		#	print "%2d" % (zimages[j]),
		#print " ]"

		# Select a pseudorandom element from the pool of unused images.
		# Python's randint(a, b) includes both endpoints.
		u = random.randint(unused_start, unused_start + num_unused - 1)

		# Swap it into place.
		temp       = zimages[u]
		zimages[u] = zimages[k]
		zimages[k] = temp

		# Decrease the size of the pool by 1.
		# (Yes, unused_start and k always have the same value.  Using two
		# variables wastes neglible memory and makes the code easier to
		# understand.)
		unused_start += 1
		num_unused   -= 1

	return pmtc_t(zimages[1:], N)

# ----------------------------------------------------------------
# Auxiliary routine for sort_pmtcs() below.
#
# Return -1 if a <  b;
# return  0 if a == b;
# return +1 if a >  b.
# Compare lexically on cycle types.
# Break ties within cycle type by lexical compare on image maps.

def pmtc_cmp(ta, tb):
	# Compare number of cycles
	nca = ta[2]
	ncb = tb[2]
	if (nca < ncb):
		return  1
	if (nca > ncb):
		return -1

	# Compare lengths of cycles
	cta = ta[1]
	ctb = tb[1]
	for i in range(0, nca):
		if (cta[i] < ctb[i]):
			return  1
		if (cta[i] > ctb[i]):
			return -1

	# Compare image maps
	pmta = ta[0]
	pmtb = tb[0]
	n    = pmta.n
	for i in range(1, n+1):
		azi = pmta.zimages[i]
		bzi = pmtb.zimages[i]
		if (azi < bzi):
			return  1
		if (azi > bzi):
			return -1

	return 0

# ----------------------------------------------------------------
# This could be done using __cmp__ but this is faster:  I compute
# cycle types once and for all, rather than on every compare.
#
# Make a list of triples of permutations, cycle types, and number of cycles.

def sort_pmtcs(list):
	m = len(list)

	pairs = []
	for pmt in list:
		ct = pmt.cycle_type()
		pairs.append([pmt, ct, len(ct)])
	pairs.sort(pmtc_cmp)

	for i in range(0, m):
		list[i] = pairs[i][0]

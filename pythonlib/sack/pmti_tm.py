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
import random
import sackint
import uniqc_m

# Permutations with image-map I/O.

class pmti_t:

	# Python arrays are zero-up.  Permutations are almost universally taken
	# to be on the set {1, 2, 3, ..., n}.  So, elements[0] is always 0;
	# elements[1] through elements[n] are images.

	# Naming convention:
	# * Something called "images" is an externally visible list of the
	#   form [3, 1, 2, 4].
	# * Something called "zimages" is an internal list of the
	#   form [0, 3, 1, 2, 4].

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
		c = pmti_t(range(1, a.n+1), a.n)
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
		c = pmti_t(range(1, a.n+1), a.n)
		for i in range(1, c.n+1):
			c.zimages[a.zimages[i]] = i
		return c

	def scan(self, images_string, n):
		image_strings = re.split(',', images_string)
		n = len(image_strings)
		images = range(0, n)
		for i in range(0, n):
			images[i] = int(image_strings[i])
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
				# WARNING!  This swap logic doesn't work right if the cycles aren't disjoint.
				temp = zimages[cycle[0]]
				zimages[cycle[0]] = zimages[cycle[k]]
				zimages[cycle[k]] = temp
				k -= 1

			cidx -= 1

		images = zimages[1:]
		self.__init__(images, n)
		self.check_permutation()

	def __str__(self):
		string = str(self.zimages[1])
		for i in range(2, len(self.zimages)):
			string += "," + str(self.zimages[i])
		return string

	def __repr__(self):
		return self.__str__()

	def __getitem__(self, i):
		if (i == 0):
			print "pmti: zimage[0] is protected."
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
		print >> sys.stderr, "pmti.inv_img: inverse not found."
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

	# Omits one-cycles.
	def cycle_decomposition_non_triv(self):
		cd = self.cycle_decomposition()
		rv = []
		for cycle in cd:
			if (len(cycle) > 1):
				rv.append(cycle)
		return rv

	def cycle_type(self):
		cd = self.cycle_decomposition()
		ct = map(len, cd)
		ct.sort(reverse=True)
		return ct

	# For a permutation pi on n symbols, returns a (zero-up) list the kth
	# element of which is the number of cycles in pi of length k.  There's no
	# such thing as a 0-cycle but the 0 slot is set to 0.
	#
	# Example:
	#
	# * Cycle decomposition is (1) (2) (3) (4) (5 6) (7 8) (9 10 11)
	#
	# * Cycle type is [3 2 2 1 1 1 1]
	#
	# * Cycle counts are [0 4 2 1 0 0 0 0 0 0 0 0]
	#   meaning that there are 4 1-cycles, 2 2-cycles, and 1 3-cycle, and no
	#   cycles of any other length.

	def cycle_counts(self):
		n = self.n
		counts = [0] * (n+1)
		marks  = [0] * (n+1)
		for i in range(1, n+1):
			if (marks[i]):
				continue
			cycle_length = 0
			next = i
			marks[next] = 1
			while (1):
				cycle_length += 1
				next = self.zimages[next]
				if (next == i):
					break
				marks[next] = 1
			counts[cycle_length] += 1
		return counts

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
		sigma = pmti_t(self.zimages[1:], n)
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
			tau = pmti_t(id_imgs, n)
			j = sigma.zimages[i]
			tau.zimages[i] = j
			tau.zimages[j] = i
			taus.append(tau)
			# Set sigma := tau * sigma.
			sigma = tau * sigma
			# Repeat.
		return taus

def from_cycles(cycles, n):
	obj = pmti_t(range(1, n+1), n)
	obj.cycle_fill(cycles, n)
	return obj

def from_cycle(cycle, n):
	obj = pmti_t(range(1, n+1), n)
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

def params_from_string(params_string):
	n = int(params_string)
	return n

def from_string(value_string, params_string):
	n = params_from_string(params_string)
	obj = pmti_t(range(1, n+1), n)
	obj.scan(value_string, n)
	return obj

def identity_pmti(n):
	return pmti_t(range(1, n+1), n)

def kth_pmti(k, n, nfact):
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
		for i in range(q, ni):
			temp[i] = temp[i+1]

		ni -= 1
	return pmti_t(images, n)

# ================================================================
# rand_pmti:  returns a permutation on N symbols, uniformly distributed on S_N.

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

def rand_pmti(N):
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

	return pmti_t(zimages[1:], N)

# ----------------------------------------------------------------
# Auxiliary routine for sort_pmtis() below.
#
# Return -1 if a <  b;
# return  0 if a == b;
# return +1 if a >  b.
# Compare lexically on cycle types.
# Break ties within cycle type by lexical compare on image maps.

def pmti_cmp(ta, tb):
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

def sort_pmtis(list):
	m = len(list)

	pairs = []
	for pmt in list:
		ct = pmt.cycle_type()
		pairs.append([pmt, ct, len(ct)])
	pairs.sort(pmti_cmp)

	for i in range(0, m):
		list[i] = pairs[i][0]

#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2005-01-11
# (Ported to Python 2006-03-06)
#
# This is a radix-2 fast Fourier transform.
# This file contains the library routines.  The I/O wrapper is the file pyfft.
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
import sys
import copy
import re
from   math import *

# ----------------------------------------------------------------
def half_trig_table(n, forward):
	W = []
	for i in range(0, int(n/2)):
		arg = 2.0 * pi * i / n
		if (forward):
			arg = -arg
		W.append(cos(arg) + sin(arg)*1j)
	return W

# ----------------------------------------------------------------
def full_trig_table(n, forward):
	W = []
	for i in range(0, n):
		arg = 2.0 * pi * i / n
		if (forward):
			arg = -arg
		W.append(cos(arg) + sin(arg)*1j)
	return W

# ----------------------------------------------------------------
# u is input
# v is output

def fft(u, fold_in, fold_out, forward, scale):
	v = copy.copy(u)
	n = len(v)
	n2 = n / 2
	log2n = log2(n)
	sqrt_recip_2 = sqrt(0.5)

	if (not is_a_power_of_two(n)):
		print "pyfft_m:  input length", n, "is not a power of two."

	W = half_trig_table(n, forward)

	# Output folding.
	if (fold_out):
		j = 1
		for i in range(0, n2):
			v[j] = -v[j]
			j += 2

	# Bit-reverse stage.
	for i in range(0, n):
		ir = bit_reverse(i, log2n)
		if (i < ir):
			temp  = v[i]
			v[i]  = v[ir]
			v[ir] = temp

	#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	# Radix-two stages.
	#
	# y00 \ / @    \ / @    \ / @    \ / Y00
	# y08 / \ @    \ / @    \ / @    \ / Y01
	# y04 \ / @ W0 / \ @    \ / @    \ / Y02
	# y12 / \ @ W4 / \ @    \ / @    \ / Y03
	#
	# y02 \ / @    \ / @ W0 / \ @    \ / Y04
	# y10 / \ @    \ / @ W2 / \ @    \ / Y05
	# y06 \ / @ W0 / \ @ W4 / \ @    \ / Y06
	# y14 / \ @ W4 / \ @ W6 / \ @    \ / Y07
	#
	# y01 \ / @    \ / @    \ / @ W0 / \ Y08
	# y09 / \ @    \ / @    \ / @ W1 / \ Y09
	# y05 \ / @ W0 / \ @    \ / @ W2 / \ Y10
	# y13 / \ @ W4 / \ @    \ / @ W3 / \ Y11
	#
	# y03 \ / @    \ / @ W0 / \ @ W4 / \ Y12
	# y11 / \ @    \ / @ W2 / \ @ W5 / \ Y13
	# y07 \ / @ W0 / \ @ W4 / \ @ W6 / \ Y14
	# y15 / \ @ W4 / \ @ W6 / \ @ W7 / \ Y15
	#
	# a   \ / c   --> c := a + b
	# b   / \ d   --> d := a - b
	#
	# a   \ / c   --> c := a + w * b
	# b w / \ d   --> d := a - w * b
	#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

	num_flocks = int(n/2)
	flock_sep  = 2
	bperflock  = 1
	wingspan   = 1
	twiddle_stride = int(n/2)
	stageno = 0
	fno = 0
	bno = 0
	twiddleidx = 0
	num_stages = log2n

	for stageno in range(0, num_stages):
		for fno in range(0, num_flocks):
			twiddleidx = 0

			for bno in range(0, bperflock):
				upperidx = fno * flock_sep + bno
				loweridx = upperidx + wingspan

				a  = v[upperidx]
				b  = v[loweridx]
				w  = W[twiddleidx]
				wb = w * b
				c  = a + wb
				d  = a - wb

				if (scale):
					c *= sqrt_recip_2
					d *= sqrt_recip_2

				v[upperidx] = c
				v[loweridx] = d

				twiddleidx += twiddle_stride

		num_flocks     >>= 1
		flock_sep      <<= 1
		bperflock      <<= 1
		wingspan       <<= 1
		twiddle_stride >>= 1

	# Input folding.
	if (fold_in):
		j = 1
		for i in range(0, n2):
			v[j] = -v[j]
			j += 2

	return v

# ----------------------------------------------------------------
# u is input
# t is temp input
# v is output

def dft(u, fold_in, fold_out, forward, scale):
	t = copy.copy(u)
	v = copy.copy(u)
	n = len(v)
	n2 = int(n/2)

	W = full_trig_table(n, forward)

	# Output folding.
	if (fold_out):
		if (n & 1):
			print >> sys.stderr, "pyfft_m.dft:  cannot fold output with odd vector length", n
			sys.exit(1)
		j = 1
		for i in range(0, n2):
			t[j] = -t[j]
			j += 2

	# DFT per se
	for k in range(0, n):
		sum = 0
		for j in range(0, n):
			sum += W[(k*j) % n] * t[j]
		v[k] = sum

	if (scale):
		s = 1.0 / sqrt(n)
		for k in range(0, n):
			v[k] *= s

	# Input folding.
	if (fold_in):
		if (n & 1):
			print >> sys.stderr, "pyfft_m.dft:  cannot fold input with odd vector length", n
			sys.exit(1)
		j = 1
		for i in range(0, n2):
			v[j] = -v[j]
			j += 2

	return v

# ----------------------------------------------------------------
def bit_reverse(input, num_bits):
	output = input

	output = ((output & 0xaaaaaaaa) >>  1) | ((output & 0x55555555) <<  1)
	output = ((output & 0xcccccccc) >>  2) | ((output & 0x33333333) <<  2)
	output = ((output & 0xf0f0f0f0) >>  4) | ((output & 0x0f0f0f0f) <<  4)
	output = ((output & 0xff00ff00) >>  8) | ((output & 0x00ff00ff) <<  8)
	output = ((output & 0xffff0000) >> 16) | ((output & 0x0000ffff) << 16)

	output >>= (32 - num_bits)

	return output & ((1 << num_bits) - 1)

# ----------------------------------------------------------------
def log2(n):
	rv = 0
	nsave = n

	if (n == 0):
		print >> sys.stderr, "log2:  Can't take logarithm of zero."
		sys.exit(1)

	while (n != 1):
		n >>= 1
		rv += 1

	if (nsave != (1 << rv)):
		print >> sys.stderr, "Argument", nsave, "is not a power of two."
		sys.exit(1)

	return rv

# ----------------------------------------------------------------
def is_a_power_of_two(n):
	if (n == 0):
		return 0
	if ((n & (n - 1)) == 0):
		return 1
	return 0

#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2008-01-31
# ================================================================
from __future__ import division # 1/2 = 0.5, not 0.

# ----------------------------------------------------------------
# Example:
# * input = [1, 2, 3, 4, 5]
# * window_size = 2
# * output = [ (1+2)/2, (2+3)/2, (3+4)/2, (4+5)/2 ]

def smoother(input, window_size):
	input_size = len(input)
	output_size = input_size - window_size + 1
	output = [0.0] * output_size

	# This is correct, but inefficient:  it computes things over and over.
	#for k in range(0, output_size):
	#	output[k] = 0.0
	#	for j in range(0, window_size):
	#		output[k] += input[k+j]
	#	output[k] *= (1.0 / window_size)


	# First, compute the first window sum.
	# +-+-+-+-+-+-+-+-+-+-+
	# |#|#|#|#| | | | | | |
	# +-+-+-+-+-+-+-+-+-+-+
	#  |     /
	#  |    /
	#  |   /
	#  |  /
	#  v v
	#  +-+
	#  |#|
	#  +-+

	# Let i index the input and j index the output.
	sum = 0.0
	scale = 1.0 / window_size
	i = 0
	j = 0
	while (i < window_size):
		sum += input[i]
		i += 1

	# Second, update windows.  Add the leading sample and subtract the
	# trailing one.
	while (i < input_size):
		output[j] = sum * scale
		sum -= input[j]
		sum += input[i]
		i += 1
		j += 1

	# Last sample
	output[j] = sum * scale

	return output

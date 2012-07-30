#!/usr/bin/python -Wall

# ================================================================
# Given a list, returns a list of pairs of elements and repetition counts.
# Example (with commas elided for legibility):
#
#   Input:  [ 1 1 1 2 2 3 3 3 3 5 5 1 1 ]
#   Output: [ [3 1] [2 2] [4 3] [2 5] [2 1] ]
#
# I.e. there is a run of 3 1's, then a run of 2 2's, then a run of 4 3's, then
# 2 5's, then 2 1's.  This similar to the output of the Unix "uniq -c" command,
# if the input were one number per line.  However, uniq -c puts the columns in
# reverse order from what I do here.
# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2008-01-22
# ================================================================

def uniqc(list):
	rv = []
	n = len(list)

	if (n == 0):
		return []

	curri = 0
	nexti = 1
	head  = list[curri]
	count = 1

	while (curri < n):
		if (nexti == n): # Last element in the list
			if (list[curri] == head):
				rv.append([head, count])
			else:
				rv.append([list[curri], 1])
		elif (list[curri] == list[nexti]):
			count += 1
		else:
			rv.append([head, count])
			head = list[nexti]
			count = 1
		curri += 1
		nexti += 1

	return rv

# ----------------------------------------------------------------
# Test cases:

#def test1(list):
#	#print list
#	#print uniqc(list)
#	#print
#
#	# Pipe the output to, say, expand -20.
#	print list, "\t", uniqc(list)
#
#def test_uniqc():
#	test1([])
#	test1([8])
#	test1([8, 8])
#	test1([8, 9])
#	test1([9, 8])
#	test1([9, 9])
#	test1([8, 8, 8])
#	test1([8, 8, 9])
#	test1([8, 9, 8])
#	test1([8, 9, 9])
#	test1([9, 8, 8])
#	test1([9, 8, 9])
#	test1([9, 9, 8])
#	test1([9, 9, 9])
#
#test_uniqc()

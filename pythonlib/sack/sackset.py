
# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

# ----------------------------------------------------------------
def print_set_as_column(S):
	for a in S:
		print a

# ----------------------------------------------------------------
def print_set_as_row(S):
	for a in S:
		print a,
	print

# ----------------------------------------------------------------
def element_of(x, S):
	for a in S:
		if (a == x):
			return 1
	return 0

# ----------------------------------------------------------------
def subset_of(T, S):
	for t in T:
		if (not element_of(t, S)):
			return 0
	return 1

# ----------------------------------------------------------------
def set_append_unique(S, x):
	if (not element_of(x, S)):
		S.append(x)


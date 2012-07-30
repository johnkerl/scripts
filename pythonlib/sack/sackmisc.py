#!/usr/bin/python -Wall

# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

from sackall_m import *

# ----------------------------------------------------------------
def foo1():
	G1 = v4_gm.get_elements_str("");
	G2 = v4_gm.get_elements_str("");

	G3 = direct_product(G1, G2)
	print_cayley_table(G3)

# ----------------------------------------------------------------
def foo2():
	G = [quatu_tm.from_string("i", ""), quatu_tm.from_string("j", "")]

	close_group(G)
	print_set_as_column(G)

# ----------------------------------------------------------------
def foo3():
	G = quatu_gm.get_elements_str("")
	H = [quatu_tm.quatu_t(0), quatu_tm.quatu_t(1)];
	print "G:"
	print_set_as_column(G)
	print
	print "H:"
	print_set_as_column(H)
	print
	print "G/H:"
	GH = quotient(G, H)
	print_set_as_column(GH)

# ----------------------------------------------------------------
def foo4():

	G = quatu_gm.get_elements_str("")
	print "G:"
	print_set_as_column(G)
	print

	H = [quatu_tm.quatu_t(0), quatu_tm.quatu_t(1)];
	print "H:"
	print_set_as_column(H)
	print

	GH = quotient(G, H)
	print "G/H:"
	print_set_as_column(GH)
	print

	K = v4_gm.get_elements_str("");
	print "K:"
	print_set_as_column(K)
	print

	G3 = direct_product(GH, K)
	print "G/H x K:"
	print_set_as_column(G3)
	print

	#print_cayley_table(G3)
	print "Z(G/H x K):"
	Z = get_center(G3)
	print_set_as_column(Z)
	print

# ----------------------------------------------------------------
def foo5():
	G = T_gm.get_elements_str("")
	for x in G:
		y = x.inv()
		xy = x*y
		yx = y*x
		print x, y, xy, yx

# ----------------------------------------------------------------
foo1()

#!/usr/bin/python

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2005-01-11
#
# This is an Lagrange-interpolation module.
#
# Example using degree 3:
# Given x_0 .. x_3, y_0 .. y_3, compute the polynomial
#
#              (x - x_1)(x - x_2)(x - x_3)
# y_0 ------------------------------------ +
#              (x_0-x_1)(x_0-x_2)(x_0-x_3)
#
#     (x - x_0)         (x - x_2)(x - x_3)
# y_1 ------------------------------------ +
#     (x_1-x_0)         (x_1-x_2)(x_1-x_3)
#
#     (x - x_0)(x - x_1)         (x - x_3)
# y_2 ------------------------------------ +
#     (x_2-x_0)(x_2-x_1)         (x_2-x_3)
#
#     (x - x_0)(x - x_1)(x - x_2)
# y_3 ------------------------------------
#     (x_3-x_0)(x_3-x_1)(x_3-x_2)
#
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
from math     import *
from kerlutil import *

# ----------------------------------------------------------------
# Cubic case:
# c0 = y0 / (          (x0-x1)*(x0-x2)*(x0-x3))
# c1 = y1 / ((x1-x0)          *(x1-x2)*(x1-x3))
# c2 = y2 / ((x2-x0)*(x2-x1)          *(x2-x3))
# c3 = y3 / ((x3-x0)*(x3-x1)*(x3-x2))

def li_make_coeffs_from_xs_and_ys(xs, ys):
	n = len(xs)
	cs = [0] * n
	for i in range(0, n):
		denom = 1.0
		for j in range(0, n):
			if (i != j):
				denom *= xs[i] - xs[j]
		cs[i] = ys[i] / denom
	return cs

# ----------------------------------------------------------------
def li_make_coeffs_from_xs_and_f(xs, f):
	return li_make_coeffs_from_xs_and_ys(xs, map(f, xs))

# ----------------------------------------------------------------
# Cubic case:
# c0 *          (x-x1)*(x-x2)*(x-x3) + \
# c1 * (x-x0)         *(x-x2)*(x-x3) + \
# c2 * (x-x0)*(x-x1)         *(x-x3) + \
# c3 * (x-x0)*(x-x1)*(x-x2) 

def li_eval(x, xs, cs):
	n = len(xs)
	sum = 0.0
	for i in range(0, n):
		term = cs[i]
		for j in range(0, n):
			if (i != j):
				term *= x - xs[j]
		sum += term
	return sum

#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2008-02-04
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
import sp_funcs_m # For beta(a, b)

# ----------------------------------------------------------------
# For 0 < x < 1, betapdf(x) is
#
#   x**(alpha-1) * (1-x)**(beta-1)
#   ------------------------------
#           B(alpha, beta)
#
# where B(alpha, beta) is simply what it needs to be to normalize
# the denominator, namely,
#
#   B(alpha, beta) = int_0^1 x**(alpha-1) * (1-x)**(beta-1) dx.
#
# This may also be written as
#
#                    Gamma(alpha) * Gamma(beta)
#   B(alpha, beta) = --------------------------.
#                       Gamma(alpha + beta)

def betapdf(x, alpha, beta):
	return x**alpha * (1.0-x)**beta / sp_funcs_m.beta(alpha, beta)

# You can call this instead if you've already got the denominator.
# This simply avoids redundant computation.
def betapdfaux(x, alpha, beta, denom):
	return x**alpha * (1.0-x)**beta / denom
def betapdfdenom(alpha, beta):
	return sp_funcs_m.beta(alpha, beta)

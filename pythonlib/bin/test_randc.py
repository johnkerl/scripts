#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2008-02-06
#
# Test code for randc_m.py.
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
import randc_m
import sys
from   cplxreal_m import *
import stats_m

# ----------------------------------------------------------------
def report(Zs):
	Z2s = []
	abses = []
	phzes = []
	reals = []
	imags = []
	for Z in Zs:
		Z2s.append(conj(Z)*Z)
		abses.append(abs(Z))
		phzes.append(phz(Z))
		reals.append(real(Z))
		imags.append(imag(Z))
		if (print_details):
			print "%11.7f %11.7f" % (Z.real, Z.imag)
			#print "%11.7f %11.7f" % (abs(Z), phz(Z))
	print
	print >> sys.stderr, "E[Z]      =", stats_m.find_mean(Zs)
	print >> sys.stderr, "E[|Z|^2]  =", stats_m.find_mean(Z2s)
	print >> sys.stderr, "E[abs(Z)] =", stats_m.find_mean(abses)
	print >> sys.stderr, "E[phz(Z)] =", stats_m.find_mean(phzes)
	print >> sys.stderr, "E[re(Z)]  =", stats_m.find_mean(reals)
	print >> sys.stderr, "E[im(Z)]  =", stats_m.find_mean(imags)
	print

# ----------------------------------------------------------------
def test_randc_unit(N, print_details):
	Zs = []
	for k in range(0, N):
		Z = randc_m.randc_unit()
		Zs.append(Z)
	report(Zs)

# ----------------------------------------------------------------
def test_randc_mean_sq_1(N, print_details):
	Zs = []
	for k in range(0, N):
		Z = randc_m.randc_mean_sq_1()
		Zs.append(Z)
	report(Zs)

# ----------------------------------------------------------------
def test_randc_normal(N, mu, sigma_squared, print_details):
	Zs = []
	for k in range(0, N):
		Z = randc_m.randc_normal(mu, sigma_squared)
		Zs.append(Z)
	report(Zs)

# ----------------------------------------------------------------
N=100
print_details = 1
if (len(sys.argv) == 2):
	N = int(sys.argv[1])

#test_randc_unit(N, print_details)
#test_randc_mean_sq_1(N, print_details)
test_randc_normal(N, 2.0+3.0j, 4.0, print_details)

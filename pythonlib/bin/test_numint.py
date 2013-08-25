#!/usr/bin/python -Wall

# ================================================================
# Copyright (c) John Kerl 2007
# kerl.john.r@gmail.com
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
from kerlutil import *
from cmath import *

def c(x):
	return 1.0
def i(x):
	return x
def f(z):
	return 1./z
def g(z):
	return sin(z)/z
def h(z):
	return exp(1j*z)/z

n=10000

s = numint(c, frange(2., 3., n)); print "%11.7f" % (s)
s = numint(i, frange(2., 3., n)); print "%11.7f" % (s)

s = numint(c, ztrange(1., 0, pi, n)); print "%11.7f %11.7f" % (s.real, s.imag)
s = numint(i, ztrange(1., 0, pi, n)); print "%11.7f %11.7f" % (s.real, s.imag)
print

s = numint(f, ztrange(1., 0, 2*pi, n)); print "%11.7f %11.7f" % (s.real, s.imag)
print

s = numint(g, ztrange(1., 0,   pi, n)); print "%11.7f %11.7f" % (s.real, s.imag)
s = numint(g, ztrange(1., pi,2*pi, n)); print "%11.7f %11.7f" % (s.real, s.imag)
s = numint(g, ztrange(1., 0, 2*pi, n)); print "%11.7f %11.7f" % (s.real, s.imag)
print

s = numint(h, ztrange(1., 0,   pi, n)); print "%11.7f %11.7f" % (s.real, s.imag)
s = numint(h, ztrange(1., pi,2*pi, n)); print "%11.7f %11.7f" % (s.real, s.imag)
s = numint(h, ztrange(1., 0, 2*pi, n)); print "%11.7f %11.7f" % (s.real, s.imag)
print

for R in [1., .8, .6, .4, .2, .1, .01, .001, .0001]:
	s1  = numint(h, ztrange(R, 0, pi, n))
	s2  = numint(h, ztrange(R, pi, 2*pi, n))
	s12 = numint(h, ztrange(R, 0, 2*pi, n))
	printf_row([R] + clist_to_rlist([s1, s2, s12]))

#  1.0000000
#  2.4999995

# -2.0000099   0.0000000
#  0.0000001  -0.0000000

#  0.0000002   6.2831849
#  0.0000003  -0.0000000

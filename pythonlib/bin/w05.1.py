#!/usr/bin/python -Wall

# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# Copyright (c) John Kerl 2007
# kerl.john.r@gmail.com
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
from kerlutil import *
from cmath import *

def f(z):
	return exp(1j*z)/(z-1j)**2

s = numint(f, mfrange(-20, 0.01, 20))
print "%11.7f %11.7f" % (s.real, s.imag)

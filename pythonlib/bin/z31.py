#!/usr/bin/python -Wall

# ================================================================
# Copyright (c) John Kerl 2007
# kerl.john.r@gmail.com
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
from math     import *
from cmath    import *
from kerlutil import *

# ----------------------------------------------------------------
def f(z):
	#return z**3 + 1
	return 1/(z**3 + 1)

# ----------------------------------------------------------------
tlo = 0
thi = 2*pi
nt = 1000
dt = (thi-tlo)/nt

for t in mfrange(tlo, dt, thi):
	ws = []
	#for R in [ .5, .6, .7, .8 ]:
	#for R in [ 1, 2, 3, 4 ]:
	for R in [ 2, 3, 4, 5 ]:
		z = R * exp(1j*t)
		w = f(z)
		ws.append(w)
	parts = []
	for w in ws:
		parts.append(w.real)
		parts.append(w.imag)
	printf_row([t] + parts, "%.7e")

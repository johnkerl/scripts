#!/usr/bin/python -Wall

from __future__ import division
from kerlutil import mfrange
from cmath import sqrt

ab_s = mfrange(-3.0, 0.02, 3.0)

for a in ab_s:
	for b in ab_s:
		# z^2 - a z - b
		D = a**2 + 4*b
		sqrt_D = sqrt(D)
		root1 = (a + sqrt_D) * 0.5
		root2 = (a - sqrt_D) * 0.5
		if abs(root1) < 1.0 and abs(root2) < 1.0:
			print a, b

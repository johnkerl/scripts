#!/usr/bin/python -Wall

from math import *

N=10
thetamin = 0.0
thetamax = pi
for k in range(0, N+1):
	theta = thetamin + (thetamax - thetamin) * k / N
	x = cos(theta)
	y = sin(theta)
	print '%11.7f %11.7f %11.7f' % (theta, x, y)

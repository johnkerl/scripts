#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2009-02-02
# ================================================================

from   __future__ import division
import sys
import random

N = 100000
p = 0.5

if len(sys.argv) == 2:
	p = float(sys.argv[1])
if len(sys.argv) == 3:
	p = float(sys.argv[1])
	N = int(sys.argv[2])

sX  = 0.0
sX2 = 0.0
for i in range(0, N):
	X = -1
	if (random.uniform(0, 1) < p):
		X = 1
	#print X
	sX  += X
	sX2 += X**2

EX  = sX  / N
EX2 = sX2 / N
VarX = EX2 - EX**2

print "N      = %d"     % (N)
print "p      = %11.7f" % (p)
print "E[X]   = %11.7f" % (EX)
print "E[X^2] = %11.7f" % (EX2)
print "Var(X) = %11.7f" % (VarX)

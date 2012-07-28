#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2009-02-02
# ================================================================

from   __future__ import division
import sys
import random

N = 100
p = 0.5

if len(sys.argv) == 2:
	p = float(sys.argv[1])
if len(sys.argv) == 3:
	p = float(sys.argv[1])
	N = int(sys.argv[2])

for i in range(0, N):
	U = 0
	if (random.uniform(0, 1) < p):
		U = 1
	print U

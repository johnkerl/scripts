#!/usr/bin/python -Wall

# ================================================================
# Copyright (c) John Kerl 2007
# kerl.john.r@gmail.com
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
import random
from stats_m import *

N=10000
xarray=[]
for i in range(0, N):
	xarray.append(random.normalvariate(0, 1))
for i in range(0, N/2):
	xarray.append(random.normalvariate(3, .5))

if 1:
	for x in xarray:
		print x
else:
	h=0.1
	plot_kde(xarray, h, -3, 6, 300)

#!/usr/bin/python -Wall

# ================================================================
# Copyright (c) John Kerl 2007
# kerl.john.r@gmail.com
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
from normal_m import *

#for x in [ 0.001, 0.01, 0.1, 0.25, 0.5, 1, 2, 4, 10, 100, 1000 ]:
#	#print x, erftaylor(x), erfsmallx(x), erfbigx(x)
#	print x, erf(x)
#	#erftaylor(x)
#	#print
#	#erfsmallx(x)
#	#print
#	#erfbigx(x)
#	#print
#	#print

#for x in [ 0.001, 0.01, 0.1, 0.25, 0.5, 1, 2, 4, 10, 100, 1000 ]:
#	print x, erf(x)

for x in frange(0.01, 0.99, 20):
	y = inverf(x)
	z = erf(y)
	print x, y, z, z-x
print
for x in [0.00001, 0.0001, 0.001, 0.01, 0.1]:
	y = inverf(x)
	z = erf(y)
	print x, y, z, z-x
print
print
for x in frange(0.01, 0.99, 20):
	y = invnorm(x)
	z = normalcdf(y)
	print x, y, z, z-x
print
for x in [0.00001, 0.0001, 0.001, 0.01, 0.1]:
	y = invnorm(x)
	z = normalcdf(y)
	print x, y, z, z-x
print
print

#for x in frange(0.01, 0.99, 20):
#	y = invnorm(x)
#	z = normalcdf(y)
#	print x, y, z, z-x
##print
##for x in [0.00001, 0.0001, 0.001, 0.01, 0.1]:
##	y = invnorm(x)
##	z = normalcdf(y)
##	print x, y, z, z-x


#for x in [.5, .4, .3, .2, .1, .08, .06, .04, .02, .01, .005]:
#	print x, invnorm(x)
#	print
#print invnorm(0.001)

#inverf(0.1)

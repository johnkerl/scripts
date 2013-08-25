#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2008-02-06
#
# Pseudorandom scalar-complex routines layered on top of Python's (real)
# random module.
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
import random
import math
from cplxreal_m import *

# ----------------------------------------------------------------
def randc_unit():
	phz = random.uniform(0.0, 2.0*math.pi)
	return complex(math.cos(phz), math.sin(phz))

# ----------------------------------------------------------------
def randc_mean_sq_1():
	s = 0.70710678118654746 # 1.0/math.sqrt(2.0)
	re = random.gauss(0.0, s)
	im = random.gauss(0.0, s)
	return complex(re, im)

# ----------------------------------------------------------------
def randc_normal(mu, sigma_squared):
	s = 0.70710678118654746 # 1.0/math.sqrt(2.0)
	scale = sigma_squared * s
	re = random.gauss(real(mu), scale)
	im = random.gauss(imag(mu), scale)
	return complex(re, im)


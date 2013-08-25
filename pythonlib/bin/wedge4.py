#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
from sackmat_m import *
from sackst_m import *
import random

a=1
b=0
c=0
d=0
e=0
f=1

A = simple_tensor([ \
	[  0,  a,  b, c], \
	[ -a,  0,  d, e], \
	[ -b, -d,  0, f], \
	[ -c, -e, -f, 0]])

AA = A ^ A

AA.printf()

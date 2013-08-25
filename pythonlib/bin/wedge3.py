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

u = simple_tensor([-1,2,3])
v = simple_tensor([4,-5,6])
w = simple_tensor([7,8,-9])

uv = u ^ v
vw = v ^ w
uw = u ^ w
uvw = u ^ v ^ w

print "u^v:"; uv.printf()
print "u^w:"; uw.printf()
print "v^w:"; vw.printf()
print "u^v^w:"; uvw.printf()

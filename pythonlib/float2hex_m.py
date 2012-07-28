#!/usr/bin/python

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-15
# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
import struct

def float2hex(x):
    p = struct.pack  ("!f", x)
    i = struct.unpack("!I", p)
    s = "%08x" % (int(i[0]))
    return s

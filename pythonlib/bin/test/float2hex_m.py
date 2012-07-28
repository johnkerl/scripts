#!/usr/bin/python

import struct

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-15
# ================================================================

def float2hex(x):
    p = struct.pack  ("!f", x)
    i = struct.unpack("!I", p)
    s = "%08x" % (int(i[0]))
    return s
